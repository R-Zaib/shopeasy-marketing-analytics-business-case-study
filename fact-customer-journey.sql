-- Common Table Expression (CTE)
-- The WITH clause is used to define the DuplicateRecords CTE. 
-- A CTE is a temporary result set that you can reference within a SELECT, INSERT, UPDATE, or DELETE statement. 
-- The DuplicateRecords CTE will be available only for the duration of the query that follows it.

WITH DuplicateRecords AS (
	SELECT
		JourneyID,
		CustomerID,
		ProductID,
		Stage,
		Action,
		Duration,
		ROW_NUMBER() OVER(
			PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action
			ORDER BY JourneyID
		) AS row_num

	FROM
		dbo.customer_journey
)


-- Select all records from the CTE where row number > 1, indicating duplicate entries.
SELECT *
FROM DuplicateRecords
WHERE row_num > 1
ORDER BY JourneyID


-- Outer query select the final cleaned and standardized data

SELECT
	JourneyID,
	CustomerID,
	ProductID,
	VisitDate,
	Stage,		-- this will use uppercased stage from subquery for consistency
	Action,
	COALESCE(Duration, CASE WHEN avg_duration is NULL THEN 0 ELSE avg_duration END) AS Duration

FROM
	(
		-- subquery to process and clean the data
		SELECT
			JourneyID,
			CustomerID,
			ProductID,
			VisitDate,
			UPPER(Stage) AS Stage,
			Action,
			Duration,
			AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration,
			ROW_NUMBER() OVER(
				PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action
				ORDER BY JourneyID
			) AS row_num

		FROM
			dbo.customer_journey
	) AS subquery
WHERE
	row_num = 1;
