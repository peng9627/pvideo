DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`     INT(11)                                          DEFAULT 0,
    `title`       VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `content`     VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `reply`       VARCHAR(128) COLLATE utf8mb4_unicode_ci,
    `status`      INT(1)                                  NOT NULL DEFAULT 0,
    `create_time` INT(10) UNSIGNED                                 DEFAULT 0,
    `reply_time`  INT(10) UNSIGNED                                 DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;