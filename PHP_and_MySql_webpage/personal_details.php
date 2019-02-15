<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

//get values from html form
$ssn = $_GET["ssn"];
$user_name = $_GET["name"];
$bank_id = $_GET["bankid"];
$bank_number = $_GET["banumber"];
$email_id = $_GET["email"];
$phone_number = $_GET["phone"];

//Initialize bank account if not there
$insert_bank = "INSERT INTO BANK_ACCOUNT (BankID, BANumber) VALUES('$bank_id','$bank_number');";
( $b = mysql_query( $insert_bank ));


$insert_sql = "INSERT INTO USER_ACCOUNT (SSN, Name, Balance , BankID, BANumber) VALUES ($ssn,'$user_name', 10000 ,'$bank_id',$bank_number);";
( $t = mysql_query( $insert_sql )) or die (mysql_error());

//Insert Email
$insert_email = "INSERT INTO ELECTRONIC_ADDRESS (Identifier, SSN, Type) VALUES ('$email_id', $ssn, 'email');";
( $e = mysql_query( $insert_email )) or die (mysql_error());

//Insert Phone Number
$insert_phone = "INSERT INTO ELECTRONIC_ADDRESS (Identifier, SSN, Type) VALUES ('$phone_number', $ssn, 'phone');";
( $p = mysql_query( $insert_phone )) or die (mysql_error());

header('Location: account.html');
exit;
?>
