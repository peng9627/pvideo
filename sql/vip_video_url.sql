DROP TABLE IF EXISTS `vip_video_url`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vip_video_url`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`    VARCHAR(10) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `index`   INT(11) UNSIGNED                        NOT NULL DEFAULT 0,
    `ping`    INT(11) UNSIGNED                        NOT NULL DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;