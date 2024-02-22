DROP TABLE IF EXISTS `recharge_config`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recharge_config`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`        VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `create_time` INT(10) UNSIGNED                                 DEFAULT 0,
    `amount`      DECIMAL(10, 2)                          NOT NULL DEFAULT 0,
    `status`      INT(10) UNSIGNED                                 DEFAULT 0,
    `vip_days`    INT(10) UNSIGNED                                 DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;