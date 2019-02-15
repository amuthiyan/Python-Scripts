<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$transact_id = $_GET["transact_id"];
$send_ssn = $_GET["send_ssn"];
$ident = $_GET["identifier"];
$memo = $_GET["memo"];
$amount = $_GET["amount"];

//print $amount;

//Get the ssn of the person being sent money
$ssn_check = "SELECT(SSN) FROM ELECTRONIC_ADDRESS WHERE Identifier = '$ident';";
($ssn_temp = mysql_fetch_assoc(mysql_query( $ssn_check ))) or die (mysql_error());



$ssn_receiver = $ssn_temp["SSN"];
//print $ssn_receiver;


//Add sent money to the balance of receiving user
$sql_add_money = "UPDATE USER_ACCOUNT SET Balance = Balance+$amount WHERE SSN='$ssn_receiver';";
( $a = mysql_query( $sql_add_money )) or die (mysql_error());

//print $send_ssn;
//Subtract that money from the Balance of the sender
$sql_sub_money = "UPDATE USER_ACCOUNT SET Balance = Balance-$amount WHERE SSN='$send_ssn';";
( $b = mysql_query( $sql_sub_money )) or die (mysql_error());

//Get current datetime
$curr_date = date("Y/m/d h:i:sa");

//print $curr_date;

//Update record of transaction in the SEND_TRANSACTION table
$sql_insert_transact = "INSERT INTO SEND_TRANSACTION (STid, Amount, Datetime, Memo, Cancelled, SSN, Identifier) VALUES ('$transact_id',$amount,'$curr_date','$memo',0,'$send_ssn','$ident');";

( $t = mysql_query( $sql_insert_transact )) or die (mysql_error());

header('Location: transaction.html');
exit;
?>
