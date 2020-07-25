<?PHP

$input = $_GET['input'];
$conn = new mysqli('localhost','root','','internetandapplications');
if ($conn->connect_error){
	die("Connection failed: ". $conn->connect_error);
}

$query = "SELECT country_name , count(*) as cnt from country c 
			join trials t on c.nct_id = t.nct_id where official_title 
			LIKE '%".$input."%' or brief_title LIKE '%".$input."%' or acronym 
			LIKE '%".$input."%' group by country_name order by cnt DESC";
$result = $conn->query($query) or die($conn->error);;
$data=array();
while ( $row = $result->fetch_assoc()){
	$data[] = $row;
}
echo json_encode($data);
$conn->close();

?>