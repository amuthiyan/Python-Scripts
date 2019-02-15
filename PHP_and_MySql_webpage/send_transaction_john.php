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

$limit_one = 0;
$limit_week = 0;
$final_amount = 0;
$amount_input = 0;
$start_week = 0;
$end_week = 0;

$verif_mail = "SELECT Verified FROM ELECTRONIC_ADDRESS WHERE Identifier='$ident';";
$verified_rows = mysql_fetch_assoc(mysql_query($verif_mail)); //add this for the true/false value you get for email verification
$verified = $verified_rows["Verified"];

checkBalance($verified);

//print "$limit_one <br>";
//print "$limit_week <br>";

$curr_date = date("Y/m/d h:i:sa");
$curr_day = date("N");

//print "curr_day: $curr_day <br>";

for($i = 0; $i < 7; $i++){
  if($curr_day == $i+1){
		 $start_week = date("Y/m/d h:i:sa", mktime(0, 0, 0, date("m")  , date("d") - $i , date("Y")));
	     $end_week = date("Y/m/d h:i:sa", mktime(0, 0, 0, date("m")  , ((6-$i) + date("d")), date("Y")));
	}
 }
 
 $all_between = "SELECT SUM(Amount) AS Trans_Sum FROM SEND_TRANSACTION WHERE Datetime BETWEEN '$start_week' AND '$end_week';";
 //print "all between: $all_between <br>";
 $rows = mysql_fetch_assoc(mysql_query($all_between));
 //print "rows: $rows <br>";
 $final_amount = $rows["Trans_Sum"]; 	

//print "$curr_date <br>";
//print "$curr_day <br>";
//print "final amount: $final_amount <br>";

//Get the ssn of the person being sent money
$ssn_check = "SELECT(SSN) FROM ELECTRONIC_ADDRESS WHERE Identifier = '$ident';";
($ssn_temp = mysql_fetch_assoc(mysql_query( $ssn_check ))) or die (mysql_error());

$ssn_receiver = $ssn_temp["SSN"];
//print $ssn_receiver;

$total = $amount + $final_amount;

if($total > $limit_week){
  	print "You have exceeded the limit for a single transaction";
}
else{
	
	if($amount > $limit_one){
		print "The amount you have entered has gone over the maximum limit for transactions in a week. Please enter another value.";
	}
	else{
		//Add sent money to the balance of receiving user
       $sql_add_money = "UPDATE USER_ACCOUNT SET Balance = Balance+$amount WHERE SSN='$ssn_receiver';";
       ( $a = mysql_query( $sql_add_money )) or die (mysql_error());
	
	   //print $send_ssn;
       //Subtract that money from the Balance of the sender
       $sql_sub_money = "UPDATE USER_ACCOUNT SET Balance = Balance-$amount WHERE SSN='$send_ssn';";
       ( $b = mysql_query( $sql_sub_money )) or die (mysql_error());
	   
		
		//Update record of transaction in the SEND_TRANSACTION table
        $sql_insert_transact = "INSERT INTO SEND_TRANSACTION (STid, Amount, Datetime, Memo, Cancelled, SSN, Identifier) VALUES ('$transact_id',$amount,'$curr_date','$memo',0,'$send_ssn','$ident');";

        ( $t = mysql_query( $sql_insert_transact )) or die (mysql_error());
	}
}

//header('Location: transaction.html');
//exit;

function checkBalance($verif){
	  global $limit_one, $limit_week; 
	
	  if($verif == 1){
	    $limit_one = 999.99;
	    $limit_week = 19999.99;
	  }
	  else{
		$limit_one = 499.99;
	    $limit_week = 9999.99;	
	  }
  }

?>
