<?php
	require 'database.php';
	$city = $_GET['city'];
	$category = $_GET['category'];
	
	$con = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
	if (!$con) {
		die("Error connecting: " . mysqli_error($con));
	}
	
	$sql = 'SELECT b.name, b.location, r.dish_text, r.dish_freq, r.dish_reviews, r.token_results FROM reviews r, rests b, cats c WHERE b.bus_id = r.bus_id AND r.bus_id = c.bus_id AND b.location = "' . $city . '" AND c.category = "' . $category . '" ORDER BY r.dish_freq DESC LIMIT 10';
	$result = mysqli_query($con, $sql);
	if ($result->{'num_rows'} > 0) {
		echo '<h1 style="color:#464646; text-align:center"><i>Delicious dishes await...</i></h1>';
	}
	else {
		echo '<h1 style="color:#464646; text-align:center"><i>There wasn\'t enough data to <br>determine what dishes people are talking about :(</i></h1>';
	}
	while($row = mysqli_fetch_array($result)) {
		echo "<div ";
		echo "style='position:relative;background-color:#FFF8F8;border-style:solid; border-color:#464646; border-width:2px; border-radius:15px; padding:10px; margin-bottom:10px'>";
		echo "<div style='text-align:center;font:small-caps 25px georgia'><b>Dish:</b> <u>" . $row['dish_text'] . "</u><hr/></div>";
		echo "<b>Restaurant:</b> " . $row['name'] . "<br>";
		echo "<b>City:</b> " . $row['location'] . "<br>";
		
		echo "<i>This dish was mentioned " . $row['dish_freq'] . " times </i><br>";
		echo "Here's what people are saying about it...<br>\"" . $row['dish_reviews'] . "\"<br>";
		echo "<div style='padding:5px;width:50%;position:relative;top:0px;right:0px;background-color:#464646;color:#FFFFFF'><i><p style='background-color:#383838;padding:2px;margin-bottom:0px;margin-bottom:0px;margin:0px'>Token statistics:</p></i>" . $row['token_results'] . "</div>";
		echo "</div>";
	}
	mysqli_close($con);
?>