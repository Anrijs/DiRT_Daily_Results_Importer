<html>
  <head>
    <title>DiRT Cross Platform Results</title>
  </head>
  
<body>
<h1>DiRT Rally Cross-Platform Results by <a href="https://reddit.com/u/Th3HolyMoose">/u/Th3HolyMoose</a></h1>
<br><br>
<h3>Results are imported hourly on the 50th minute to import the last entries just before the event ends.</h3>
<a href="https://github.com/Th3HolyMoose/DiRT_Daily_Results_Importer">Source Code</a>

<p>
  Both Daily's and both Weekly's are now imported. Daily's are imported everyone hour, and weekly's only once 10 minutes after the end of the event has finished.
</p>
<p>Mobile Users Note: The result pages will take a second to load on a phone, the webbrowser might freeze for a few seconds. Just let it do it's thing and it should run smoothly afterwards!</p>
<br>
<h2>Imported Dailies</h2>

<?php
   function endsWith($haystack, $needle) {
   // search forward starting from end minus needle length characters
   return $needle === "" || (($temp = strlen($haystack) - strlen($needle)) >= 0 && strpos($haystack, $needle, $temp) !== false);
}
   function scanResults($dir) {
   $dirs = scandir("results/" . $dir);
   for($i = 0; $i < count($dirs); $i++) {
		    if($dirs[$i] == "template.html" || is_dir("results/" . $dir . "/" . $dirs[$i]) || !endsWith($dirs[$i], ".html")) {
		    continue;
		    }
		    echo "<a href='results/" . $dir . "/" . $dirs[$i] . "'>" . $dirs[$i] . "</a><br>";		    
		    }
		    }
   
   scanResults("daily");
   
?>

<br>
<h2>Imported Daily 2's</h2>
<?php
scanResults("daily2");
   ?>
<br>

<h2>Imported Weekly</h2>
<?php
scanResults("weekly1");
   ?>
<br>

<h2>Imported Weekly 2</h2>
<?php
scanResults("weekly2");
   ?>
<br>


</body>
</html>
