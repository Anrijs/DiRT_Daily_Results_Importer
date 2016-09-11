<html>
<body>
<h1>DiRT Rally Cross-Platform Daily Results by <a href="https://reddit.com/u/Th3HolyMoose">/u/Th3HolyMoose</a></h1>
<br><br>
<h3>Results are imported hourly on the 50th minute to import the last entries just before the event ends.</h3>
<a href="https://github.com/Th3HolyMoose/DiRT_Daily_Results_Importer">Source Code</a>
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
