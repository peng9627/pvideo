DROP TABLE IF EXISTS `advertisement_clicked`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_clicked`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `ad_id`       INT(11) UNSIGNED    NOT NULL,
    `user_id`     INT(11) UNSIGNED    NOT NULL,
    `create_time` INT(10) UNSIGNED DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;