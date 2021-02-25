SELECT COUNT(DISTINCT u.userID)
FROM Users u, Items i
WHERE u.rating > 1000 AND u.userID = i.sellerID;
