# What will this code sample implement?
The code sample implements the following operation:

1. Python: Download a timeseries of daily deaths per country using the data from https://github.com/CSSEGISandData/COVID-19

2. Python: Convert the table so that each country and each day is a separate row 

3. Python: Provide code to upload the table from step 3 into an SQL table named deaths_total

4. Python: From the data in step 2, calculate the daily change in deaths for each country

5. Python: Provide code to upload the table from step 4 into an SQL table named deaths_change_python

6. SQL: Provide SQL code to calculate the daily change for each country using only the data from deaths_total and save it into an SQL table named deaths_change_sql

# How to run the code
<strong>Note:</strong> The database used in this sample code is MySQL.

1. The first file (.py) will conduct step1 to step 6. Before running the python file, change the values of these variables in your system: user, password, host and database. For example:
- user = 'root'
- password = 'yourdbpassword'
- host = 'localhost'
- database = 'covid19'

When the application finished, two tables with loaded data will appear in your database including deaths_total and deaths_change_python

2. Open the SQL file in MySQL Workbench, right click on the working schema and select "Set as Default Schema". Then run the script. When it finished, a table named deaths_change_sql will be created
