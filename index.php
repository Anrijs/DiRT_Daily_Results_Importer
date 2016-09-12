<html>
  <head>
    <title>DiRT Daily Cross Platform Results</title>
  </head>
  
<body>
<h1>DiRT Rally Cross-Platform Daily Results by <a href="https://reddit.com/u/Th3HolyMoose">/u/Th3HolyMoose</a></h1>
<br><br>
<h3>Results are imported hourly on the 50th minute to import the last entries just before the event ends.</h3>
<a href="https://github.com/Th3HolyMoose/DiRT_Daily_Results_Importer">Source Code</a>

<p>
  For now only dailies are imported (because of their simplicity). Plan for future is to add support for wager/delta, weekly's and monthly's, hopefully with added individual stage times and driver profiles.
</p>
<p>Mobile Users Note: The result pages will take a second to load on a phone, the webbrowser might freeze for a few seconds. Just let it do it's thing and it should run smoothly afterwards!</p>
<br>
<h2>Imported Dailies</h2>

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
