-- SELECT data from at least 3 tables
SELECT * FROM SalesTransaction;
SELECT * FROM Customers WHERE Gender = 'Female';
SELECT * FROM Products WHERE ProductCategory = 'Beauty';

-- Perform some type of aggregation
SELECT Products.ProductCategory, SUM(SalesTransaction.TotalAmount) AS TotalSalesAmount
FROM SalesTransaction
JOIN Products ON SalesTransaction.ProductID = Products.ProductID
GROUP BY Products.ProductCategory;