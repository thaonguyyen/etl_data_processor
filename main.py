from sqlalchemy import create_engine
from insert_csv import CSVInserter  
from insert_api import APIInserter  

db_connection_string = 'mysql+pymysql://root:4Thaopa$$word@localhost/sales'
csv_file_path = r'C:\Users\thaon\Downloads\SEMESTER 6\DS 2002\ETL Data Processor\retail_sales_dataset.csv'
engine = create_engine(db_connection_string)
raw_connection = engine.raw_connection()

csv_inserter = CSVInserter(engine, csv_file_path)
api_inserter = APIInserter(engine, raw_connection)

csv_inserter.insert_initial_data()
print("Inserted initial CSV data sucessfully!")
api_inserter.insert_customer()
print("Inserted customer data sucessfully!")
api_inserter.insert_employee()
print("Inserted employee data sucessfully!")
csv_inserter.insert_sales_transaction()
print("Inserted sales transaction data sucessfully!")
api_inserter.insert_inventory()
print("Inserted inventory data sucessfully!")