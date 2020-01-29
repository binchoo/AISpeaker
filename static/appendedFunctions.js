function passThis(a, e){
	e.preventDefault();
    var cursorX = e.pageX;
    //var cursorY = e.pageY+50;
    var cursorY = 20;
	var a_address = a.getAttribute('href');
	var div= document.createElement('div');
	div.setAttribute("style", "-moz-box-flex: 1;flex: 1 1 auto;margin: auto;position: absolute;inset: 0px;  background: rgba(0,0,0,0.3) none repeat scroll 0% 0%;z-index: 999;position: fixed;top: 0;  left: 0;bottom: 0;right: 0;z-index: 3;width: 100%;min-width:320px");
	div.style.zIndex = "999";
	div.classList.add('appendedArticleContent');
	var iframe = document.createElement('iframe');
	iframe.style.zIndex = "999";
	iframe.style.width="70%"
	iframe.style.height="100%"
	iframe.style.margin="0 15%";
	iframe.style.padding="8px";
	iframe.style.backgroundColor="white";
	iframe.style.border="none";
	console.log("Im a a "+ a_address);
	
	//iframe.style.display = "none";
	iframe.src = /* your URL here */a_address;
	div.appendChild(iframe);
	a.parentNode.appendChild(div);
	div.onclick = function(evt) {
		if(evt.target !== iframe) {
			a.parentNode.removeChild(div);
		}
	}
}
ignore_href_click = function(e) {
	e.preventDefault();
}

function imfromExternal(){
	alert("i'm from external .js!")
}