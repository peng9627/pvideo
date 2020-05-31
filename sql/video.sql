DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `type`        INT(11)             NOT NULL,
    `title`       VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `play_count`  INT(11) UNSIGNED DEFAULT 0,
    `address`     VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `horizontal`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `vertical`    VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;