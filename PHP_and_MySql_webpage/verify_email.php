<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

//get values from html form
$ident = $_GET["ident"];
$code = $_GET["code"];

$verify_ident = "UPDATE ELECTRONIC_ADDRESS SET Verified=1 WHERE Identifier='$ident';";
( $b = mysql_query( $verify_ident ));

header('Location: account.html');
exit;
?>
