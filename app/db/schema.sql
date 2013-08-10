CREATE TABLE Item (
	upc INTEGER AUTO_INCREMENT, 
	title VARCHAR(50),
	type ENUM('cd', 'dvd'),
	category ENUM('rock', 'pop', 'rap', 'country', 'classical', 'new age', 'instrumental'),
	company VARCHAR(50),
	year DATE,
	price NUMERIC(5,2),
	stock INTEGER,
	PRIMARY KEY(upc)
)
	AUTO_INCREMENT = 1000
;

CREATE TABLE LeadSinger (
	upc INTEGER,
	name VARCHAR(50),
	PRIMARY KEY(upc, name),
	FOREIGN KEY(upc) REFERENCES Item(upc)
);

CREATE TABLE HasSong (
	upc INTEGER,
	title VARCHAR(50),
	PRIMARY KEY(upc, title),
	FOREIGN KEY(upc) REFERENCES Item(upc)
);

CREATE TABLE Customer(
  	cid INTEGER AUTO_INCREMENT,
	password VARCHAR(20),
	name VARCHAR(50),
	address VARCHAR(50),
	phone VARCHAR (20),
	PRIMARY KEY(cid)
)
	AUTO_INCREMENT = 1000
;

CREATE TABLE Purchase (
	receiptid INTEGER AUTO_INCREMENT,
	purchasedate DATE,
	cid INTEGER,
	cardnum CHAR(16),
	expirydate DATE,
	expecteddate DATE,
	delivereddate DATE,
	PRIMARY KEY(receiptid),
	FOREIGN KEY(cid) REFERENCES Customer(cid)
)
	AUTO_INCREMENT = 1000
;

CREATE TABLE PurchaseItem (
	receiptid INTEGER,
	upc INTEGER,
	quantity INTEGER,
	PRIMARY KEY(receiptid, upc),
	FOREIGN KEY(receiptid) REFERENCES Purchase(receiptid),
	FOREIGN KEY(upc) REFERENCES Item(upc)
);

CREATE TABLE ReturnTable(
	retid INTEGER AUTO_INCREMENT,
	returndate DATE,
	receiptid INTEGER,
	PRIMARY KEY(retid),
	FOREIGN KEY(receiptid) REFERENCES Purchase(receiptid)
)
	AUTO_INCREMENT = 1000
;

CREATE TABLE ReturnItem(
	retid INTEGER,
	upc INTEGER,
	quantity INTEGER,
	PRIMARY KEY(retid, upc),
	FOREIGN KEY(upc) REFERENCES Item(upc)
);

