import requests
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class APIInserter:
    def __init__(self, engine, raw_connection):
        self.engine = engine
        self.raw_connection = raw_connection
    
    # make API call to generate random first and last names
    def fetch_names(self, quantity):
        key = 'b809c0e8efb24b188885e63682863b4f'
        url = 'https://randommer.io/api/Name'
        response = requests.get(
            url,
            headers={"X-Api-Key": key, "Content-Type": "application/json"},
            params={"nameType": "fullname", "quantity": quantity}
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch names: {response.status_code}, {response.text}")
            return []

    # make API call to generate random dates
    def fetch_dates(self, year, num_dates):
        api_url = 'https://api.lrs.org/random-date-generator'
        params = {
            'year': year,
            'num_dates': num_dates
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            dates = [details['db'] for key, details in data['data'].items()]
            return dates
        else:
            print(f"Failed to fetch random dates: {response.status_code}, {response.text}")
            return []

    # insert customer names into Customer table
    def insert_customer(self):
        try:
            names = self.fetch_names(200)
            with self.engine.connect() as connection:
                cursor = self.raw_connection.cursor()
                for full_name in names:
                    name = full_name.split(' ')
                    first_name = name[0]
                    last_name = name[1]
                    query = f"""
                        UPDATE Customers
                        SET FirstName = %s, LastName = %s
                        WHERE FirstName IS NULL OR LastName IS NULL
                        LIMIT 1;
                    """
                    cursor.execute(query, (first_name, last_name))
        except:
            print(f"An error occurred inserting customer")
            self.raw_connection.rollback()
        finally:      
            self.raw_connection.commit()
            cursor.close()

    # insert employee names into Employees table
    def insert_employee(self):
        try:
            names = self.fetch_names(200)
            with self.engine.connect() as connection:
                cursor = self.raw_connection.cursor()
                for full_name in names:
                    name = full_name.split(' ')
                    first_name = name[0]
                    last_name = name[1]
                    query = f"""
                        INSERT INTO Employees (FirstName, LastName) 
                        VALUES (%s, %s)
                    """
                    cursor.execute(query, (first_name, last_name))
        except:
            print(f"An error occurred inserting employee")
            self.raw_connection.rollback()
        finally:      
            self.raw_connection.commit()
            cursor.close()

    # insert date into Inventory table
    def insert_inventory(self):
        dates = self.fetch_dates(2023, 200)

        with self.engine.begin() as connection:
            for date in dates:
                product_id_result = connection.execute(text("SELECT ProductID FROM Products ORDER BY RAND() LIMIT 1"))
                product_id = product_id_result.scalar()
                insert_query = text("INSERT INTO Inventory (ProductID, StockDate) VALUES (:product_id, :stock_date)")
                try:
                    connection.execute(insert_query, {'product_id': product_id, 'stock_date': date})
                except SQLAlchemyError as e:
                    print(f"Error inserting inventory data: {e}")
