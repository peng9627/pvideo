DROP TABLE IF EXISTS `video_type`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_type`
(
    `id`    INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `title` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `pid`   INT(11) DEFAULT 0,
    `pic`   VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;