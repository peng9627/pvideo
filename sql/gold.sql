DROP TABLE IF EXISTS `gold`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gold` (
  `id`         INT(11) PRIMARY KEY                          NOT NULL AUTO_INCREMENT UNIQUE,
  `type`       INT(11)                                      NOT NULL, /* 1.注册送 2.推荐送 3.签到 4.提卡 5.赠送下级 6.上级赠送 5.其他 */
  `source`     VARCHAR(32)                                  NOT NULL,
  `user_id`    INT(11)                                      NOT NULL,
  `gold`       DECIMAL(19, 2)                               NOT NULL,
  `total_gold` DECIMAL(19, 2)                               NOT NULL,
  `time`       INT(11) UNSIGNED                             NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
