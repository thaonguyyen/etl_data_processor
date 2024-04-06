# ETL-Data-Processor
## Database
I utilized MySQL as the database to store my tables. I made this database using the root account and password. 

create database sales;

use sales;

I created and used the database called 'sales' with the code above and then I executed my 'create_tables.sql' code to create the tables in 'sales'
After inserting the data into the tables, I executed 'queries.sql' to author one or more SQL queries (SELECT statements) to demonstrate proper functionality.

## Inserting CSV
In order to insert my csv file called 'retail_sales_dataset.csv' that I downloaded from Kaggle, I created a separate class called 'CSVInserter' in the  'insert_csv.py' file. I first inserted the initial data for the Customers and Products tables that were found right in the dataset csv. After this initial insert, I inserted in my SalesTransaction table using foreign keys referencing Customers and Employees and other transaction data from the dataset. I made sure that the data across these tables were consistent to the original csv file. 

## Inserting API
In order to insert from an API call, I created a separate class called 'APIInserter' in the 'insert_api.py' file. I utilized the Name api from Randommer.io to generate random first and last names for Customers and Employees. I also fetched random dates from the Random Date Generator API created by Library Research Service to use as StockDate in the Inventory table. I then inserted the data fetched from these APIs into the appropriate tables.

## Inserting into Tables
In order to run the methods created by CSVInserter and APIInserter, I compiled all the methods concisely into 'main.py'. By running this file, the table will now be completely filled with the data accumulated by a csv file and API calls.


