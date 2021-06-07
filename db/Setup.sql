
create database IF NOT EXISTS Loyality_System_DB;

CREATE TABLE IF NOT EXISTS costumer
(
  costumerID INTEGER PRIMARY KEY,
  email VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS product_order
(
  product_orderID INTEGER PRIMARY KEY,
  unit_price INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  productID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS costumer_order
(
  costumer_orderID INTEGER PRIMARY KEY,
  total_price INTEGER NOT NULL,
  costumerID INTEGER NOT NULL,
  product_orderID INTEGER NOT NULL,
  order_date datetime NOT NULL,
  discount INTEGER NOT NULL,
  FOREIGN KEY (costumerID) REFERENCES costumer (costumerID),
  FOREIGN KEY (product_orderID) REFERENCES product_order (product_orderID)
);