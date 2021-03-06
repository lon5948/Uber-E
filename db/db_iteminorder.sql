-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.0.29

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

--
-- Table structure for table `iteminorder`
--

DROP TABLE IF EXISTS `iteminorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iteminorder` (
  `oid` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `quantity` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iteminorder`
--

LOCK TABLES `iteminorder` WRITE;
/*!40000 ALTER TABLE `iteminorder` DISABLE KEYS */;
INSERT INTO `iteminorder` VALUES (1,'user','1653469111860854300.png',130,2),(2,'user','1653469111860854300.png',130,1),(3,'user','1654237062028890100.jpg',45,1),(4,'chicken','1654237062028890100.jpg',1000,1),(5,'a','1653551588575691300.gif',100,1),(6,'espresso','1653469111860854300.png',130,2),(7,'latte','1653469097963337500.jpg',100,4),(8,'latte','1653469097963337500.jpg',100,10),(9,'espresso','1653469111860854300.png',130,5),(10,'latte','1653469097963337500.jpg',100,5),(11,'espresso','1653469111860854300.png',130,4),(12,'latte','1653469097963337500.jpg',100,1),(12,'espresso','1653469111860854300.png',130,1),(13,'latte','1653469097963337500.jpg',100,1),(13,'espresso','1653469111860854300.png',130,1),(14,'latte','1653469097963337500.jpg',100,1),(14,'espresso','1653469111860854300.png',130,2),(15,'latte','1653469097963337500.jpg',100,2),(15,'espresso','1653469111860854300.png',130,2),(16,'chicken','1654237062028890100.jpg',1000,2),(17,'chicken','1654237062028890100.jpg',1000,2),(18,'chicken','1654237062028890100.jpg',1000,10),(19,'chicken','1654237062028890100.jpg',1000,12),(20,'chicken','1654237062028890100.jpg',1000,12),(21,'chicken','1654237062028890100.jpg',1000,10),(22,'chicken','1654237062028890100.jpg',1000,1),(23,'chicken','1654237062028890100.jpg',1000,1),(24,'chicken','1654237062028890100.jpg',1000,1),(25,'chicken','1654237062028890100.jpg',1000,12),(26,'chicken','1654237062028890100.jpg',1000,1),(27,'chicken','1654237062028890100.jpg',1000,2),(28,'latte','1653469097963337500.jpg',100,1),(29,'chicken','1654237062028890100.jpg',1000,1),(30,'chicken','1654237062028890100.jpg',1000,12),(31,'chicken','1654237062028890100.jpg',1000,1),(32,'chicken','1654237062028890100.jpg',1000,2),(33,'chicken','1654237062028890100.jpg',1000,1),(34,'chicken','1654237062028890100.jpg',1000,1),(35,'chicken','1654237062028890100.jpg',1000,2),(36,'a','1653551588575691300.gif',100,2),(37,'b','1653551617428719600.gif',100,1),(38,'b','1653551617428719600.gif',100,2),(39,'latte','1653469097963337500.jpg',100,1),(40,'latte','1653469097963337500.jpg',100,3),(41,'latte','1653469097963337500.jpg',100,1),(41,'espresso','1653469111860854300.png',130,1),(42,'c','1653551631306578500.gif',100,1),(43,'d','1653551661371712200.jpg',100,3),(44,'dog','1654417676735644100.jpg',62,5),(45,'b','1653551617428719600.gif',100,5),(46,'b','1653551617428719600.gif',100,1),(47,'b','1653551617428719600.gif',100,5),(48,'c','1653551631306578500.gif',100,8),(49,'b','1653551617428719600.gif',100,2),(50,'c','1653551631306578500.gif',100,2),(51,'b','1653551617428719600.gif',100,5),(52,'b','1653551617428719600.gif',100,2);
/*!40000 ALTER TABLE `iteminorder` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-15 14:48:55
