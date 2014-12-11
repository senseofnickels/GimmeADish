<!doctype html>
<html>
<head>
<script>
	function showCategories() {
		divopen = '<div style="position:relative; top:20px; padding:5px; background-color:#FFF8F8">';
		divclose = '</div>';
		loading = '<img src="loading.gif">';
		document.getElementById("reviews").innerHTML = '';
		city = document.getElementById("selectcity").value;
		if (city == "") {
			document.getElementById("category").innerHTML = '';
			return;
		} else {
			document.getElementById("category").innerHTML = divopen+loading+divclose;
			xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange = function() {
				if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					document.getElementById("category").innerHTML = divopen + xmlhttp.responseText + divclose;
				}
			}
			xmlhttp.open("GET","getcategories.php?city="+city,true);
			xmlhttp.send();
		}
	}
	
	function showReviews() {
		divopen = '<div style="position:relative;margin:5px;padding:5px">';
		divclose = '</div>';
		loading = '<img style="margin-top:20px;margin-left:50%;margin-right:50%" src="loading.gif">';
	
		city = document.getElementById("selectcity").value;
		category = document.getElementById("selectcategory").value;
		
		if (city == "" || category == "") {
			document.getElementById("reviews").innerHTML = '';
			return;
		} else {
			document.getElementById("reviews").innerHTML = divopen + loading + divclose;
			xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange = function() {
				if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					document.getElementById("reviews").innerHTML = divopen + xmlhttp.responseText + divclose;
				}
			}
			xmlhttp.open("GET","getreviews.php?city="+city+"&category="+category,true);
			xmlhttp.send();
		}
	}
</script>
</head>
    
<body bgcolor="#600000">

<img style="width:100%; max-width:1000px; max-height:322px; display:block; margin-left:auto; margin-right:auto" src="banner.png">
<div style="background-color: #FFC0C0; font-family:calibri; position: relative; top:20px; padding:10px; max-width:1000px; display:block; margin-left:auto; margin-right:auto">
    
	<div>
		<p style="color:#FFFFFF;display:block;background-color:#600000; border-radius:20px; text-align:center; padding:5px; margin-left:auto; margin-right:auto">Are you ready to see what delicious dishes people are <i>craving</i> for? Go ahead and take a look.</p>
    </div>
	<div id="city" style="padding:5px; background-color:#FFF8F8">
        <?php require 'getcities.php'; ?>
    </div>

    
    <div id="category"></div>

    <div id="reviews"></div>
		
		<!--
		<div style="background-color:#FFF8F8;border-style:solid; border-color:#464646; border-width:2px; border-radius:15px; padding:10px; margin-bottom:10px">
            <b>Restaurant:</b> <a href="#"> restaurant-result-1</a> (hyperlink to yelp page) <br>
            <b>Dish:</b> its-delish-dish <br>
            People are talking about this dish favorably <b>xx%</b> of the time! <br>
            They mostly describe it as: <b>descriptor-1</b> and <b>descriptor-2</b> <br>
            Check out what they have to say... <br>
            <i>"...review-excerpt-1..."</i> <br>
            <i>"...review-excerpt-2..."</i>
        </div>
        <div style="background-color:#FFF8F8;border-style:solid; border-color:#464646; border-width:2px; border-radius:15px; padding:10px; margin-bottom:10px">
            <p style="font-size:20px; margin:2px"><b>Restaurant:</b> <a style="text-decoration:none" href="http://www.yelp.com/biz/roam-artisan-burgers-san-francisco-3"> Roam Artisan Burgers</a></p>
            <p style="margin:2px"><b>Dish:</b> Bison "Heritage" Burger</p>
            <p style="margin:2px">People are talking about this dish favorably <b>97%</b> of the time!</p>
            <p style="margin:2px">They mostly describe it as: <b>juicy</b> and <b>eclectic</b></p>
            <p style="margin:10px">Check out what they have to say... <br></p>
            <p style="margin:2px;text-align:center"><i>"...I could not get over how juicy this burger was without feeling like it was sloppy...."</i> <br>
            <i>"...I love their choice of cheeses and eclectic toppings...."</i></p>
        </div>
        -->
    

    
    <h1>
        <br>
        <br>
    </h1>
</div>
</body>
</html>