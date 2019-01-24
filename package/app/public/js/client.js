function request(success, error) {
	var ajax = new XMLHttpRequest();
	ajax.addEventListener('load', function() {
			if (ajax.status >= 200 && ajax.status < 400) {
				success(JSON.parse(ajax.responseText), ajax.status);
			} else {
				error(ajax.status)
			}
	});
	
	ajax.addEventListener('error', function() {
		error(ajax.status)
	});
	
	return ajax
}

function get(url, success, error) {
	ajax = request(success, error);
	ajax.open("GET", url, true);
	ajax.send();
}

