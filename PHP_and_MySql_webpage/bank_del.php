<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$ssn = $_GET["ssn_del"];
$bankid = $_GET["bankid_del"];
$banumber = $_GET["banumber_del"];

$del_sql = "DELETE FROM HAS_ADDITIONAL WHERE SSN='$ssn' AND BankID='$bankid' AND BANumber = '$banumber';";

( $d = mysql_query( $del_sql )) or die (mysql_error());

header('Location: account.html');
exit;
?>
