-- MySQL dump 10.13  Distrib 5.5.50, for Linux (x86_64)
--
-- Host: localhost    Database: onthego_db
-- ------------------------------------------------------
-- Server version	5.5.50-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `distributor`
--

DROP TABLE IF EXISTS `distributor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distributor` (
  `did` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distributor`
--

LOCK TABLES `distributor` WRITE;
/*!40000 ALTER TABLE `distributor` DISABLE KEYS */;
INSERT INTO `distributor` VALUES (1,'El Table'),(2,'The Hoop');
/*!40000 ALTER TABLE `distributor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `price` decimal(5,2) unsigned DEFAULT NULL,
  `distributor` int(10) unsigned DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`mid`),
  KEY `distributor` (`distributor`),
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`distributor`) REFERENCES `distributor` (`did`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'El Table Club',7.00,1,'bacon, turkey, avocado, tomato,\ngreens, provolone, and mayo on sourdough bread'),(2,'ABCD',5.50,1,'apple, bacon, cheddar, and dijon on wheat\nbread'),(3,'LGBLT',4.50,1,'lettuce, bacon, tomato, and mayo on\nsourdough bread'),(4,'The Green Monstah',5.50,1,'avocado, pesto, goat cheese,\nprovolone, and greens on sourdough bread'),(5,'Bread Serious',6.50,1,'turkey, brie, cranberry sauce, and walnuts on rosemary'),(6,'The Bro-wich',5.00,1,'a-bro-cado and bro-volone cheese toasted on a plain bagel'),(7,'The Consensu-el',2.00,1,'avocado on a slice of multigrain toast'),(8,'The Consensu-el (+ bacon)',3.00,1,'avocado and bacon on a slice of multigrain toast'),(9,'Darjeeling Limited',4.50,1,'brie and mango chutney on multigrain bread'),(10,'Darjeeling Limited (+ ham)',5.50,1,'brie, mango chutney, and ham on multigrain bread'),(11,'Italiano',6.00,1,'ham, pesto, roasted red pepeprs, and provolone on rosemary garlic bread'),(12,'Le Petit Francais',6.00,1,'brie, apple, honey, and walnuts on a croissant'),(13,'Murphys Law',4.50,1,'cheddar, avocado, and tomato toasted on rye bread'),(14,'Love Snack',3.50,1,'brie + strawberry jam on a croissant'),(15,'Sharp n Sweet',4.50,1,'cheddar cheese and fig jam on multigrain bread'),(16,'Nutella Croissant',3.00,1,''),(17,'Nutella Croissant (+ apple)',3.50,1,''),(18,'The Tenure Track',7.00,1,'turkey, artichoke tapenade, sun-dried tomatoes, avocado, and provolone on multigrain bread'),(19,'The Tourist',6.50,1,'turkey, avocado, crisp apple slices, and provolone cheese on sourdough bread'),(20,'Uh Huh Honey',4.50,1,'muenster, apple, walnuts, and honey on sourdough bread'),(21,'The Vegan',5.00,1,'hummus, tomato, avocado, roasted red peppers, and salt & pepper on wheat bread'),(22,'Young Money Millionaire',5.00,1,'bagel with cream cheese, avocado, roasted reds, and salt & pepper'),(23,'Rosy Roasty Toasty',4.50,1,'goat cheese, tomatoes, roasted red peppers, pesto, and greens on rosemary garlic bread'),(24,'Mini Quesadilla',2.00,1,'1 gluten free quesadilla'),(25,'Mini Quesadillas',3.00,1,'2 gluten free quesadillas'),(26,'Mini Quesadilla (+ avocado)',3.00,1,'1 gluten free quesadilla + avocado'),(27,'Mini Quesadillas (+ avocado)',4.00,1,'2 gluten free quesadillas + avocado'),(28,'DeSombre Side Salad',3.50,1,'greens with sliced apple, chopped walnuts, and goat cheese (gluten free)'),(29,'Macintyre Side Salad',3.50,1,'greens with hummus, roasted red peppers, and tomatoes (gluten free)'),(30,'Hansu Side Salad',3.50,1,'greens with avocado, sundried tomatoes, and walnuts (gluten free)'),(31,'Hansu Side Salad (+ bacon)',4.50,1,'greens with avocado, sundried tomatoes, walnuts, and bacon (gluten free)');
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `student` int(10) unsigned DEFAULT NULL,
  `distributor` int(10) unsigned DEFAULT NULL,
  `complete` int(1) DEFAULT NULL,
  `dt` datetime DEFAULT NULL,
  `notes` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `distributor` (`distributor`),
  KEY `student` (`student`),
  CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`distributor`) REFERENCES `distributor` (`did`) ON DELETE SET NULL,
  CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`student`) REFERENCES `student` (`bnum`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES (1,23456789,1,1,'2018-05-10 18:03:16',NULL),(2,23456789,1,1,'2018-05-10 18:24:51',NULL),(3,24567890,1,1,'2018-05-10 18:27:50',NULL),(4,24567890,1,1,'2018-05-10 18:48:28','no cheese'),(5,24567890,1,NULL,'2018-05-12 02:10:40',''),(6,24567890,1,NULL,'2018-05-12 02:10:40',''),(7,24567890,1,1,'2018-05-12 02:11:36',''),(8,24567890,1,1,'2018-05-12 02:20:53',''),(9,24567890,1,1,'2018-05-12 02:21:54',''),(10,24567890,1,1,'2018-05-12 02:24:40',''),(11,24567890,1,1,'2018-05-12 02:49:50',''),(12,20805803,1,1,'2018-05-12 18:17:58',''),(13,24567890,1,NULL,'2018-05-13 14:00:23',''),(14,24567890,1,NULL,'2018-05-13 14:37:24',''),(15,24567890,1,NULL,'2018-05-13 14:37:44',''),(16,24567890,1,NULL,'2018-05-13 14:37:51',''),(17,24567890,1,NULL,'2018-05-13 14:38:21',''),(18,24567890,1,NULL,'2018-05-13 14:38:29',''),(19,24567890,1,1,'2018-05-13 14:44:01',''),(20,24567890,1,NULL,'2018-05-13 14:51:17',''),(21,24567890,1,1,'2018-05-13 15:24:30',''),(22,24567890,1,NULL,'2018-05-13 16:39:31',''),(23,24567890,1,NULL,'2018-05-13 16:40:25',''),(24,24567890,1,NULL,'2018-05-13 16:41:49',''),(25,24567890,1,NULL,'2018-05-13 16:44:34',''),(26,24567890,1,NULL,'2018-05-13 16:44:44',''),(27,24567890,1,NULL,'2018-05-13 16:45:33',''),(28,24567890,1,NULL,'2018-05-13 16:45:46',''),(29,20758475,1,1,'2018-05-13 18:57:07','Vegetarian!'),(30,20758475,1,1,'2018-05-13 19:03:52',''),(31,23456789,1,NULL,'2018-05-14 13:27:50',''),(32,24567890,1,1,'2018-05-14 14:06:55',''),(33,24567890,1,1,'2018-05-14 14:07:29','');
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchaseItems`
--

DROP TABLE IF EXISTS `purchaseItems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchaseItems` (
  `pid` int(10) unsigned NOT NULL,
  `mid` int(10) unsigned NOT NULL,
  `quantity` int(2) unsigned DEFAULT NULL,
  `complete` int(1) DEFAULT NULL,
  PRIMARY KEY (`pid`,`mid`),
  KEY `pid` (`pid`),
  KEY `mid` (`mid`),
  CONSTRAINT `purchaseItems_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `purchase` (`pid`),
  CONSTRAINT `purchaseItems_ibfk_2` FOREIGN KEY (`mid`) REFERENCES `menu` (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchaseItems`
--

LOCK TABLES `purchaseItems` WRITE;
/*!40000 ALTER TABLE `purchaseItems` DISABLE KEYS */;
INSERT INTO `purchaseItems` VALUES (1,1,2,1),(2,1,1,1),(2,3,2,1),(3,2,2,1),(4,1,2,NULL),(7,1,1,NULL),(7,2,1,NULL),(7,3,2,NULL),(8,1,1,NULL),(8,2,1,NULL),(8,3,1,NULL),(9,3,1,1),(10,1,1,1),(10,3,1,1),(11,1,1,1),(11,2,1,1),(11,3,1,1),(12,2,1,1),(13,1,3,1),(13,2,1,NULL),(13,3,0,NULL),(13,4,1,NULL),(14,1,1,NULL),(15,1,1,NULL),(16,1,1,NULL),(17,1,1,NULL),(18,3,1,NULL),(19,1,0,NULL),(20,1,1,NULL),(21,1,0,NULL),(21,2,0,NULL),(22,1,0,NULL),(22,4,1,NULL),(23,4,1,NULL),(24,2,1,NULL),(24,3,1,NULL),(25,2,7,NULL),(26,2,1,NULL),(27,2,1,NULL),(28,1,1,1),(28,3,1,NULL),(29,1,3,1),(29,2,2,1),(29,3,1,1),(30,1,18,1),(30,2,12,1),(30,3,78,1),(31,1,1,NULL),(32,1,0,1),(32,31,0,1),(33,1,0,1);
/*!40000 ALTER TABLE `purchaseItems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `bnum` int(10) unsigned NOT NULL DEFAULT '0',
  `name` varchar(30) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` char(60) DEFAULT NULL,
  `admin` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`bnum`),
  KEY `admin` (`admin`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`admin`) REFERENCES `distributor` (`did`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (12345678,'Wendy','wwellesley18','$2b$12$NNpS7z5HaH5XasrhpmFtXeUudRW/Hvu0PktdJLpV6lyES8xAWVE7i',NULL),(20758475,'Eliza','emcnair','$2b$12$25ez6wvA6ds8vFNynNTnxeQdDVKsioavcu9kFPltJzB6NngPDtBmu',1),(20805803,'Chloe','cblazey','$2b$12$Ih2mGsFoNSYe2hWeoqIcTOLR7q9t0NgUg6hfdM8Ecf3O1WRYwYtP.',NULL),(23456789,'Scott D Anderson','sanderson','$2b$12$XI49TDqPqFw9tjnLJQTCyOhL3O7uNmSB0SIg7CucsX3hLEdhUVrYm',NULL),(24567890,'Scott D Anderson','sampleadmin','$2b$12$kO84.cGhHeAb.3bOlkCUN.GO1CW8wnaPPciAzxqP87URdU5q6ydw.',1);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-14 14:22:53
