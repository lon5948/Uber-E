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
-- Table structure for table `shop`
--

DROP TABLE IF EXISTS `shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop` (
  `uid` int DEFAULT NULL,
  `sid` int NOT NULL AUTO_INCREMENT,
  `shopname` varchar(255) DEFAULT NULL,
  `shoptype` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `location` geometry NOT NULL,
  PRIMARY KEY (`sid`),
  KEY `uid` (`uid`),
  SPATIAL KEY `idx_location` (`location`),
  CONSTRAINT `shop_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop`
--

LOCK TABLES `shop` WRITE;
/*!40000 ALTER TABLE `shop` DISABLE KEYS */;
INSERT INTO `shop` VALUES (1,17,'macdonald','fast food',24.7847,121,_binary '\0\0\0\0\0\0\0D‘ú\ã\ã\È8@ª\Óo@^@'),(2,18,'starbucks','coffee',24.8115,120.975,_binary '\0\0\0\0\0\0\0×€Y»\Ï8@\nü\ì\ëa>^@'),(3,19,'user3','user3',20,120,_binary '\0\0\0\0\0\0\0\0\0\0\0\0\04@\0\0\0\0\0\0^@'),(4,20,'user4','user4',20,120,_binary '\0\0\0\0\0\0\0\0\0\0\0\0\04@\0\0\0\0\0\0^@'),(5,21,'user5','user5',20,120,_binary '\0\0\0\0\0\0\0\0\0\0\0\0\04@\0\0\0\0\0\0^@'),(6,22,'user6','user6',20,120,_binary '\0\0\0\0\0\0\0\0\0\0\0\0\04@\0\0\0\0\0\0^@'),(7,23,'Kentucky Fried Chicken','fast food',24.7996,121.012,_binary '\0\0\0\0\0\0\0§\ÅdÍ°\Ì8@QNûŸ\È@^@');
/*!40000 ALTER TABLE `shop` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-03 12:48:14
