SELECT
	c.CustomerID,
	c.CustomerName,
	c.Email,
	c.Gender,
	c.Age,
	CASE
		WHEN c.Age < 25 THEN 'Young Adults'
		WHEN c.Age BETWEEN 25 AND 45 THEN 'Middle Age'
		WHEN c.Age > 45 THEN 'Older People'
	END AS AgeGroup,
	g.Country,
	g.City
		
FROM 
	dbo.customers as c
LEFT JOIN
	dbo.geography g

ON
	c.GeographyID = g.GeographyID;
	
