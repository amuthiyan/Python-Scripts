<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$req_id = $_GET["req_id"];
$req_ssn = $_GET["req_ssn"];
$ident = $_GET["identifier"];
$memo = $_GET["memo"];
$amount = $_GET["amount"];

$ssn_check = "SELECT(SSN) FROM ELECTRONIC_ADDRESS WHERE Identifier = '$ident';";
($ssn_temp = mysql_fetch_assoc(mysql_query( $ssn_check ))) or die (mysql_error());

$ssn_rec = $ssn_temp["SSN"];

//Get current datetime
$curr_date = date("Y/m/d h:i:sa");

$sql_insert_req = "INSERT INTO REQUEST_TRANSACTION (RTid, Amount, Datetime, Memo, SSN) VALUES ('$req_id',$amount,'$curr_date','$memo','$req_ssn');";
( $t = mysql_query( $sql_insert_req )) or die (mysql_error());

$sql_insert_from = "INSERT INTO FROM_E (RTid, Identifier,Percentage) VALUES ('$req_id','$ident',100);";
( $h = mysql_query( $sql_insert_from ))or die (mysql_error());

header('Location: transaction.html');
exit;
?>
