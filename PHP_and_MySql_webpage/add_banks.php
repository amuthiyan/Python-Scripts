<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

//get values from html form
$ssn = $_GET["ssn_add"];
$bank_id = $_GET["bankid_add"];
$bank_number = $_GET["banumber_add"];

$insert_bank = "INSERT INTO BANK_ACCOUNT (BankID, BANumber) VALUES('$bank_id','$bank_number');";
( $b = mysql_query( $insert_bank ));

$insert_sql = "INSERT INTO HAS_ADDITIONAL (SSN, BankID, BANumber) VALUES ('$ssn','$bank_id','$bank_number');";

( $t = mysql_query( $insert_sql )) or die (mysql_error());

header('Location: account.html');
exit;
?>
