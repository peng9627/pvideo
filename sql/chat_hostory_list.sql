DROP TABLE IF EXISTS `chat_history_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history_list`
(
    `id`        INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`   INT(11)          DEFAULT 0,
    `to_id`     INT(11)          DEFAULT 0,
    `last_time` INT(10) UNSIGNED DEFAULT 0,
    `unread` INT(10) UNSIGNED DEFAULT 0,
    `content`   VARCHAR(255)        NOT NULL COLLATE utf8mb4_unicode_ci
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
