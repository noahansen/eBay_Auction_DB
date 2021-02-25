
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Completed parser Author: Noah Hansen (nphansen@wisc.edu)
Modified: 2/25/2021

Has useful imports and functions for parsing, including:

1) Directory handling -- the parser takes a list of json files
and opens each file inside of a loop. You need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Author: Noah Hansen

Parses a single json file, putting the data for each table into .DAT files
so they can be bulk loaded into the database. For the bulk loading to work, all double quotes
are escaped with an additional double quote. All string value are surrounded by double quotes.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        # 4 files for the 4 tables in the DB
        b = open("bids.DAT", "a")
        u = open("users.DAT", "a")
        c = open("categories.DAT","a")
        it = open("items.DAT","a")

        for item in items:

            # fields for the items table
            item_id = item["ItemID"]
            # escape double quotations with another quotation
            name = '"%s"' % sub(r'"', '""', item["Name"])
            currently = transformDollar(item["Currently"])
            first_bid = transformDollar(item["First_Bid"])
            num_bids = item["Number_of_Bids"]
            location = '"%s"' % sub(r'"', '""',item["Location"])
            country_seller = '"%s"' % item["Country"]
            started = '"%s"' % transformDttm(item["Started"])
            ends = '"%s"' % transformDttm(item["Ends"])
            seller_id = '"%s"' % item["Seller"]["UserID"]
            rating = item["Seller"]["Rating"]
            description = item["Description"]

            if description == None: # some of the descriptions are null.
                 description = "NULL" # Will convert this to a null value later using sql

            description = '"%s"' % sub(r'"', '""', description)  

            # write to items table
            it.write(item_id + columnSeparator + seller_id + columnSeparator + 
                     name + columnSeparator + currently + columnSeparator + 
                     first_bid + columnSeparator + num_bids + columnSeparator + 
                     started + columnSeparator + ends + columnSeparator + 
                     description + "\n")

            # bids table
            bids = item["Bids"] # all of the bids on an item are in this bids array
            if bids != None:
                for bid in bids: 
                    bidder_id = '"%s"' % bid["Bid"]["Bidder"]["UserID"]
                    time = '"%s"' % bid["Bid"]["Time"]
                    amount = transformDollar(bid["Bid"]["Amount"])

                    # write to the bids table
                    b.write(item_id + columnSeparator)
                    b.write(bidder_id + columnSeparator)
                    b.write(time + columnSeparator)
                    b.write(amount + "\n")

                    # write the bidder data to the user table
                    u.write(bidder_id + columnSeparator)
                    u.write(bid["Bid"]["Bidder"]["Rating"] + columnSeparator)
                    
                    # Instead of being empty, sometimes the location field does not even exist in the json
                    try:
                        loc = '"%s"' % sub(r'"', '""', bid["Bid"]["Bidder"]["Location"])
                    except:
                        loc =  None

                    if(loc == None):
                        loc = "NULL
                    
                    u.write(loc + columnSeparator)

                    try:
                        country = '"%s"' % bid["Bid"]["Bidder"]["Country"]
                    except:
                        country = '"NULL"'

                    u.write(country + "\n")

            #write the seller data to the users table 
            u.write(seller_id + columnSeparator)
            u.write(rating + columnSeparator)
            u.write(location + columnSeparator)
            u.write(country_seller + "\n")


            #write to the category table
            for cat in item["Category"]:
                c.write(item_id + columnSeparator + '"%s"' % cat + "\n")

        b.close()
        u.close()
        c.close()
        it.close()
     

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python3 parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
