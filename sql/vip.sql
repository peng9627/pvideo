DROP TABLE IF EXISTS `vip`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vip`
(
    `id`                INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `account_id`        INT(11)                                 NOT NULL,
    `create_time`       INT(10) UNSIGNED DEFAULT 0,
    `start_time`        INT(10) UNSIGNED DEFAULT 0,
    `end_time`          INT(10) UNSIGNED DEFAULT 0,
    `order_no`          VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `operation_account` VARCHAR(128) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;