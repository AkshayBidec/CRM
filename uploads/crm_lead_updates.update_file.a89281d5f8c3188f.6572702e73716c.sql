-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: erp_general_db
-- ------------------------------------------------------
-- Server version	5.7.19

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
-- Current Database: `erp_general_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `erp_general_db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `erp_general_db`;

--
-- Table structure for table `auth_cas`
--

DROP TABLE IF EXISTS `auth_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_cas`
--

LOCK TABLES `auth_cas` WRITE;
/*!40000 ALTER TABLE `auth_cas` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_cas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_event`
--

DROP TABLE IF EXISTS `auth_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_membership`
--

DROP TABLE IF EXISTS `auth_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_membership`
--

LOCK TABLES `auth_membership` WRITE;
/*!40000 ALTER TABLE `auth_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_company_details`
--

DROP TABLE IF EXISTS `general_company_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_company_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(1000) NOT NULL,
  `company_identification` varchar(2000) NOT NULL,
  `company_address_line1` varchar(5000) NOT NULL,
  `country` varchar(500) NOT NULL,
  `states` varchar(500) NOT NULL,
  `city` varchar(500) NOT NULL,
  `pincode` int(11) NOT NULL,
  `office_number` int(11) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `company_address_line2` varchar(5000) DEFAULT NULL,
  `verification_code` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_company_details`
--

LOCK TABLES `general_company_details` WRITE;
/*!40000 ALTER TABLE `general_company_details` DISABLE KEYS */;
INSERT INTO `general_company_details` VALUES (25,'345345','1234567','asdfasd','afsdfd','asdfas','3fdasfcadsf',123456,2147483647,'T','2018-02-01 23:52:51',NULL,'adfa','qwe');
/*!40000 ALTER TABLE `general_company_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_master_features`
--

DROP TABLE IF EXISTS `general_master_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_master_features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `feature_name` varchar(500) NOT NULL,
  `category` varchar(500) DEFAULT NULL,
  `sub_category` varchar(500) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id__idx` (`company_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_master_features_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `general_company_details` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_master_features_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_master_features`
--

LOCK TABLES `general_master_features` WRITE;
/*!40000 ALTER TABLE `general_master_features` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_master_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_master_verification_details`
--

DROP TABLE IF EXISTS `general_master_verification_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_master_verification_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verification_code` varchar(5000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `remarks` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_master_verification_details`
--

LOCK TABLES `general_master_verification_details` WRITE;
/*!40000 ALTER TABLE `general_master_verification_details` DISABLE KEYS */;
INSERT INTO `general_master_verification_details` VALUES (1,'qwe','F','2018-02-01 20:57:45',NULL,'test'),(2,'asd','T','2018-02-01 20:57:59',NULL,'test'),(6,'zxc','T','2018-02-01 20:58:23',NULL,'test');
/*!40000 ALTER TABLE `general_master_verification_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_role`
--

DROP TABLE IF EXISTS `general_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `role_name` varchar(250) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id__idx` (`company_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_role_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `general_company_details` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_role_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_role`
--

LOCK TABLES `general_role` WRITE;
/*!40000 ALTER TABLE `general_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_role_features`
--

DROP TABLE IF EXISTS `general_role_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_role_features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `feature_id` int(11) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id__idx` (`role_id`),
  KEY `feature_id__idx` (`feature_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_role_features_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `general_role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_role_features_ibfk_2` FOREIGN KEY (`feature_id`) REFERENCES `general_master_features` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_role_features_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_role_features`
--

LOCK TABLES `general_role_features` WRITE;
/*!40000 ALTER TABLE `general_role_features` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_role_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_role_hrchy`
--

DROP TABLE IF EXISTS `general_role_hrchy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_role_hrchy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `upper_role_id` int(11) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id__idx` (`role_id`),
  KEY `upper_role_id__idx` (`upper_role_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_role_hrchy_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `general_role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_role_hrchy_ibfk_2` FOREIGN KEY (`upper_role_id`) REFERENCES `general_role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_role_hrchy_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_role_hrchy`
--

LOCK TABLES `general_role_hrchy` WRITE;
/*!40000 ALTER TABLE `general_role_hrchy` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_role_hrchy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_session`
--

DROP TABLE IF EXISTS `general_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_type` varchar(250) NOT NULL,
  `login_time` datetime DEFAULT NULL,
  `logout_time` datetime DEFAULT NULL,
  `duration` varchar(200) DEFAULT NULL,
  `ip_address` varchar(500) NOT NULL,
  `locations` varchar(500) DEFAULT NULL,
  `mac_address` varchar(500) DEFAULT NULL,
  `is_active` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_session`
--

LOCK TABLES `general_session` WRITE;
/*!40000 ALTER TABLE `general_session` DISABLE KEYS */;
INSERT INTO `general_session` VALUES (19,2,'super_admin','2018-02-06 15:36:38','2018-02-06 15:36:44','0M 0D 0h 0m 6s ','127.0.0.1',NULL,NULL,0),(20,2,'super_admin','2018-02-06 16:26:10','2018-02-06 16:55:44','0M 4D 14h 37m 6s **','127.0.0.1',NULL,NULL,0),(21,2,'super_admin','2018-02-06 16:56:02','2018-02-06 16:58:20','0M 4D 14h 39m 42s **','127.0.0.1',NULL,NULL,0),(22,2,'super_admin','2018-02-06 16:58:26','2018-02-06 16:59:50','0M 4D 14h 41m 12s **','127.0.0.1',NULL,NULL,0),(23,2,'super_admin','2018-02-06 16:59:56','2018-02-06 17:00:02','0M 0D 0h 0m 6s ','127.0.0.1',NULL,NULL,0),(24,2,'super_admin','2018-02-06 17:01:05','2018-02-06 18:27:30','0M 0D 1h 26m 24s ','127.0.0.1',NULL,NULL,0),(25,2,'super_admin','2018-02-06 18:27:38','2018-02-06 18:34:33','0M 0D 0h 6m 55s ','127.0.0.1',NULL,NULL,0),(26,2,'super_admin','2018-02-06 18:38:14','2018-02-06 19:08:38','0M 0D 0h 30m 24s ','127.0.0.1',NULL,NULL,0),(27,2,'super_admin','2018-02-06 19:35:04',NULL,NULL,'127.0.0.1',NULL,NULL,1);
/*!40000 ALTER TABLE `general_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_superadmin_details`
--

DROP TABLE IF EXISTS `general_superadmin_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_superadmin_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `first_name` varchar(250) NOT NULL,
  `last_name` varchar(250) DEFAULT NULL,
  `email_id` varchar(500) NOT NULL,
  `mobile_number` int(11) NOT NULL,
  `password` varchar(512) NOT NULL,
  `temp_password` varchar(512) DEFAULT NULL,
  `verification_code` varchar(5000) NOT NULL,
  `forgot_password_verification` varchar(2000) DEFAULT NULL,
  `ip_address` varchar(500) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `no_login_attempts` int(11) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `last_logout_time` datetime DEFAULT NULL,
  `mac_address` varchar(500) DEFAULT NULL,
  `locations` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id__idx` (`company_id`),
  CONSTRAINT `general_superadmin_details_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `general_company_details` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_superadmin_details`
--

LOCK TABLES `general_superadmin_details` WRITE;
/*!40000 ALTER TABLE `general_superadmin_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_superadmin_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_user`
--

DROP TABLE IF EXISTS `general_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `first_name` varchar(250) NOT NULL,
  `last_name` varchar(250) DEFAULT NULL,
  `email_id` varchar(500) NOT NULL,
  `mobile_number` int(11) NOT NULL,
  `password` varchar(512) NOT NULL,
  `temp_password` varchar(512) DEFAULT NULL,
  `forgot_password_verification` varchar(2000) DEFAULT NULL,
  `ip_address` varchar(500) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `no_login_attempts` int(11) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `last_logout_time` datetime DEFAULT NULL,
  `is_superadmin` int(11) NOT NULL,
  `mac_address` varchar(500) DEFAULT NULL,
  `locations` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_id` (`email_id`),
  KEY `company_id__idx` (`company_id`),
  CONSTRAINT `general_user_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `general_company_details` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_user`
--

LOCK TABLES `general_user` WRITE;
/*!40000 ALTER TABLE `general_user` DISABLE KEYS */;
INSERT INTO `general_user` VALUES (2,25,'nitidh','namw','name@name.com',2147483647,'1',NULL,NULL,'127.0.0.1','T','2018-02-01 23:52:51',NULL,0,'2018-02-02 02:18:38','2018-02-06 19:08:38',1,NULL,NULL);
/*!40000 ALTER TABLE `general_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_user_features`
--

DROP TABLE IF EXISTS `general_user_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_user_features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `feature_id` int(11) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `feature_id__idx` (`feature_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_user_features_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `general_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_user_features_ibfk_2` FOREIGN KEY (`feature_id`) REFERENCES `general_master_features` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_user_features_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_user_features`
--

LOCK TABLES `general_user_features` WRITE;
/*!40000 ALTER TABLE `general_user_features` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_user_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general_user_role`
--

DROP TABLE IF EXISTS `general_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `general_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `role_id__idx` (`role_id`),
  KEY `session_id__idx` (`session_id`),
  CONSTRAINT `general_user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `general_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `general_role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `general_user_role_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `general_session` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_user_role`
--

LOCK TABLES `general_user_role` WRITE;
/*!40000 ALTER TABLE `general_user_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `general_user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `erp_crm_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `erp_crm_db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `erp_crm_db`;

--
-- Table structure for table `auth_cas`
--

DROP TABLE IF EXISTS `auth_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_cas`
--

LOCK TABLES `auth_cas` WRITE;
/*!40000 ALTER TABLE `auth_cas` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_cas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_event`
--

DROP TABLE IF EXISTS `auth_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_membership`
--

DROP TABLE IF EXISTS `auth_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_membership`
--

LOCK TABLES `auth_membership` WRITE;
/*!40000 ALTER TABLE `auth_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_audit_trail`
--

DROP TABLE IF EXISTS `crm_audit_trail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_audit_trail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table_name` varchar(500) NOT NULL,
  `audit_datetime` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `function_operation` varchar(500) NOT NULL,
  `instance_key` varchar(500) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_audit_trail`
--

LOCK TABLES `crm_audit_trail` WRITE;
/*!40000 ALTER TABLE `crm_audit_trail` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_audit_trail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_audit_trail_value`
--

DROP TABLE IF EXISTS `crm_audit_trail_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_audit_trail_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `audit_trail_id` int(11) DEFAULT NULL,
  `col_name` varchar(500) NOT NULL,
  `old_value` varchar(1000) NOT NULL,
  `new_value` varchar(1000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `audit_trail_id__idx` (`audit_trail_id`),
  CONSTRAINT `crm_audit_trail_value_ibfk_1` FOREIGN KEY (`audit_trail_id`) REFERENCES `crm_audit_trail` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_audit_trail_value`
--

LOCK TABLES `crm_audit_trail_value` WRITE;
/*!40000 ALTER TABLE `crm_audit_trail_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_audit_trail_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_campaign_field`
--

DROP TABLE IF EXISTS `crm_campaign_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_campaign_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_id` int(11) NOT NULL,
  `form_name` varchar(250) NOT NULL,
  `field_name` varchar(500) DEFAULT NULL,
  `field_type_id` int(11) DEFAULT NULL,
  `field_values` varchar(250) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `field_type_id__idx` (`field_type_id`),
  CONSTRAINT `crm_campaign_field_ibfk_1` FOREIGN KEY (`field_type_id`) REFERENCES `crm_master_field_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_campaign_field`
--

LOCK TABLES `crm_campaign_field` WRITE;
/*!40000 ALTER TABLE `crm_campaign_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_campaign_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_campaign_field_value`
--

DROP TABLE IF EXISTS `crm_campaign_field_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_campaign_field_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `field_value` varchar(1000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id__idx` (`field_id`),
  CONSTRAINT `crm_campaign_field_value_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `crm_campaign_field` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_campaign_field_value`
--

LOCK TABLES `crm_campaign_field_value` WRITE;
/*!40000 ALTER TABLE `crm_campaign_field_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_campaign_field_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_customer_details`
--

DROP TABLE IF EXISTS `crm_customer_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_customer_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_type` int(11) DEFAULT NULL,
  `first_name` varchar(250) NOT NULL,
  `last_name` varchar(250) DEFAULT NULL,
  `email_id` varchar(500) NOT NULL,
  `mobile_number` int(11) NOT NULL,
  `firm_name` varchar(500) NOT NULL,
  `designation` varchar(250) DEFAULT NULL,
  `firm_address` varchar(1000) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_type__idx` (`customer_type`),
  CONSTRAINT `crm_customer_details_ibfk_1` FOREIGN KEY (`customer_type`) REFERENCES `crm_customer_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_customer_details`
--

LOCK TABLES `crm_customer_details` WRITE;
/*!40000 ALTER TABLE `crm_customer_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_customer_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_customer_type`
--

DROP TABLE IF EXISTS `crm_customer_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_customer_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_type` varchar(250) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_customer_type`
--

LOCK TABLES `crm_customer_type` WRITE;
/*!40000 ALTER TABLE `crm_customer_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_customer_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_deal_field`
--

DROP TABLE IF EXISTS `crm_deal_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_deal_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_id` int(11) NOT NULL,
  `form_name` varchar(250) NOT NULL,
  `field_name` varchar(500) DEFAULT NULL,
  `field_type_id` int(11) DEFAULT NULL,
  `field_values` varchar(250) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `field_type_id__idx` (`field_type_id`),
  CONSTRAINT `crm_deal_field_ibfk_1` FOREIGN KEY (`field_type_id`) REFERENCES `crm_master_field_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_deal_field`
--

LOCK TABLES `crm_deal_field` WRITE;
/*!40000 ALTER TABLE `crm_deal_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_deal_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_deal_field_value`
--

DROP TABLE IF EXISTS `crm_deal_field_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_deal_field_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `field_value` varchar(1000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id__idx` (`field_id`),
  CONSTRAINT `crm_deal_field_value_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `crm_deal_field` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_deal_field_value`
--

LOCK TABLES `crm_deal_field_value` WRITE;
/*!40000 ALTER TABLE `crm_deal_field_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_deal_field_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_events_field`
--

DROP TABLE IF EXISTS `crm_events_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_events_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_id` int(11) NOT NULL,
  `form_name` varchar(250) NOT NULL,
  `field_name` varchar(500) DEFAULT NULL,
  `field_type_id` int(11) DEFAULT NULL,
  `field_values` varchar(250) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `field_type_id__idx` (`field_type_id`),
  CONSTRAINT `crm_events_field_ibfk_1` FOREIGN KEY (`field_type_id`) REFERENCES `crm_master_field_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_events_field`
--

LOCK TABLES `crm_events_field` WRITE;
/*!40000 ALTER TABLE `crm_events_field` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_events_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_events_field_value`
--

DROP TABLE IF EXISTS `crm_events_field_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_events_field_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `field_value` varchar(1000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id__idx` (`field_id`),
  CONSTRAINT `crm_events_field_value_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `crm_events_field` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_events_field_value`
--

LOCK TABLES `crm_events_field_value` WRITE;
/*!40000 ALTER TABLE `crm_events_field_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_events_field_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_lead_field`
--

DROP TABLE IF EXISTS `crm_lead_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_lead_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_id` int(11) NOT NULL,
  `form_name` varchar(250) NOT NULL,
  `field_name` varchar(500) DEFAULT NULL,
  `field_type_id` int(11) DEFAULT NULL,
  `field_values` varchar(250) DEFAULT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `field_type_id__idx` (`field_type_id`),
  CONSTRAINT `crm_lead_field_ibfk_1` FOREIGN KEY (`field_type_id`) REFERENCES `crm_master_field_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_lead_field`
--

LOCK TABLES `crm_lead_field` WRITE;
/*!40000 ALTER TABLE `crm_lead_field` DISABLE KEYS */;
INSERT INTO `crm_lead_field` VALUES (1,1,'leads_add','Company',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(2,1,'leads_add','Lead_Owner',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(3,1,'leads_add','First_Name',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(4,1,'leads_add','Last_Name',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(5,1,'leads_add','Title',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(6,1,'leads_add','Email_ID',1,'email','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(7,1,'leads_add','Phone',1,'int','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(8,1,'leads_add','Fax',1,'int','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(9,1,'leads_add','Mobile',1,'int','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(10,1,'leads_add','Website',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(11,1,'leads_add','Lead_Source',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(12,1,'leads_add','Lead_Status',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(13,1,'leads_add','Street',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(14,1,'leads_add','City',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(15,1,'leads_add','State',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(16,1,'leads_add','Pincode',1,'int','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(17,1,'leads_add','Country',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25),(18,1,'leads_add','Description',1,'string','T','2018-02-05 16:26:49',NULL,NULL,NULL,25);
/*!40000 ALTER TABLE `crm_lead_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_lead_field_value`
--

DROP TABLE IF EXISTS `crm_lead_field_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_lead_field_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `field_value` varchar(1000) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `field_id__idx` (`field_id`),
  CONSTRAINT `crm_lead_field_value_ibfk_1` FOREIGN KEY (`field_id`) REFERENCES `crm_lead_field` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_lead_field_value`
--

LOCK TABLES `crm_lead_field_value` WRITE;
/*!40000 ALTER TABLE `crm_lead_field_value` DISABLE KEYS */;
INSERT INTO `crm_lead_field_value` VALUES (22,1,0,'bidec','T','2018-02-05 20:19:30',NULL,NULL,NULL),(23,2,0,'priyesh','T','2018-02-05 20:19:30',NULL,NULL,NULL),(24,3,0,'priyesh','T','2018-02-05 20:19:30',NULL,NULL,NULL),(25,4,0,'ji','T','2018-02-05 20:19:31',NULL,NULL,NULL),(26,5,0,'sherma','T','2018-02-05 20:19:31',NULL,NULL,NULL),(27,6,0,'priyesh@bidec.xyz','T','2018-02-05 20:19:31',NULL,NULL,NULL),(28,7,0,'9999999999','T','2018-02-05 20:19:31',NULL,NULL,NULL),(29,8,0,'','T','2018-02-05 20:19:31',NULL,NULL,NULL),(30,9,0,'','T','2018-02-05 20:19:31',NULL,NULL,NULL),(31,10,0,'','T','2018-02-05 20:19:31',NULL,NULL,NULL),(32,11,0,'himself','T','2018-02-05 20:19:31',NULL,NULL,NULL),(33,12,0,'done','T','2018-02-05 20:19:31',NULL,NULL,NULL),(34,13,0,'ghar ','T','2018-02-05 20:19:31',NULL,NULL,NULL),(35,14,0,'ke ','T','2018-02-05 20:19:31',NULL,NULL,NULL),(36,15,0,'peeche','T','2018-02-05 20:19:31',NULL,NULL,NULL),(37,16,0,'000000','T','2018-02-05 20:19:31',NULL,NULL,NULL),(38,17,0,'pakistan','T','2018-02-05 20:19:31',NULL,NULL,NULL),(39,18,0,'done','T','2018-02-05 20:19:31',NULL,NULL,NULL),(40,1,0,'bidec','T','2018-02-05 20:27:19',NULL,NULL,NULL),(41,2,0,'priyesh','T','2018-02-05 20:27:19',NULL,NULL,NULL),(42,3,0,'priyesh','T','2018-02-05 20:27:19',NULL,NULL,NULL),(43,4,0,'ji','T','2018-02-05 20:27:19',NULL,NULL,NULL),(44,5,0,'sherma','T','2018-02-05 20:27:19',NULL,NULL,NULL),(45,6,0,'priyesh@bidec.xyz','T','2018-02-05 20:27:19',NULL,NULL,NULL),(46,7,0,'9999999999','T','2018-02-05 20:27:19',NULL,NULL,NULL),(47,8,0,'ihiuh','T','2018-02-05 20:27:19',NULL,NULL,NULL),(48,9,0,'0000000000','T','2018-02-05 20:27:19',NULL,NULL,NULL),(49,10,0,'bidec.xyz','T','2018-02-05 20:27:19',NULL,NULL,NULL),(50,11,0,'himself','T','2018-02-05 20:27:19',NULL,NULL,NULL),(51,12,0,'done','T','2018-02-05 20:27:19',NULL,NULL,NULL),(52,13,0,'ghar','T','2018-02-05 20:27:19',NULL,NULL,NULL),(53,14,0,'ke','T','2018-02-05 20:27:19',NULL,NULL,NULL),(54,15,0,'peeche','T','2018-02-05 20:27:19',NULL,NULL,NULL),(55,16,0,'000000','T','2018-02-05 20:27:19',NULL,NULL,NULL),(56,17,0,'pakistan','T','2018-02-05 20:27:19',NULL,NULL,NULL),(57,18,0,'done','T','2018-02-05 20:27:19',NULL,NULL,NULL);
/*!40000 ALTER TABLE `crm_lead_field_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_lead_status`
--

DROP TABLE IF EXISTS `crm_lead_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_lead_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lead_status` varchar(250) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_lead_status`
--

LOCK TABLES `crm_lead_status` WRITE;
/*!40000 ALTER TABLE `crm_lead_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `crm_lead_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `crm_master_field_type`
--

DROP TABLE IF EXISTS `crm_master_field_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_master_field_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_type_name` varchar(250) NOT NULL,
  `is_active` char(1) NOT NULL DEFAULT 'T',
  `db_entry_time` datetime NOT NULL,
  `db_entered_by` int(11) DEFAULT NULL,
  `db_update_time` datetime DEFAULT NULL,
  `db_updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_master_field_type`
--

LOCK TABLES `crm_master_field_type` WRITE;
/*!40000 ALTER TABLE `crm_master_field_type` DISABLE KEYS */;
INSERT INTO `crm_master_field_type` VALUES (1,'company_name','T','2018-02-05 13:35:57',NULL,NULL,NULL,25);
/*!40000 ALTER TABLE `crm_master_field_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-07 12:24:51
