
"use strict"

const releases = [
	"20231231",
	"20231231-debug",
	"20231226",
	"20231226-debug"
];

window.onload = function() {
	const release_list = document.getElementById("releases");
	for (const release of releases) {
		const basename = "stendhal-webview-" + release + ".apk";
		const anchor = document.createElement("a");
		anchor.href = "dist/" + basename;
		anchor.innerText = basename;
		const li = document.createElement("li");
		li.appendChild(anchor);
		release_list.appendChild(li);
	}
};
