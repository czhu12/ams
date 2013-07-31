CREATE TABLE Item (
upc VARCHAR(20), 
title VARCHAR(50),
type ENUM('cd', 'dvd'),
category ENUM('rock', 'pop', 'rap', 'country', 'classical', 'new age', 'instrumental'),
company VARCHAR(50),
year
price 
stock
PRIMARY KEY(upc)
);

CREATE TABLE LeadSinger (
upc VARCHAR(20),
name VARCHAR(50),
PRIMARY KEY(upc, name)
);

CREATE TABLE HasSong (
upc VARCHAR(20),
title VARCHAR(50),
PRIMARY KEY(upc, title)
);

CREATE TABLE Purchase (
receiptId INTEGER,
date DATE,
cid INTEGER,
card_num 
);
