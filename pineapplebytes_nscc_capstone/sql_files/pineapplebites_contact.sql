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
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `contact_id` int NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `extension` varchar(10) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `relationship` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (101,'Gordon','Ramsey','5550101','10','Head Chef','Primary','Client','gramsey@burgerjoint.com'),(102,'Maria','Rossi','5550202','22','Manager','Secondary','Client','mrossi@pastapalace.com'),(103,'Kenji','Sato','5550303','0','Owner','Primary','Client','ksato@sushizen.com'),(104,'Elena','Rodriguez','5550404','5','IT Lead','Technical','Client','erod@tacofiesta.com'),(105,'Robert','Miller','5550505','101','Purchasing','Billing','Client','rmiller@steakhouse.com'),(106,'Marco','Polo','5551101','1','Owner','Primary','Client','marco@pizzeria.com'),(107,'Sarah','Lee','5551102','0','Chef','Technical','Client','lee@greengarden.com'),(108,'James','Cook','5551103','5','Manager','Primary','Client','jcook@bluelagoon.com'),(109,'Anita','Dash','5551104','2','IT Tech','Technical','Client','adash@mamaleone.com'),(110,'Raj','Patel','5551105','0','Admin','Secondary','Client','rpatel@curryex.com'),(111,'Lucy','Sky','5551106','12','Cashier','Primary','Client','lsky@waffle.com'),(112,'Bill','Gates','5551107','0','CEO','Primary','Client','bill@dailygrind.com'),(113,'Rosa','Diaz','5551108','3','Supervisor','Technical','Client','rdiaz@salsaking.com'),(114,'Tom','Hardy','5551109','1','Chef','Secondary','Client','tom@noodlebar.com'),(115,'Emily','Blunt','5551110','0','Owner','Primary','Client','emily@bistro21.com'),(116,'Kevin','Hart','5551111','4','Manager','Technical','Client','kevin@dimsum.com'),(117,'Chris','Pratt','5551112','11','IT Lead','Primary','Client','pratt@steakpit.com'),(118,'Zoe','Saldana','5551113','0','Partner','Secondary','Client','zoe@veganvibes.com'),(119,'Will','Smith','5551114','2','Clerk','Primary','Client','will@goldendragon.com'),(120,'Anne','Hath','5551115','0','Director','Primary','Client','anne@pizzahut.com'),(121,'Peter','Parker','5551116','9','Intern','Technical','Client','peter@bagel.com'),(122,'Bruce','Wayne','5551117','101','Owner','Primary','Client','bruce@ramen.com'),(123,'Clark','Kent','5551118','0','Reporter','Secondary','Client','clark@classic.com'),(124,'Diana','Prince','5551119','7','Manager','Technical','Client','diana@tacotime.com'),(125,'Barry','Allen','5551120','0','IT','Primary','Client','barry@smoothie.com');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
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
