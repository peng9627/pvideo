DROP TABLE IF EXISTS `advertisement`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `type`    INT(11) UNSIGNED                        NOT NULL,
    `pic`     VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `count`   DECIMAL(19, 0) UNSIGNED                 NOT NULL DEFAULT 0,
    `index`   INT(11) UNSIGNED                        NOT NULL DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;