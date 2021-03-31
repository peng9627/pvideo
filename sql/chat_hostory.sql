DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history`
(
    `id`           INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`      INT(11)          DEFAULT 0,
    `to_id`        INT(11)          DEFAULT 0,
    `create_time`  INT(10) UNSIGNED DEFAULT 0,
    `receive_time` INT(10) UNSIGNED DEFAULT 0,
    `content`      VARCHAR(255)        NOT NULL COLLATE utf8mb4_unicode_ci,
    `deleted`     INT(1)             NOT NULL            DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
