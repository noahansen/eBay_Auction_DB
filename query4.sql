WITH table1 AS(
	SELECT MAX(i.currently) AS max
	FROM Items i
)
SELECT i.itemID
FROM Items i, table1 T
WHERE i.currently = T.max;
