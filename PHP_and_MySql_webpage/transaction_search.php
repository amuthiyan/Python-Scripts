<?php
include("db_details.php");

//connect to database
($dbh = mysql_connect ($hostname,$username,$password))
		or die("Unable to connect to MySQL database");
print "Successfully connected to MySQL.<br><br>";
mysql_select_db($project);

$trans_id = $_GET["trans_id"];

$trans_sql = "SELECT * FROM SEND_TRANSACTION WHERE STid = '$trans_id';";

( $t = mysql_query( $trans_sql )) or die (mysql_error());

if(mysql_num_rows($t) == 0) die ("no data");


$out = "";

//add styles to the table
$out .= "<style> table, th, caption{margin:auto; border : 2px solid black;} </style>";
$out .= "<style> caption {color:blue} </style>";
$out .= "<style> td {color:blue;}</style>";
$out .= "<style>th{background : #aaaaaa ;}</style>";


//add headers and caption to the table
$out .= "<table border=2>";

$out .= "<caption>Transactions ID: " . $trans_id . "</caption>";

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
?>
