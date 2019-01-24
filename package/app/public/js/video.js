function thumbs(thumb, video_code) {
	ajax = get("/thumbs?thumb="+thumb+"&code="+video_code, function(response, http_code) {
		if (response.status == "ok"){
			if (response.thumb == "up") {
				tb = document.getElementById("thumbs_up_text")
				tb.textContent = parseInt(tb.textContent) + 1
			}
			if (response.thumb == "down") {
				tb = document.getElementById("thumbs_down_text")
				tb.textContent = parseInt(tb.textContent) + 1
			}
		}
	}, function (http_code) {
		
	});
}

document.getElementsByTagName('video')[0].addEventListener('error', function(event) {
	var elements = document.querySelectorAll(".vid");
	Array.prototype.forEach.call(elements, function(el, i){
		 el.parentNode.removeChild(el);
	});
	
	var p = document.getElementById("vid-wrapper");
    var newElement = document.createElement("div");
    newElement.innerHTML = "<h1>Sorry <span>:(</span></h1> <p>The video are not available.</p>";
    p.appendChild(newElement);
	
}, true);