CREATE TABLE `brand_category` (
  `brand_id` int NOT NULL,
  `brand_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`brand_id`)
) 
CREATE TABLE `health_category` (
  `status_id` int NOT NULL,
  `status_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) 
CREATE TABLE `zip_code` (
  `zip_code` varchar(20) NOT NULL,
  `median_age` int NOT NULL,
  `median_income` int NOT NULL,
  `population` int NOT NULL,
  `state` varchar(20) NOT NULL,
  PRIMARY KEY (`zip_code`),
  CONSTRAINT `zip_code_ibfk_1` FOREIGN KEY (`zip_code`) REFERENCES `hospital` (`zip_code`)
) 
CREATE TABLE `hospital` (
  `hospital_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `capacity` int NOT NULL,
  `staff_num` int NOT NULL,
  `zip_code` varchar(20) NOT NULL,
  PRIMARY KEY (`hospital_id`),
  KEY `hospital_ibfk_1_idx` (`zip_code`)
) 
CREATE TABLE `test` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `test_date` date NOT NULL,
  `result` int NOT NULL,
  `brand_id` int NOT NULL,
  PRIMARY KEY (`test_id`),
  KEY `test_ibfk_1_idx` (`brand_id`),
  KEY `test_ibfk_2_idx` (`patient_id`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brand_category` (`brand_id`),
  CONSTRAINT `test_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`patient_id`) ON DELETE CASCADE
) 
CREATE TABLE `patient` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `hospital_id` int DEFAULT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `age` int NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`patient_id`),
  KEY `patient_ibfk_1_idx` (`hospital_id`),
  KEY `patient_ibfk_3_idx` (`status`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`hospital_id`),
  CONSTRAINT `patient_ibfk_3` FOREIGN KEY (`status`) REFERENCES `health_category` (`status_id`)
) 
