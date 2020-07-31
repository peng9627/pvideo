DROP TABLE IF EXISTS `video_history`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_history`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`     INT(11)             NOT NULL,
    `video_id`    INT(11)             NOT NULL,
    `video_type`  INT(11)             NOT NULL,/* 1.视频, 2.影视*/
    `update_time` INT(10) UNSIGNED DEFAULT 0,
    `content`     VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;
