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
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL,
  `total_hours` decimal(5,2) DEFAULT NULL,
  `age` decimal(10,1) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `schedule_flag` varchar(255) DEFAULT NULL,
  `summary_description` text,
  `priority` varchar(50) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `ticket_type` varchar(100) DEFAULT NULL,
  `subtype` varchar(100) DEFAULT NULL,
  `item` varchar(100) DEFAULT NULL,
  `date_entered` date DEFAULT NULL,
  `team_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (9001,2.00,4.0,'Open','Scheduled','POS Terminal #4 not powering on','High',500.00,'Hardware','Repair','401','2026-02-15','Emergency Response'),(9002,1.00,1.0,'In Progress','Unscheduled','Software update for menu pricing','Medium',0.00,'Software','Update','205','2026-02-18','Menu & Pricing Ops'),(9003,3.00,18.0,'Closed','Scheduled','Monthly network security audit','Low',250.00,'Maintenance','Audit','110','2026-02-01','Remote Software Support'),(9004,0.00,0.0,'Open','Unscheduled','Kitchen Printer failing during rush','Emergency',150.00,'Hardware','Replacement','302','2026-02-19','Emergency Response'),(9005,4.00,9.0,'Pending','Scheduled','Training session for new staff','Low',100.00,'Service','Training','550','2026-02-10','Menu & Pricing Ops'),(9006,5.00,0.0,'Open','U','Server down in Pizza Hut','High',200.00,'Hardware','Server','806','2026-02-19','POS Hardware Repair'),(9007,1.00,4.0,'Closed','S','Update menu price','Low',0.00,'Software','Config','807','2026-02-15','Remote Software Support'),(9008,2.00,1.0,'In Progress','U','Replace screen','Medium',150.00,'Hardware','Monitor','810','2026-02-18','POS Hardware Repair'),(9009,1.00,0.0,'Open','U','Printer Jamming','High',50.00,'Hardware','Printer','805','2026-02-19','POS Hardware Repair'),(9010,3.00,9.0,'Pending','S','Network Check','Low',100.00,'Network','Audit','823','2026-02-10','Network Infrastructure'),(9011,1.00,49.0,'Closed','S','Reset Router','Low',0.00,'Hardware','Network','806','2026-01-01','Network Infrastructure'),(9012,8.00,0.0,'Open','U','Database Error','High',500.00,'Software','Critical','824','2026-02-19','Remote Software Support'),(9013,1.00,1.0,'In Progress','S','Battery swap','Medium',75.00,'Hardware','Power','816','2026-02-18','POS Hardware Repair'),(9014,1.00,14.0,'Closed','S','Cleaning terminal','Low',20.00,'Maintenance','Clean','817','2026-02-05','Menu & Pricing Ops'),(9015,0.00,0.0,'Open','S','Add new user','Medium',0.00,'Software','Admin','809','2026-02-19','Remote Software Support'),(9016,1.00,0.0,'Pending','U','Tablet Won\'t Charge','High',100.00,'Hardware','Mobile','807','2026-02-19','POS Hardware Repair'),(9017,2.00,30.0,'Closed','U','Cable fix','Low',40.00,'Hardware','Cable','821','2026-01-20','POS Hardware Repair'),(9018,4.00,0.0,'Open','U','Wifi Failure','High',250.00,'Network','Wifi','820','2026-02-19','Network Infrastructure'),(9019,1.00,1.0,'In Progress','S','Menu sync','Low',0.00,'Software','Sync','818','2026-02-18','Remote Software Support'),(9020,1.00,5.0,'Closed','U','Emergency Reboot','High',0.00,'Software','Reboot','819','2026-02-14','Remote Software Support'),(9021,10.00,0.0,'Open','S','New install','Medium',2000.00,'Project','New','814','2026-02-19','On-Site Technicians'),(9022,2.00,8.0,'Pending','S','Staff training','Low',150.00,'Service','Train','815','2026-02-11','Menu & Pricing Ops'),(9023,3.00,0.0,'Open','U','Card reader error','High',80.00,'Hardware','Reader','814','2026-02-19','POS Hardware Repair'),(9024,0.00,9.0,'Closed','S','Paper restock','Low',10.00,'Service','Supply','811','2026-02-10','On-Site Technicians'),(9025,2.00,1.0,'In Progress','U','Scanner lag','Medium',60.00,'Hardware','Scanner','821','2026-02-18','POS Hardware Repair');
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
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
