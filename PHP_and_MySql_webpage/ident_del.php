<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$ssn = $_GET["ssn_change"];
$ident = $_GET["ident_del"];

$del_sql = "DELETE FROM ELECTRONIC_ADDRESS WHERE SSN='$ssn' AND Identifier='$ident';";

( $d = mysql_query( $del_sql )) or die (mysql_error());

header('Location: account.html');
exit;
?>
