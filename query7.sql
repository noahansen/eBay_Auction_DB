SELECT COUNT(DISTINCT C.Category)
FROM Categories C, Items I
WHERE C.itemID = I.itemID AND I.currently>100.00 AND I.numberOfBids >0;
