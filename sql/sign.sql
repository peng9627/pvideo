DROP TABLE IF EXISTS `sign`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sign`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED             DEFAULT 0,
    `user_id`     INT(10)             NOT NULL,
    `gold`        INT(11)             NOT NULL DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;