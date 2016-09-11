<html>
<body>
<h1>DiRT Rally Results by /u/Th3HolyMoose</h1>
<br><br>
<h3>Results are imported hourly on the 55th minute to import the last entries just before the event ends.</h3>
<br><br><br>
<?php
   $dirs = scandir("results/");
   for($i = 0; $i < count($dirs); $i++) {
		    if($dirs[$i] == "template.html" || is_dir("results/" . $dirs[$i])) {
		    continue;
		    }
		    echo "<a href='results/" . $dirs[$i] . "'>" . $dirs[$i] . "</a><br>";		    
   }
   
   
   
?>



</body>
</html>
