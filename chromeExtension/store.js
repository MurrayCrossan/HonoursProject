function handleUpdated(tabId, changeInfo, tab) {
	if (changeInfo.url) {
		page_visited = tab.url;
		var xhr = new XMLHttpRequest();
		var url = "http://127.0.0.1:5000/url?url=";
		var query = url + String(tab.url);
		var body = xhr.response;
		
		xhr.open("GET", query);
		xhr.send();
		
		xhr.onreadystatechange = function() {
			if (xhr.readyState === 4) {
				var parser = new DOMParser()
				var responseDoc = parser.parseFromString(xhr.responseText, "text/html")
				var phish_or_legit = responseDoc.getElementById("phish_or_legit").innerHTML
				if (phish_or_legit === "Phishing") {
						alert("The following webpage: \n" + tab.url + " has been predictied to be: " + phish_or_legit)
				}
			}
		}
	}
}

chrome.tabs.onUpdated.addListener(handleUpdated)