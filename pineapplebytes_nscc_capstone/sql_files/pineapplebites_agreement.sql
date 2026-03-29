<<<<<<< HEAD
﻿-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
=======
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
--
-- Host: localhost    Database: pineapplebites
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'e06b7f8f-0d92-11f1-9116-a83ca52f83f5:1-87';

--
-- Table structure for table `agreement`
--

DROP TABLE IF EXISTS `agreement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agreement` (
  `agreement_id` int NOT NULL,
  `agreement_type` varchar(100) DEFAULT NULL,
  `agreement_name` varchar(255) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `billing_cycle` varchar(50) DEFAULT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`agreement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agreement`
--

LOCK TABLES `agreement` WRITE;
/*!40000 ALTER TABLE `agreement` DISABLE KEYS */;
INSERT INTO `agreement` VALUES (501,'SLA','Premium POS Support','1200.00','30','2025-01-01','2026-01-01','Active'),(502,'Maintenance','Hardware Maintenance','500.00','90','2024-06-01','2025-06-01','Expiring'),(503,'Subscription','Cloud Backup Basic','150.00','30','2025-02-15','2027-02-15','Active'),(504,'Software','Full Enterprise License','5000.00','365','2025-01-10','2026-01-10','Active'),(505,'Software','Cloud Storage','99.00','30','2025-03-01','2026-03-01','Active'),(506,'Maintenance','Hardware Care','450.00','365','2025-01-01','2026-01-01','Active'),(507,'SLA','POS Gold Plus','800.00','30','2024-12-01','2025-12-01','Active'),(508,'Software','Kitchen Monitor','120.00','30','2025-02-01','2026-02-01','Active'),(509,'Service','Network Security','300.00','90','2025-01-15','2026-01-15','Active'),(510,'SLA','24/7 Remote Support','1500.00','365','2025-05-01','2026-05-01','Pending'),(511,'Maintenance','Tablet Warranty','200.00','365','2024-08-01','2025-08-01','Expiring'),(512,'Software','Email Hosting','50.00','30','2025-01-01','2026-01-01','Active'),(513,'Maintenance','Security Camera','600.00','180','2024-11-01','2025-11-01','Active'),(514,'Software','Backup Service','75.00','30','2025-02-10','2026-02-10','Active'),(515,'SLA','Premium Support','1000.00','30','2025-03-15','2026-03-15','Active'),(516,'Hardware','Printer Rental','300.00','90','2025-01-01','2026-01-01','Active'),(517,'Subscription','Software License A','2000.00','365','2024-05-01','2025-05-01','Active'),(518,'Software','Antivirus Bundle','150.00','365','2025-01-20','2026-01-20','Active'),(519,'Service','Server Hosting','2500.00','365','2024-10-01','2025-10-01','Active'),(520,'Maintenance','Database Care','400.00','30','2025-02-01','2026-02-01','Active'),(521,'Project','App Integration','5000.00','0','2025-01-01','2025-06-01','Closed'),(522,'SLA','Legacy Support','300.00','30','2025-04-01','2026-04-01','Active'),(523,'Service','Wireless Install','1200.00','0','2025-02-15','2025-03-15','Active'),(524,'Software','POS Essentials','500.00','365','2025-01-05','2026-01-05','Active');
/*!40000 ALTER TABLE `agreement` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-23  9:40:30
