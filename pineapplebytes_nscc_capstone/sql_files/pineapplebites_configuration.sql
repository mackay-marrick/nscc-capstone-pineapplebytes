-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
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
-- Table structure for table `configuration`
--

DROP TABLE IF EXISTS `configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration` (
  `configuration_id` int NOT NULL,
  `configuration_name` varchar(255) DEFAULT NULL,
  `configuration_type` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `tag_number` varchar(100) DEFAULT NULL,
  `model_number` varchar(100) DEFAULT NULL,
  `purchased_date` date DEFAULT NULL,
  PRIMARY KEY (`configuration_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration`
--

LOCK TABLES `configuration` WRITE;
/*!40000 ALTER TABLE `configuration` DISABLE KEYS */;
INSERT INTO `configuration` VALUES (801,'Front Counter POS 1','Terminal','Online','998877','1001','5500','2024-11-12'),(802,'Kitchen Display Unit','Monitor','Damaged','887766','1002','3300','2024-05-20'),(803,'Main Server Rack','Server','Online','776655','1003','9000','2023-10-05'),(804,'Outdoor Tablet 1','Handheld','In Repair','665544','1004','2200','2025-01-15'),(805,'Printer Kitchen 1','Hardware','Online','1122','2001','101','2024-05-10'),(806,'Router Main','Network','Online','3344','2002','202','2024-01-15'),(807,'POS Tablet 5','Mobile','Offline','5566','2003','303','2025-02-01'),(808,'Scanner Front','Hardware','Online','7788','2004','404','2024-11-20'),(809,'Server Mini','Hardware','Repair','9900','2005','505','2023-12-05'),(810,'Display Wall','Monitor','Online','1212','2006','606','2024-06-30'),(811,'Printer Receipt','Hardware','Online','3434','2007','707','2024-08-15'),(812,'POS Stand 1','Stand','Broken','5656','2008','808','2024-02-10'),(813,'Cash Drawer','Hardware','Online','7878','2009','909','2024-09-01'),(814,'Card Reader 1','Hardware','Online','9090','2010','110','2025-01-12'),(815,'Handheld 1','Mobile','Online','2121','2011','211','2025-01-05'),(816,'UPS Backup','Battery','Online','4343','2012','312','2024-03-25'),(817,'POS Terminal 6','Hardware','Offline','6565','2013','413','2024-12-10'),(818,'Kitchen Screen 2','Monitor','Online','8787','2014','514','2024-07-05'),(819,'Wall Mount','Hardware','Online','1010','2015','615','2024-05-20'),(820,'Modem Fiber','Network','Online','3030','2016','716','2024-01-05'),(821,'Scanner Barcode','Hardware','Repair','5050','2017','817','2025-02-15'),(822,'Order Tablet 7','Mobile','Online','7070','2018','918','2024-10-10'),(823,'Ethernet Switch','Network','Online','9090','2019','119','2024-11-01'),(824,'POS Tablet 8','Mobile','Online','1111','2020','220','2025-01-20');
/*!40000 ALTER TABLE `configuration` ENABLE KEYS */;
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
