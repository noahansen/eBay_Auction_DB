WITH table1 AS(
	SELECT C.itemID as itemID, COUNT(C.itemID) AS count 
	FROM Categories C 
	GROUP BY itemID
)
SELECT COUNT(T.itemID)
FROM table1 T
WHERE T.count = 4;
