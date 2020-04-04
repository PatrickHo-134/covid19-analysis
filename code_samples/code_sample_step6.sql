CREATE table deaths_change_sql AS 
SELECT r1.CountryRegion,
r2.CalDate,
(r2.Total - r1.Total) AS DailyChange
FROM deaths_total r1 LEFT JOIN deaths_total r2
ON datediff(r2.CalDate, r1.CalDate) = 1
WHERE r1.CountryRegion = r2.CountryRegion
ORDER BY
r1.CountryRegion, r1.CalDate
;

ALTER TABLE deaths_change_sql
ADD CONSTRAINT PK_deaths_change PRIMARY KEY (CountryRegion, CalDate);

SELECT * FROM deaths_change_sql
WHERE CountryRegion LIKE 'Australia';