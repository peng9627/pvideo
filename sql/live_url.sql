DROP TABLE IF EXISTS `live_url`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_url`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`    VARCHAR(10) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;