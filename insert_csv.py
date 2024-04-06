import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class CSVInserter:
    def __init__(self, engine, file_path):
        self.engine = engine
        self.file_path = file_path

    # insert initial retail csv dataset
    def insert_initial_data(self):
        # read retail csv dataset
        data = pd.read_csv(self.file_path, nrows=200) 

        # change csv columns so it matches table columns
        data = data.rename(columns={
            'Product Category' : 'ProductCategory',
            'Quantity' : 'ProductQuantity',
            'Price per Unit': 'PricePerUnit',
        })

        # split csv dataset into matching columns for tables
        customers_data = data[['Gender', 'Age']]
        products_data = data[['ProductCategory', 'PricePerUnit', 'ProductQuantity']]

        # insert into tables
        try:
            with self.engine.begin() as connection:
                customers_data.to_sql('customers', con=connection, if_exists='append', index=False)
                products_data.to_sql('products', con=connection, if_exists='append', index=False)
        except Exception as e:
            print(f"Error inserting initial CSV data: {e}")

    # insert csv data into SalesTransaction with foreign key to Products
    def insert_sales_transaction(self):
        data = pd.read_csv(self.file_path, nrows=200)

        # change csv columns so it matches table columns
        data = data.rename(columns={
            'Date': 'TransactionDate',
            'Total Amount' : 'TotalAmount',
        })

        sales_transactions_data = data[['TransactionDate', 'TotalAmount']]

        # insert into SalesTransaction table with foreign keys
        with self.engine.connect() as connection:
            # fetch all ProductIDs in advance
            product_ids = [row[0] for row in connection.execute(text("SELECT ProductID FROM Products")).fetchall()]
            table_index = 0

            # fetch all CustomerIDs in advance
            customer_ids = [row[0] for row in connection.execute(text("SELECT CustomerID FROM Customers")).fetchall()]

            for index, row in sales_transactions_data.iterrows():
                # get product id
                product_id = product_ids[table_index]

                # get customer matching transaction
                customer_id = customer_ids[table_index]
                table_index += 1

                # get random employee for transaction
                employee_result = connection.execute(text("SELECT EmployeeID FROM Employees ORDER BY RAND() LIMIT 1"))
                employee_id = employee_result.scalar()

                # insert into SalesTransaction
                query = text("""
                    INSERT INTO SalesTransaction (ProductID, CustomerID, EmployeeID, TransactionDate, TotalAmount)
                    VALUES (:product_id, :customer_id, :employee_id, :transaction_date, :total_amount)
                """)
                try:
                    connection.execute(query, {
                        'product_id': product_id,
                        'customer_id': customer_id,
                        'employee_id': employee_id,
                        'transaction_date': row['TransactionDate'],
                        'total_amount': row['TotalAmount']
                    })
                except SQLAlchemyError as e:
                    print(f"Error inserting sales transaction data: {e}")
            connection.commit()       