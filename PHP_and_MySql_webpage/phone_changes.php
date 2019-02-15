<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$ssn = $_GET["ssn_change"];
$phone = $_GET["phone_change"];

$update_sql = "UPDATE ELECTRONIC_ADDRESS SET Identifier='$phone' WHERE SSN='$ssn' AND Type='phone';";

( $u = mysql_query( $update_sql )) or die (mysql_error());
header('Location: account.html');
exit;
?>
