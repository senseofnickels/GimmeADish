<?php
	require 'database.php';
	$city = $_GET['city'];
	
	$con = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
	if (!$con) {
		die("Error connecting: " . mysqli_error($con));
	}
	
	$sql = "SELECT DISTINCT c.category FROM cats c, rests b WHERE c.bus_id = b.bus_id AND b.location = '" . $city . "'";
	$result = mysqli_query($con, $sql);
	
	echo '<img src="category.png"><b> 2. </b> Select your genre of deliciousness: ';
    
	echo '<select name="selectcategory" id="selectcategory" onchange="showReviews()" style="background-color:#464646; color:#EEEEEE; -moz-border-radius: 5px; padding:5px">';
	echo '<option value="">Select a category...</option>';
	while($row = mysqli_fetch_array($result)) {
		echo '<option value="' . $row['category'] . '">' . $row['category'] . '</option>';
	}
	
	echo '</select>';
	
	mysqli_close($con);
?>