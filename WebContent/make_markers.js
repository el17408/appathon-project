//synchronous
function httpGet2(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

//asynchronous
function httpGet(theUrl)
{
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
	    xmlHttp.onreadystatechange = function(){ 
	    	if (this.readystate === 4 && this.status === 200) {
	        	return this.responseText;
	    	}
	    }
		xmlHttp.send( null );
	    return xmlHttp.responseText;
}