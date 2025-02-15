SELECT
	ReviewID,
	CustomerID,
	ProductID,
	ReviewDate,
	Rating,
	CASE
		WHEN Rating < 3 THEN 'Bad'
		WHEN Rating = 3 THEN 'Satisfactory'
		WHEN Rating > 3 THEN 'Good'
		END AS RatingLevel,
	REPLACE(ReviewText, '  ', ' ') AS ReviewText

FROM customer_reviews

