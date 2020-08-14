<%@page import="appathon_ntua.Servlet"%>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
         <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        
        <title>Appathon project</title>
        
		<!-- Load stylesheet -->
		<link rel="stylesheet" type="text/css" href="styles.css">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
		
		<!-- Load favicon -->
		<link rel="icon" type="image/x-icon" href="favicon.ico">
		
		
        <!-- Load js files to use with google maps -->
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDR919QvVF2Y632fs9uwdASsOAiVaykJd4" type="text/javascript"></script>
        <script type="text/javascript">
        $(document).ready(function() {
            // execute
        	(function() {
					var country='<%=session.getAttribute("countries")%>';
					var count='<%=session.getAttribute("counters")%>';
					if (country == "undefined" || country == "null" || country == undefined || country == null || country == 'null' || country == 'undefined'){
						initMap();
						return;
					}
					//transform country,count from string to array
					country = country.replace(/^\[|\]$/g, "").split(", ");
					count = count.replace(/^\[|\]$/g, "").split(", ");
					var format='<%=session.getAttribute("format")%>';
					createOutput(country,count,format)					
				
			})();
    	});
        function createOutput( country , count, format ) {
    		var toReturn= [];
    		for(var i = 0; i < country.length; i++) {
    			//the key is exposed. Should be a session attribute...
    			var request = JSON.parse(httpGet("https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDR919QvVF2Y632fs9uwdASsOAiVaykJd4&address="+country[i]));
    			if (request.status == "ZERO_RESULTS" || request.status == "INVALID_REQUEST") {
    				continue;
    			}
    			else{
    				//create json object and add it to the array
    				toReturn.push({country_name: country[i],
    								lat: request.results[0].geometry.location.lat,
    								lng: request.results[0].geometry.location.lng,
    								cnt: count[i]});
    				
    			}
    		}
    		if (format == "map"){
    			return makeMarkers(toReturn);
    		}
    		else if (format == "json") {
    			if(toReturn.length == 0){
    				document.body.innerHTML= "{status : Zero_Results}";
    				return;
    			}
    			toReturn.push({status:200});
    			document.body.innerHTML= JSON.stringify(toReturn);
    			return;
    		}
    		return;
    	}
    	
    	
        function initMap() {
	        // map options
	        var options = {
	            zoom: 2,
	            center: new google.maps.LatLng(45.8665231, -6.9240942), // center map
	            mapTypeId: google.maps.MapTypeId.TERRAIN,
	            mapTypeControl: false
	        };

	        // init map
	        var map = new google.maps.Map(document.getElementById('map_canvas'), options);
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
    			if (arr[i].cnt == undefined )
    				arr[i].cnt = "1";
    			var marker = new google.maps.Marker({
    				position: new google.maps.LatLng(arr[i].lat, arr[i].lng),
    				map : map,
    				title: arr[i].country_name,
    				label : arr[i].cnt
    			});
    		}
    	}
    	
    	function httpGet(theUrl) // synchronous xml http request
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
	</script>
		
    </head>
    <body>
    
    <!-- Gif while loading data , doesn't work properly -->
    <div class="loader-wrapper">
    	<span class="loader"><span class="loader-inner"></span></span>
    </div>
    
    <div>
		  
		<!-- The form -->
		<form class="example" action="appathonservlet" id="formid" method="post" >
		<a href="http://localhost:8080/appathon_ntua/"><img src="logo.jpg" title="NTUA" ></a>
		
		
		  <input type="text" placeholder="Search for a diseace..." id="search" name="search">
		  <button form="formid" type="submit" ><i class="fa fa-search"></i></button>
		  <br>
		  
		<!-- The radio buttons -->
		  <input type="radio" id="format" name="format" value="map" checked>
		  	<label for="map">Map</label>
		  <input type="radio" id="format" name="format" value="json">
		  	<label for="json">json</label>
		</form>	
			
		<!-- The google maps div -->
        <div id="map_canvas" style="width: 1326px; height:567px;"></div>
       </div>
    
    <footer class="footer-container text-center">
    	<div class="container">
    		<p>© Website created by Dimitris Roussis 
    			<a href="https://github.com/el17408/appathon-project" title="" class="fa-icon">
    				<i class="fa fa-github"></i>
    			</a>
    		</p>
    	</div>
    </footer>
    
    <!-- Script to remove loader after page is loaded -->
    <script>
    	$(window).on("load",function(){
    		$(".loader-wrapper").fadeOut("slow");
    	});
    	
    </script>
 </body>
    
</html>