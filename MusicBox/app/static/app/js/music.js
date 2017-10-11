
function hide(){
	var h = setTimeout(
				function () {
					$('#profilephoto').popover('hide');
				}, 3000
			);
}

var playlist,x,slider,processor,controller;
var Pflag = 0;
var Lflag = 0;
var loginflag = 0;
var Var,playM;
var degs = 0;
var count = 0;
var gettimes = 0;

window.onload = function(){
    x = document.getElementById("source");
    getinfo();
	
	slider = document.getElementById("slider");
	processor = document.getElementById("processor");
	controller = document.getElementById('controller');

	slider.addEventListener("click",dragDropHandler);
	controller.addEventListener("mousedown",dragDropHandler);
	controller.addEventListener("mouseup",dragDropHandler);
	
}

function movecontroller(){
	var movelen = event.clientX - slider.offsetWidth;
	if(movelen < 90){movelen = 90;}
	if(movelen > 555){movelen = 555;}
	controller.style.left = (-5 + movelen - 90 ) + "px";
	processor.style.width = (8 + movelen - 90 ) + "px";
}

function movemusic(){
	var time = x.duration;
	if( isNaN(time) ){ return; }
	var movelen = event.clientX - slider.offsetWidth;
	if(movelen < 90){movelen = 90;}
	if(movelen > 555){movelen = 555;}
	x.currentTime = (movelen - 90)/465.0 * time;
}

function dragDropHandler(event){
	switch(event.type){
		case "click":{
			movecontroller();
			movemusic();
			Pflag = 0;
			clearInterval(Var);
			playmusic();
			break;
		}
		case "mousedown":{
			Pflag = 0;
			clearInterval(Var);
			controller.style.cursor = "pointer";
			$("#controller").css("box-shadow","0px 0px 12px #FFFFFF");
			slider.addEventListener("mousemove",dragDropHandler);
			break;
		}
		case "mouseup":{
			slider.removeEventListener("mousemove",dragDropHandler);
			$("#controller").css("box-shadow","2px 4px 12px #000000");
			movecontroller();
			movemusic();
			playmusic();
			break;
		}
		case "mousemove":{
			movecontroller();
			break;
		}			
	}
}

function playmusic(){
	if (Pflag == 0){
		$('#play').attr('src',"/static/app/img/pause.png");
		x.play();
		playslider();
		Var = setInterval(function(){playslider()},500);
		Pflag = 1;
	}
	else{
		$('#play').attr('src',"/static/app/img/play.png");
		clearInterval(Var);
		x.pause();
		Pflag = 0;
	}
}

function endmusic(){
	Pflag = 0;
	clearInterval(Var);
	degs = 0;
	$("#cover").css("transform","rotate("+ degs +"deg) scale(0.6,0.6)");
	controller.style.left = -5 + "px";
	processor.style.width = 8 + "px";
}

function stopmusic(){
	$('#play').attr('src',"/static/app/img/play.png");
	endmusic();
	x.load();
}

function nextmusic() {
    $('#like').attr("src", "/static/app/img/dislike.png");
    Lflag = 0;
	endmusic();
	setinfo();
	playmusic();
}

function likemusic() {
    if (loginflag == 0) {
        alert("请登录后操作！");
        return;
    }
	if(Lflag == 0){
	    $('#like').attr("src", "/static/app/img/like.png");
	    Lflag = 1;
	    var csrftoken = getCookie('csrftoken');
	    var req = new XMLHttpRequest();
	    req.open("POST", "/like", true);
	    req.setRequestHeader('X-CSRFToken', csrftoken);
	    req.setRequestHeader("Content-type", "application/json; charset=UTF-8");
	    req.send('{"username":"' + $("#showmes").text() + '","songurl":"' + x.src + '","imgurl":"' + $("#cover").attr("src") + '","songmes":"' + $("#songmes").text() + '"}');
	}
	else{
		$('#like').attr("src","/static/app/img/dislike.png");
		Lflag = 0;
	}
}

function playslider(){
	var time = x.duration;
	if( isNaN(time) ){ return; }
	if(x.ended){
		nextmusic();
		return;
	}
	degs += 10;
	var curtime = x.currentTime;
	var len = parseFloat($("#slider").css("width").replace("px","")) - 8 ;
	var movelength = (curtime / time) * len;
	controller.style.left = (-5 + movelength) + "px";
	processor.style.width = (8 + movelength) + "px";
	$("#cover").css("transform","rotate("+ degs +"deg) scale(0.6,0.6)");
}

function getinfo() {
	var req = new XMLHttpRequest();
	req.open("GET", "/get_info?key="+ gettimes, true);
	req.send();
	req.onreadystatechange = function () {
	    if (req.readyState == 4 && req.status == 200) {
	        var text = req.responseText;
	        playlist = JSON.parse(text);
	        setinfo();
	    }
	}
	if (gettimes == 1) {
	    gettimes = 0;
	}
	else {
	    gettimes = 1;
	}
}

function setinfo(){
	if(count == playlist.num){
		playlist = getinfo();
		count = 0;
	}
	x.src = playlist.songmes[count].url;
	$("source").attr("src", playlist.songmes[count].url);
	$("#songmes").text(playlist.songmes[count].songname + "_" + playlist.songmes[count].singername);
	$("#cover").attr("src", playlist.songmes[count].img);
	count++;
}

function searchsong() {

    $("#searchModal .modal-body").html('<marquee behavior="srcoll" style="font-size:40px;">Plz waitting...</marquee>');
    $('#searchModal').modal({ backdrop: 'static' });
	var req = new XMLHttpRequest();
	req.open("GET", "/search_info?keyword=" + $("#box").val() +"&size=20&page=1", true);
	req.send();
	req.onreadystatechange = function () {
	    if (req.readyState == 4 && req.status == 200) {
	        var text = req.responseText;
	        var list = JSON.parse(text);
	        if (list.num == 0) {
	            $("#searchModal .modal-body").html('<h2 style="text-align: center;">No Results,Plz try other!</h2>');
	            return;
	        }
	        var contain = "";
	        for (var i = 0; i < list.num; i++) {
	            contain += "<tr><td>" + list.songmes[i].songname + "</td><td>" + list.songmes[i].singername +
                "</td><td><a href='javascript:void(0)' onclick='playM(" + i + ")'>Touch me</a></td></tr>"
	        }
	        $("#searchModal .modal-body").html('<table class="table table-striped">\
					  <thead>\
						<tr>\
						  <th>SongName</th>\
						  <th>Singer</th>\
						  <th>Click to play</th>\
						</tr>\
					  </thead>\
					  <tbody>'
						+ contain +
						'</tr>\
					  </tbody>\
					</table>');
	        playM = function (index) {
	            x.src = list.songmes[index].url;
	            $("#songmes").text(list.songmes[index].songname + "_" + list.songmes[index].singername);
	            $("#cover").attr("src", list.songmes[index].img);
	            $('#like').attr("src", "/static/app/img/dislike.png");
	            Lflag = 0;
	            endmusic();
	            playmusic();
	            $('#searchModal').modal('hide');
	        }
	    }
	}
}

function userlog(){
	if(loginflag == 0){
		$('#loginModal').modal({ backdrop: 'static' });
	    $('#loginModal').modal('show');
	}
	else{
		$('#profilephoto').popover('dispose');
		$("#profilephoto").attr("src","/static/app/img/c.jpg");
		$("#showmes").text("LOGIN");
		loginflag = 0;
	}
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?  
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function userlogin(){
	var name = $("#name").val();
	var pass = $("#pass").val();
	if (name == "" || pass == "") {
	    alert("用户名或密码为空！");
	    return;
	}
	if (!CheckEmail(name)) {
	    alert("请输入正确的邮箱地址！");
	    return;
	}
	if (pass.length > 20) {
	    alert("密码位数限制在20个字符以内！");
	    return;
	}

	var csrftoken = getCookie('csrftoken');
	var req = new XMLHttpRequest();
	req.onreadystatechange = function () {
	    if (req.readyState == 4 && req.status == 200) {
	        var text = req.responseText;
	        if (text == 'error') {
	            alert('请求有误！');
	        }else if(text == 'incorrect'){
	            alert('用户名或密码有误！');
	        } else {
	            alert('Welcome to the MusixBox！');
	            $("#name").val("");
	            $("#pass").val("");
	            var text = req.responseText;
	            var usermes = JSON.parse(text);
	            $("#profilephoto").attr("src", usermes.userimg);
	            $("#showmes").text(usermes.username);
	            $('#profilephoto').popover('dispose');
	            $('#profilephoto').popover({
	                title: usermes.username,
	                html: true,
	                content: usermes.usermotto +
                    "<br><a href='javascript:void(0)' style='border-top-style: solid;\
		border-width: 1px;border-color: #DDDDDD;' onclick='putimg()'>click to switch the avatar</a></br>",
	                placement: "bottom",
	            });
	            $('#loginModal').modal('hide');
	            recommendmusic();
	            loginflag = 1;
	        }
	    }
	}
	req.open("POST", "/login", true);
	req.setRequestHeader('X-CSRFToken', csrftoken);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.send("username=" + name + "&userpass=" + pass);
}

function putimg(){
	var imgurl=prompt("请输入400*400图片URL：","");
	if(imgurl != null && imgurl !=""){
	    CheckImgExists(imgurl);
	}
	else{
	    alert("输入为空！");
	}
}

function CheckImgExists(imgurl) {
    var ImgObj = new Image();
    ImgObj.src = imgurl;
    ImgObj.onerror = function () {
        alert("请输入正确的400*400的图片地址!");
        return;
    }
    ImgObj.onload = function () {
        if (ImgObj.width == 400 && ImgObj.height == 400) {
            $("#profilephoto").attr("src", imgurl);
            var csrftoken = getCookie('csrftoken');
            var req = new XMLHttpRequest();
            req.onreadystatechange = function () {
                if (req.readyState == 4 && req.status == 200) {
                    var text = req.responseText;
                    if (text == "error") {
                        alert("请求有误！");
                    }
                    else if(text == "incorrect"){
                        alert("更改失败！");
                    }else{
                        alert("更改成功！");
                    }
                }
            }
            req.open("POST", "/imgset", true);
            req.setRequestHeader('X-CSRFToken', csrftoken);
            req.setRequestHeader("Content-type", "application/json; charset=UTF-8");
            req.send('{"username":"' + $("#showmes").text() + '","imgurl":"' + imgurl +'" }');
        }
        else {
            alert("请输入正确的400*400的图片地址!");
        }
    }
}

function CheckEmail(email) {
    var szReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var bChk = szReg.test(email);
    return bChk;
}

function userreg() {
    $('#loginModal').modal('hide');
    $('#registModal').modal({ backdrop: 'static' });
    $('#registModal').modal('show');
}

function userregist() {
    var name = $("#rname").val();
    var pass = $("#rpass").val();
    if (name == "" || pass == "") {
        alert("用户名或密码为空！");
        return;
    }
    if (!CheckEmail(name)) {
        alert("请输入正确的邮箱地址！");
        return;
    }
    if (pass.length > 20) {
        alert("密码位数限制在20个字符以内！");
        return;
    }
    console.log("rname:", name);
    console.log("rpass:", pass);
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var text = req.responseText;
            if (text == 'error') {
                alert('请求有误！');
            } else if (text == 'incorrect') {
                alert('用户名已注册！');
            } else {
                alert('Welcome to the MusixBox！');
                $("#rname").val("");
                $("#rpass").val("");
                var text = '{ \
"name" : "usermes",\
"userid" : 1,\
"username" : "' + name + '",\
"userimg" : "/static/app/img/c.jpg",\
"usermotto" : "To be,or not to be."\
}'
                var usermes = JSON.parse(text);
                $("#profilephoto").attr("src", usermes.userimg);
                $("#showmes").text(usermes.username);
                $('#profilephoto').popover('dispose');
                $('#profilephoto').popover({
                    title: usermes.username,
                    html: true,
                    content: usermes.usermotto +
                    "<br><a href='javascript:void(0)' style='border-top-style: solid;\
		border-width: 1px;border-color: #DDDDDD;' onclick='putimg()'>click to switch the avatar</a></br>",
                    placement: "bottom",
                });
                $('#registModal').modal('hide');
                loginflag = 1;
            }
        }
    }
    req.open("POST", "/regist", true);
    req.setRequestHeader('X-CSRFToken', csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("username=" + name + "&userpass=" + pass);
}

function recommendmusic() {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            var text = req.responseText;
            playlist = JSON.parse(text);
            count = 0;
            setinfo();
        }
    }
    req.open("GET", "/recommend?username=" + $("#showmes").text(), true);
    req.send();
    
}
