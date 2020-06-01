DROP TABLE IF EXISTS `app_version`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_version`
(
    `id`       INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `type`     INT(11)             NOT NULL, /*1.app版本 2.框架版本 3.资源版本  */
    `name`     VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `version`  INT(10) UNSIGNED                        DEFAULT 0,
    `details`  VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
    `platform` VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
    `address`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `must`     INT(11)             NOT NULL            DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;