INSERT INTO Item (title, type, category, company, year, price, stock)
VALUES ('So Good', 'cd', 'rock', 'AMS Label', '2012-01-01', 20.01, 10);

INSERT INTO Item (title, type, category, company, year, price, stock)
VALUES ('So Cool', 'cd', 'pop', 'George Label', '2011-01-01', 155.15, 0);

INSERT INTO Item (title, type, category, company, year, price, stock)
VALUES ('Just do it', 'dvd', 'country', 'AMS Label', '2012-01-01', 9.99, 10);

INSERT INTO Item (title, type, category, company, year, price, stock)
VALUES ('Feel Good', 'dvd', 'new age', 'YES', '2012-01-01', 5.55, 100);

INSERT INTO Item (title, type, category, company, year, price, stock)
VALUES ('Enjoy', 'cd', 'classical', 'Old Label', '2001-01-01', 15.00, 1);

INSERT INTO Purchase(purchasedate)
VALUES ('2013-05-01');

INSERT INTO Purchase(purchasedate, cardnum, expirydate)
VALUES ('2013-07-20', '1212121290909090', '2014-05-14');

INSERT INTO Purchase(purchasedate)
VALUES ('2013-08-05');

INSERT INTO Purchase(purchasedate, cardnum, expirydate)
VALUES ('2013-08-05', '1212121290909090', '2014-05-14');

INSERT INTO PurchaseItem VALUES (1000, 1000, 1);
INSERT INTO PurchaseItem VALUES (1000, 1001, 2);

INSERT INTO PurchaseItem VALUES (1001, 1002, 1);
INSERT INTO PurchaseItem VALUES (1001, 1004, 5);

INSERT INTO PurchaseItem VALUES (1002, 1000, 1);
INSERT INTO PurchaseItem VALUES (1002, 1001, 2);

INSERT INTO PurchaseItem VALUES (1003, 1002, 1);
INSERT INTO PurchaseItem VALUES (1003, 1004, 5);

