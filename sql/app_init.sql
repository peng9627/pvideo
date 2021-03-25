DROP TABLE IF EXISTS `app_init`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_init`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `user_id`     INT(10) UNSIGNED DEFAULT 0,
    `device`      VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `ip`          VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;