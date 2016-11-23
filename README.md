# DiRT Rally Cross-Platform Results


## About
This tool downloads DiRT Rally online event results for all platforms (Steam, PS4, Xbox, Oculus) and saves them in one file. It is originally created by [/u/Th3HolyMoose](https://reddit.com/u/Th3HolyMoose).

## Usage
Using this tool is very easy - just run one command and it will generate all result files.
To run this tool, simply type `python daily.py` for last daily events or `python weekly.py` for weekly events.

### On this fork
Use run.py for more flexible results. Type `python run.py <event-type>` to get choosen events. Event type can be *daily1*, *daily2*, *weekly1*, *weekly2* and *monthly*

Additional optional parameter is *nohtml*. This will only import data to txt files without making HTML page.

### Usage exaples
`python run.py daily1` - import only last daily1 event

`python run.py daily1 daily2` - import last daily1 and daily2 events

`python run.py weekly1 nohtml` - import only last weekly1 event and do not generate HTML page

## SQL
My goal for this fork was SQL support for was making result datasets I could use for making personalised result pages.
For this I have added *importSql.py*

To use *importSql.py* follow theese steps:
1. Install mysql server and python-mysqldb driver
2. Make database and run SQL script from *database.sql* file
3. Rename or copy *config.example.py* to *config.py*
4. Configure database settings in *config.py*
5. Custimize sql filter function (function `filt(item)`) in *importSql.py*. At the moment it will only save all drivers from Latvia (filtered by flag).
6. Run `python importSql.py date folder` or add *sql* parameter to run.py

## u/Th3HolyMoose
To see original version in work, go to http://holymooses.com/DiRT/

## Future plans?
Yes.
