DROP TABLE IF EXISTS `video_praise`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_praise`
(
    `id`         INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_video` VARCHAR(255)        NOT NULL UNIQUE
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;