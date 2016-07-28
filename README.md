# ABOUT
This is a command line checkbook program. It currently only works with python3.
To start the program, type the following at the command line

## Usage
```
python3 main.py
```

##### NOTE

```sqlite3``` is needed to use the database functionality
```ElementTree``` is needed to use the xml functionality

## Commands

* **print**  : prints the checkbook
* **add**    : add a transaction
* **edit**   : edit a transaction
* **save**   : save the checkbook
* **load**   : load a checkbook
* **report** : generate a report for the checkbook

### Commands that can take arguments
* **print**  : ```print [<key> <value> | help]```
* **edit**   : ```edit [number]```
* **load**   : ```load [file name]```

## Configuration
In the *config.py* file, you can set some configuration options

* ```DATE_FORMAT``` : The format for date input *default = M/D/YYYY*
* ```THOSUAND_SEP``` :  If numbers have the thousands separator *default = True*
* ```LOCALE``` : The locale to use for number formatting *default = LC_ALL*
* ```FILE_NAME``` : the default file to load *default = myXML.xml*
* ```DEBIT_CATEGORIES``` & ```CREDIT_CATEGORIES``` : set the categories to choose from
* ```USE_SQL``` : use a sqlite database over xml *default = False*
* ```DB_NAME``` : the sqlite database file name *default = checkbook.db*

## Converter
```converter.py``` can be used to convert from a sqlite database to an xml file and vice versa.

### Usage
```
python3 converter.py
```