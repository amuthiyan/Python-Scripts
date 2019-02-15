<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$ssn = $_GET["ssn_change"];
$email = $_GET["email_change"];

$update_sql = "UPDATE ELECTRONIC_ADDRESS SET Identifier='$email' WHERE SSN='$ssn' AND Type='email';";

( $u = mysql_query( $update_sql )) or die (mysql_error());
header('Location: account.html');
exit;
?>
