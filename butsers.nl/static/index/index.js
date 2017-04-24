// Globals for navigation menu and content
	
	// Navigation menu sections
var navPages = [{NAVPAGESPACE}];	

	
	// Format is [id, styleparameters]
var navDivName = ['navigationHeader',{
	"magin": "11px",
	"padding": "13px",
	"font-size": "127%",
	"border-bottom-style": "groove"
	}];
var contDivName = ['displaySection',{}];

	// Add to create more divs on init
var dynamicDivNames = [navDivName, contDivName];



function pageToURLFormat(pageName) {
	/*
		Convert name of menu item to URL
	*/
	
	return "/?mod=" + pageName;
}

function hasSaneParameters(parameters) {
	/*
		Check if URL parameters are in allowed format
		Returns boolean
	*/

	allowedCharacters = 'abcdefghijklmnopqrstuvwxyz&=';
	maxLength = 127;

	if (parameters.length > maxLength)
		return false;

	for (index = 0; index < parameters.length; ++index)
		if (allowedCharacters.indexOf(parameters[index]) == -1)
			return false;
	
	return true;
}


function getPageFromHash() {
	/* 
		Gets both page and parameters from location hash
		Returns array of [nav page name, page url]
	*/

	h = location.hash;
	hParts = h.split("?");
	mainPage = hParts[0].substring(1);
	parameters = hParts[1];

	if (navPages.indexOf(mainPage) == -1 || !hasSaneParameters(parameters))
		return ['',''];

	return [mainPage, pageToURLFormat(mainPage) + "?" + parameters];
}

function editNavBar(currentPage) {
	/* 
		Build navigation menu and change navigation div 
	*/

	nav = document.getElementById(navDivName[0]);

	navMenu = [];

	for (index = 0; index < navPages.length; ++index) {

		menuName = navPages[index];

		if (menuName == currentPage)
			navMenu.push(menuName);
		else {
			val = '<a onclick="editNavBar(\''+menuName+'\');loadPage(\''+pageToURLFormat(menuName)+'\');">'+menuName+'</a>';
			navMenu.push(val);
		}
		
	}
	nav.innerHTML = navMenu.join(' - ');
}

function loadPage(currentURL, parameters) {
	/*
		Retrieve content from server and show on page
	*/

	cont = document.getElementById(contDivName[0]);
	cont.innerHTML = "Loading..";

	console.log('Retrieving: ' + currentURL);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4) {
			if (this.status == 200)
				cont.innerHTML = this.responseText;
			else
				cont.innerHTML = "Could not retrieve content: " + this.readyState;
		}
	};
	
	if (typeof parameters == 'undefined') {
		location.hash = currentURL;
		xhttp.open("GET", currentURL, true);
	}
	else {
		xhttp.open("POST", currentURL, true);
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhttp.send(parameters);	
	}

	xhttp.send();

}

function addDivToBody(divArray) {
	/*
		Add div to body
		Accepts array of [div id, div style parameters]
	*/

	divId = divArray[0];
	divStyleParameters = divArray[1];

	var newDiv = document.createElement('div');
	newDiv.id = divId;

	for (var property in divStyleParameters)
		newDiv.style.setProperty(property, divStyleParameters[property]); 

	document.getElementsByTagName('body')[0].appendChild(newDiv);

}

function initButsers() {
	/*
		Create page (navigation and content section)
		Load page from location hash
	*/

	// Create needed divs
	for (index = 0; index < dynamicDivNames.length; ++index)
		addDivToBody(dynamicDivNames[index]);

	// Load page from location hash
	vals = getPageFromHash();

	navPageName = vals[0];
	currentURL = vals[1];

	if (currentURL == '' || navPageName == '') {
		currentURL = pageToURLFormat(navPages[0]);
		navPageName = navPages[0];
	}

	editNavBar(navPageName);
	loadPage(currentURL);
}


initButsers();