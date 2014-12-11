<?php
	require 'database.php';
	
	$con = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
	if (!$con) {
		echo '<h1>It seems we had a problem<br>connecting to the database... :/</h1>';
		die("Error connecting: " . mysqli_error($con));
	}
	else {
		$sql = "SELECT DISTINCT location FROM rests";
		$result = mysqli_query($con, $sql);
		
		echo '<img src="city.png"><b> 1. </b> Select your city: ';
		
		echo '<select id="selectcity" style="background-color:#464646; color:#EEEEEE; -moz-border-radius: 5px; padding:5px" onchange="showCategories()">';
		echo '<option value="">Select a city...</option>';
		while($row = mysqli_fetch_array($result)) {
			echo '<option value="' . $row['location'] .'">' . $row['location'] . "</option>";
		}
		
		echo '</select>';
		
		mysqli_close($con);
	}
?>