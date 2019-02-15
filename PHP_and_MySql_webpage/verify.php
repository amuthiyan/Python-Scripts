<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

//get values from html form
$bank_id = $_GET["bankid_ver"];
$bank_number = $_GET["banumber_ver"];
$code = $_GET["code"];

$verify_bank = "UPDATE USER_ACCOUNT SET PBAVerified=1 WHERE BankID='$bank_id' AND BANumber='$bank_number';";
( $b = mysql_query( $verify_bank ));

$verify_additional = "UPDATE HAS_ADDITIONAL SET Verified=1 WHERE BankID='$bank_id' AND BANumber='$bank_number';";
( $v = mysql_query( $verify_additional ));

header('Location: account.html');
exit;
?>
