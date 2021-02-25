SELECT COUNT(DISTINCT I.sellerID)
FROM Items I, Bids B
WHERE I.sellerID = B.bidderID;
