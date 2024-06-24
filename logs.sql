/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: logs
-- ------------------------------------------------------
-- Server version	10.6.18-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('9ce12d7d9356');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s3bucket`
--

DROP TABLE IF EXISTS `s3bucket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `s3bucket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aws_access_key_id` varchar(100) NOT NULL,
  `aws_secret_access_key` varchar(100) NOT NULL,
  `bucket_name` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `s3bucket_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s3bucket`
--

LOCK TABLES `s3bucket` WRITE;
/*!40000 ALTER TABLE `s3bucket` DISABLE KEYS */;
INSERT INTO `s3bucket` VALUES (1,'AKIA47CRY4FXQJTGZYHJ','LD1OHNrAoIsdusrimjV7aoKhn/ZqdEOTtj8RDm+5','s3tochlogtest',2),(2,'AKIA47CRY4FX7VHS7I3S','HIGT/qhQn5b1WY6Lq075YgMcKZp2nLEVYK9XvM8o','logtestscomp',3),(3,'AKIA47CRY4FX7VHS7I3S','HIGT/qhQn5b1WY6Lq075YgMcKZp2nLEVYK9XvM8o','logtestscomp',1),(4,'AKIA47CRY4FX7VHS7I3S','HIGT/qhQn5b1WY6Lq075YgMcKZp2nLEVYK9XvM8o','logtestscomp',3);
/*!40000 ALTER TABLE `s3bucket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `aws_access_key_id` varchar(100) DEFAULT NULL,
  `aws_secret_access_key` varchar(100) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_suspended` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin@example.com','scrypt:32768:8:1$lCRC0wq2Q965UGe5$ea8e9ab051217f4ebf2da00b763c175574ea2e88722667e2e32f1a657e96b7b0e566abbde9754d509e250ef5f82f15b8d6e6cf94f4f41b30d0170742465d14e6',NULL,NULL,1,NULL),(2,'satish','satishkushwaha1987@gmail.com','scrypt:32768:8:1$75Kp6Ml4ILtPQPDk$8170a7cf9f62a90536d7ad41c3f6c00c5a98b68055f1254873802cf31af9d590194aee21c20601bbe38d31648bd171b4ba23542eac9cbf0235e47855f163f5e4','AKIA47CRY4FXQJTGZYHJ','LD1OHNrAoIsdusrimjV7aoKhn/ZqdEOTtj8RDm+5',1,NULL),(3,'kushwaha','kushwaha1987@live.com','scrypt:32768:8:1$Myq527Z0T55LPeuu$f24d316076e7add4a60614e4316d3d3a3105301e1616242f6322b87c9efa94ebbf0e4c1c9c4111b605f42791134b7982af27a59ea4efc382e1bc39af689668a5','','',0,NULL);
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

-- Dump completed on 2024-06-24 21:58:45
