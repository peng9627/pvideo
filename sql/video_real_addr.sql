DROP TABLE IF EXISTS `video_real_addr`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_real_addr`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `url_id`      INT(11) UNSIGNED DEFAULT 0,
    `address`     VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `rel_address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;