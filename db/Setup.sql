-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 18, 2021 at 07:59 PM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Setup`
--

-- --------------------------------------------------------

--
-- Table structure for table `costumer`
--

create database Loyality_System_DB;

CREATE TABLE `costumer` (
  `costumerID` int(11) NOT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `costumer_order`
--

CREATE TABLE `costumer_order` (
  `costumer_orderID` int(11) NOT NULL,
  `total_price` int(11) NOT NULL,
  `costumerID` int(11) NOT NULL,
  `product_orderID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `product_order`
--

CREATE TABLE `product_order` (
  `product_orderID` int(11) NOT NULL,
  `unit_price` int(11) NOT NULL,
  `productID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `costumer`
--
ALTER TABLE `costumer`
  ADD PRIMARY KEY (`costumerID`);

--
-- Indexes for table `costumer_order`
--
ALTER TABLE `costumer_order`
  ADD PRIMARY KEY (`costumer_orderID`),
  ADD KEY `costumerID` (`costumerID`),
  ADD KEY `product_orderID` (`product_orderID`);

--
-- Indexes for table `product_order`
--
ALTER TABLE `product_order`
  ADD PRIMARY KEY (`product_orderID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `costumer_order`
--
ALTER TABLE `costumer_order`
  ADD CONSTRAINT `costumer_order_ibfk_1` FOREIGN KEY (`costumerID`) REFERENCES `costumer` (`costumerID`),
  ADD CONSTRAINT `costumer_order_ibfk_2` FOREIGN KEY (`product_orderID`) REFERENCES `product_order` (`product_orderID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
