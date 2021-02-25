drop table if exists Items;
drop table if exists Bids;
drop table if exists Categories;
drop table if exists Users;

create table Items(
      itemID INTEGER PRIMARY KEY,
      sellerID CHAR(50),
      name CHAR(50),
      currently FLOAT,
      firstBid FLOAT,
      numberOfBids INTEGER,
      started CHAR(50),
      ends CHAR(50),
      description CHAR(100),
      FOREIGN KEY (sellerID) REFERENCES Users(userID)
);

create table Bids(
     itemID INTEGER,
     bidderID CHAR(50),
     time CHAR(50),
     amount FLOAT,
     FOREIGN KEY (itemID) REFERENCES Items(itemID),
     FOREIGN KEY (bidderID) REFERENCES Users(userID)
);

create table Categories (
      itemID INTEGER NOT NULL,
      category CHAR(50) NOT NULL,
      FOREIGN KEY (itemID) REFERENCES Items(itemID)
      PRIMARY KEY (itemID, category)
);
            
create table Users (
       userID CHAR(50) PRIMARY KEY,
       rating INTEGER,
       location CHAR(50),
       country CHAR(50)
);

    
