DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account`
(
    `id`             INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `account_name`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `pwd`            VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `salt`           VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `head`           VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `nickname`       VARCHAR(12) COLLATE utf8mb4_unicode_ci   NOT NULL,
    `sex`            INT(1) UNSIGNED  DEFAULT 0,
    `create_time`    INT(10) UNSIGNED DEFAULT 0,
    `last_time`      INT(10) UNSIGNED DEFAULT 0,
    `last_address`   VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `account_status` INT(11)          DEFAULT 0,
    `device`         VARCHAR(255)     DEFAULT NULL UNIQUE,
    `code`           VARCHAR(4)       DEFAULT NULL UNIQUE,
    `gold`           INT(11)          DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;
ALTER TABLE account
    AUTO_INCREMENT = 100000;