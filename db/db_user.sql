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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `uid` int NOT NULL,
  `account` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `longitude` float NOT NULL,
  `latitude` float NOT NULL,
  `wallet` int NOT NULL,
  `phone` varchar(10) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user1','$2b$12$OJDXxadWKg35X05cBBzsRubYo1H8kyyQm33k1aTKMn4ae.kC/wD9G','user',121.6,23.1,4684,'0912345678'),(2,'user2','$2b$12$WUoTj4NSSNsW3O5QbBsCNuArg0.e2t0XBxgolbEdLQOyypq6R0qP6','userr',121,25,2426,'0912345678'),(3,'user3','$2b$12$ECtZBOmEbLznvIqjqPMUuuJtuNcQEILoG0fpn2tZtFmSg1rjspSwe','userrr',120,20,0,'0912345678'),(4,'user4','$2b$12$AYOPX.S2ONx4zsFfXgzj3OdkVHUURJbl2T/DxP1RnXJE7S8b74WKm','userrrr',120,20,0,'0912345678'),(5,'user5','$2b$12$gl/CH/cN7SRNi5aQkIu3A.L6G8t9wSG81Y1RE4W/Z3sAdWwY4PrwC','userrrrr',120,20,0,'0912345678'),(6,'user6','$2b$12$nrVPo3pDJrk8b2xEMTQc.OpZK61L3.MOSYmIhxCPHVFg0cRonoKqC','userrrrrr',120,20,0,'0912345678'),(7,'user10','$2b$12$NvUIMs/RAQoEuBQh/3YoQOGK2uYhXD9Wum5/MF1BIgEyvuGmdPjpa','Tom',120.997,24.787,0,'0912345678');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-02  0:34:33
