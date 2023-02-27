DROP TABLE IF EXISTS `t_order`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_order`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `order_no`    VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
    `create_time` INT(10) UNSIGNED                                 DEFAULT 0,
    `account_id`  INT(11)                                 NOT NULL,
    `amount`      DECIMAL(10, 2)                          NOT NULL DEFAULT 0,
    `goods_id`    INT(11)                                 NOT NULL DEFAULT 0,
    `status`      INT(10) UNSIGNED                                 DEFAULT 0,/* 0.创建 1.已支付 2.已使用 */
    `pay_time`    INT(10) UNSIGNED                                 DEFAULT 0,
    `pay_type`    INT(10) UNSIGNED                                 DEFAULT 0,
    `details`     VARCHAR(128) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;