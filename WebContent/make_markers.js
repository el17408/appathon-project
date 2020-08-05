
$(document).ready(function() {
    // execute
	(function() {   
			
	    var input = getUrlVars()["search"];
		if (input === "" || input === " " || input == undefined || input == null) {
			return;
		}
		input = input.split("+");	//remove all occurances of +
		input = input.join(' ');	// and replace them with a space
		 if (getUrlVars()["format"] == "map"){
			createOutput(JSON.parse(httpGet("http://localhost:8080/appathon_project/sql_request.php?input="+input)),"map");
		}
		else if(getUrlVars()["format"] == "json") {
			createOutput(JSON.parse(httpGet("http://localhost:8080/appathon_project/sql_request.php?input="+input)),"json");
	    		}
	    return;
	    })();
	});
	    	
		function getUrlVars() {
    	        var vars = {};
    	        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
        return vars;
}
	function createOutput( output , format ) {
		var toReturn = [];
		
		for(var i = 0; i < output.length; i++) {
			var request = JSON.parse(httpGet("https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDR919QvVF2Y632fs9uwdASsOAiVaykJd4&address="+output[i].country_name));
			if (request.status == "ZERO_RESULTS") {
				continue;
			}
			else{
			
				output[i]["lat"] = request.results[0].geometry.location.lat;
				
				output[i]["lng"] = request.results[0].geometry.location.lng;
				toReturn.push(output[i]);
			}
		}
		if (format == "map"){
			return makeMarkers(toReturn);
		}
		else {
			if(toReturn.length == 0){
				document.body.innerHTML= "{status : Zero_Results}";
				return;
			}
			toReturn.push({status:200});
			document.body.innerHTML= JSON.stringify(toReturn);
			return;
		}
	}
	
	function httpGet(theUrl)
	{
		if (window.XMLHttpRequest){
		 	var xmlHttp = new XMLHttpRequest();
		 }
		 else {
			 var xmlHttp = new ActiveObject("Microsoft.XMLHTTP");
		 }
	    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
	    xmlHttp.send( null );
	    return xmlHttp.responseText;
	}
	
	
	function makeMarkers(arr){
		var options = {
	                    zoom: 2,
	                    center: new google.maps.LatLng(45.8665231, -6.9240942), 
	                    mapTypeId: google.maps.MapTypeId.TERRAIN,
	                    mapTypeControl: false
	                };
	
	    // init map
		var map = new google.maps.Map(document.getElementById('map_canvas'), options);
		for (var i = 0; i < arr.length; i++) {
			// init markers
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(arr[i].lat, arr[i].lng),
				map : map,
				title: arr[i].country_name,
				label : arr[i].cnt
			});
		}
	}


//synchronous
function httpGet2(theUrl)
{
	if (window.XMLHttpRequest){
	 	var xmlHttp = new XMLHttpRequest();
	 }
	 else {
		 var xmlHttp = new ActiveObject("Microsoft.XMLHTTP");
	 }
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

//asynchronous
function httpGet3(theUrl)
{
	if (window.XMLHttpRequest){
	 	var xmlHttp = new XMLHttpRequest();
	 }
	 else {
		 var xmlHttp = new ActiveObject("Microsoft.XMLHTTP");
	 }
	    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
	    xmlHttp.onreadystatechange = function(){ 
	    	if (this.readystate === 4 && this.status === 200) {
	        	return this.responseText;
	    	}
	    }
		xmlHttp.send( null );
	    return xmlHttp.responseText;
}