<?PHP

$input = $_GET['input'];
$conn = new mysqli('localhost','root','','internetandapplications');
if ($conn->connect_error){
	die("Connection failed: ". $conn->connect_error);
}
$query = "SELECT country_name , count(DISTINCT c.nct_id) as cnt FROM `trials` c join `country` t on c.nct_id = t.nct_id   join `condition` co on c.nct_id=co.nct_id join `mesh_term` mt on c.nct_id =mt.nct_id where official_title LIKE '%".$input."%' or brief_title LIKE '%".$input."%' or acronym LIKE '%".$input."%' or term LIKE '%".$input."%' or cond LIKE '%".$input."%' group by country_name order by cnt DESC";
$result = $conn->query($query) or die($conn->error);;
$data=array();
while ( $row = $result->fetch_assoc()){
	$data[] = $row;
}
echo json_encode($data);
$conn->close();

?>