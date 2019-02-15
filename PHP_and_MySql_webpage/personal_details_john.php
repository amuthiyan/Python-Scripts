<?php
include("db_details.php");

$error_message = "Several fields that are required are missing: ";

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


//Initialize bank account if not there
$insert_bank = "INSERT INTO BANK_ACCOUNT (BankID, BANumber) VALUES('$bank_id','$bank_number');";
( $b = mysql_query( $insert_bank ));


$insert_sql = "INSERT INTO USER_ACCOUNT (SSN, Name, Balance , BankID, BANumber) VALUES ($ssn,'$user_name', 0 ,'$bank_id',$bank_number);";
( $t = mysql_query( $insert_sql )) or die (mysql_error());

//Insert Email
if(isset($_GET["email"]) && !empty($_GET["email"])){
	if(checkEmail($email_id) == TRUE){
      $insert_email = "INSERT INTO ELECTRONIC_ADDRESS (Identifier, SSN, Type) VALUES ('$email_id', $ssn, 'email');";
      ( $e = mysql_query( $insert_email )) or die (mysql_error());
	}
	else{
		print "Email address not in correct format, please enter a valid email address";
	}
}
else{
  $error_message = $error_message + " email,";
}

//Insert Phone Number
if(isset($_GET["phone"]) && !empty($_GET["phone"])){
  if(checkPhone($phone) == TRUE){
    $insert_phone = "INSERT INTO ELECTRONIC_ADDRESS (Identifier, SSN, Type) VALUES ('$phone_number', $ssn, 'phone');";
    ( $p = mysql_query( $insert_phone )) or die (mysql_error());
  }
  else{
	  print "Phone number not in correct format. Please enter a valid phone number";  
  }
}
else{
  $error_message = $error_message + " phone number,";
}


function checkPhone($phone){
	  $value = $phone;
	  $value = trim($value);
	  $first = substr($value,0,2);
	  $second = substr($value,4,6);
	  $third = substr($value,8,12);
	  if(strlen($value) != 12){
		if(is_numeric($first) && is_numeric($second) && is_numeric($third)){
			if((substr($value,-5,1) == '-') && (substr($value,-9,1) == '-')){
               return TRUE;
			}		
            else{
              return FALSE;
			}			
		}
        else{
			return FALSE;
		}
	  }
	  else{
		  return FALSE;
	  }
  }
 
  function checkEmail($email){
	  $value = $email;
	  $value = $trim($value);
	  $email_len = strlen($value);
	  if($email_len >= 7){
		 $atSymb = chr("&#64");
	     $atPos = strpos($value, $atSymb);
	     $startPref = substr($value,$atPos+1,$email_len-1);
	     $dotPos = strpos($startPref, $dotSymb);
	     $dotSymb = chr("&#46");
	     if(($atPos != FALSE) && ($dotPos != FALSE)){
		   return TRUE;
		 }
		 else{
			return FALSE;
		 }
	  }
	  else{
		  return FALSE;
	  }  	  
  }
  
  function checkBankInfo($bankNum){	  
    $bankN = $trim($bankNum);  
	return $bankN;
  }
  
?>
