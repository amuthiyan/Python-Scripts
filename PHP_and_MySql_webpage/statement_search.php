<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);


$date1 = $_GET["date1"];
$date2 = $_GET["date2"];
$send_ssn = $_GET["send_ssn"];
$ident = $_GET["ident"];

if(empty($date2))
{
  $date2 = date("Y/m/d h:i:sa");
}


//Get some of transactions for the two dates
$sum_sql = "SELECT SUM(Amount) AS Trans_Sum FROM SEND_TRANSACTION WHERE Identifier='$ident' AND SSN='$send_ssn' AND Datetime BETWEEN '$date1' AND '$date2';";
$row = mysql_fetch_assoc(mysql_query($sum_sql)); 
$sum = $row['Trans_Sum'];


//$curr_date = date("Y/m/d h:i:sa");

$s = "SELECT * FROM SEND_TRANSACTION WHERE Identifier='$ident' AND SSN='$send_ssn' AND Datetime BETWEEN '$date1' AND '$date2';";

( $t = mysql_query( $s )) or die (mysql_error());
if(mysql_num_rows($t) == 0) die ("no data");


$out = "";

//add styles to the table
$out .= "<style> table, th, caption{margin:auto; border : 2px solid black;} </style>";
$out .= "<style> caption {color:blue} </style>";
$out .= "<style> td {color:blue;}</style>";
$out .= "<style>th{background : #aaaaaa ;}</style>";


//add headers and caption to the table
$out .= "<table border=2>";

$out .= "<caption>Transactions Since: " . $date1 . " Until: ". $date2 . "</caption>";

$out .= "<tr>";
	$out .= "<th> STid </th> <th> Amount </th> <th> Datetime </th> <th> Memo </th> <th> Cancelled</th> <th> Phone/Email </th>";
	$out .= "</tr>";

//populate the table with data
while( $r = mysql_fetch_array($t))
{
	$STid   =htmlspecialchars($r["STid"]);
	$amount  =htmlspecialchars($r["Amount"]);
	$datetime = htmlspecialchars($r["Datetime"]);
	$memo = htmlspecialchars($r["Memo"]);
	$cancellled = htmlspecialchars($r["Cancelled"]);
	$identifier = htmlspecialchars($r["Identifier"]);


	$out .= "<tr>";
	$out .= "<td> $STid </td> <td> $amount </td> <td> $datetime </td> <td> $memo </td> <td> $cancellled </td> <td> $identifier </td> ";
	$out .= "</tr>";
}

$out .= "</table>";

print $out;
print "<br><br>";
print "The Total Amount transacted sent to ". $ident . "between " . $date1 . " and " . $date2 . " was: $" . $sum;



?>