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
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `company_id` int NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'The Burger Joint','New York, NY','Operations'),(2,'Pasta Palace','Chicago, IL','IT Support'),(3,'Sushi Zen','San Francisco, CA','Management'),(4,'Taco Fiesta','Austin, TX','Technical Services'),(5,'Steakhouse 101','Miami, FL','Procurement'),(6,'Pizzeria Napoli','Naples, FL','Kitchen'),(7,'The Green Garden','Portland, OR','Operations'),(8,'Blue Lagoon Seafood','Seattle, WA','Management'),(9,'Mama Leone Kitchen','Boston, MA','IT'),(10,'Curry Express','London, UK','Technical'),(11,'Waffle House #44','Atlanta, GA','Operations'),(12,'The Daily Grind','Denver, CO','Support'),(13,'Salsa King','Phoenix, AZ','IT'),(14,'Noodle Bar','Vancouver, BC','Operations'),(15,'Bistro 21','Montreal, QC','Admin'),(16,'Dim Sum Palace','Toronto, ON','Kitchen'),(17,'The Steak Pit','Dallas, TX','Operations'),(18,'Vegan Vibes','Austin, TX','Management'),(19,'Golden Dragon','San Jose, CA','Technical'),(20,'Pizza Hut #12','San Diego, CA','Operations'),(21,'The Bagel Shop','Nashville, TN','Admin'),(22,'Ramen Ichiban','Honolulu, HI','Kitchen'),(23,'Classic Diner','Philadelphia, PA','Support'),(24,'Taco Time','Las Vegas, NV','IT'),(25,'Smoothie King','New Orleans, LA','Management');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
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

-- Dump completed on 2026-02-23  9:40:29
