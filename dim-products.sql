SELECT 
	ProductID,
	ProductName,
	Price,
	-- Category

	CASE
		WHEN Price < 50 THEN 'Low'
		WHEN Price BETWEEN 50 AND 200 THEN 'Medium'
		WHEN Price > 200 THEN 'High'
	END AS PriceCategory

From dbo.products;

