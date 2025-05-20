CREATE DATABASE `db_video` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

use db_video;

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account`
(
    `id`             INT(11) PRIMARY KEY                     NOT NULL UNIQUE,
    `account_name`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `pwd`            VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `salt`           VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `head`           VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `nickname`       VARCHAR(12) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `sex`            INT(1) UNSIGNED  DEFAULT 0,
    `create_time`    INT(10) UNSIGNED DEFAULT 0,
    `last_time`      INT(10) UNSIGNED DEFAULT 0,
    `last_address`   VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `account_status` INT(11)          DEFAULT 0,
    `device`         VARCHAR(255)     DEFAULT NULL,
    `platform`       VARCHAR(255)     DEFAULT NULL,
    `code`           VARCHAR(4)       DEFAULT NULL UNIQUE,
    `gold`           INT(11)          DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
ALTER TABLE account
    AUTO_INCREMENT = 100000;

DROP TABLE IF EXISTS `advertisement`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `type`    INT(11) UNSIGNED                        NOT NULL,
    `pic`     VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `count`   DECIMAL(19, 0) UNSIGNED                 NOT NULL DEFAULT 0,
    `index`   INT(11) UNSIGNED                        NOT NULL DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `advertisement_clicked`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_clicked`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `ad_id`       INT(11) UNSIGNED    NOT NULL,
    `user_id`     INT(11) UNSIGNED    NOT NULL,
    `create_time` INT(10) UNSIGNED DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED             DEFAULT 0,
    `user_id`     INT(10)             NOT NULL UNIQUE,
    `parent_id`   INT(10),
    `parent_ids`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `top_id`      INT(10)             NOT NULL,
    `times`       INT(11)             NOT NULL DEFAULT 0,
    `total_times` INT(11)             NOT NULL DEFAULT 0,
    `status`      INT(1)              NOT NULL DEFAULT 0,
    `contact`     VARCHAR(255) COLLATE utf8mb4_unicode_ci
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `app_init`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_init`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `user_id`     INT(10) UNSIGNED DEFAULT 0,
    `device`      VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `platform`    VARCHAR(255)     DEFAULT NULL,
    `ip`          VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `app_version`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_version`
(
    `id`       INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `type`     INT(11)             NOT NULL, /*1.app版本 2.框架版本 3.资源版本  */
    `name`     VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `version`  INT(10) UNSIGNED                        DEFAULT 0,
    `details`  VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
    `platform` VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
    `address`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `must`     INT(11)             NOT NULL            DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history`
(
    `id`           INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`      INT(11)                      DEFAULT 0,
    `to_id`        INT(11)                      DEFAULT 0,
    `create_time`  INT(10) UNSIGNED             DEFAULT 0,
    `receive_time` INT(10) UNSIGNED             DEFAULT 0,
    `content`      VARCHAR(255)        NOT NULL COLLATE utf8mb4_unicode_ci,
    `deleted`      INT(1)              NOT NULL DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `chat_history_list`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_history_list`
(
    `id`        INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`   INT(11)          DEFAULT 0,
    `to_id`     INT(11)          DEFAULT 0,
    `last_time` INT(10) UNSIGNED DEFAULT 0,
    `unread`    INT(10) UNSIGNED DEFAULT 0,
    `content`   VARCHAR(255)        NOT NULL COLLATE utf8mb4_unicode_ci
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`     INT(11)                                          DEFAULT 0,
    `device`      VARCHAR(255)                                     DEFAULT NULL,
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

DROP TABLE IF EXISTS `gold`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gold`
(
    `id`         INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `type`       INT(11)             NOT NULL, /* 1.注册送 2.推荐送 3.签到 4.提卡 5.赠送下级 6.上级赠送 7.后台赠送 5.其他 */
    `source`     VARCHAR(32)         NOT NULL,
    `user_id`    INT(11)             NOT NULL,
    `gold`       DECIMAL(19, 2)      NOT NULL,
    `total_gold` DECIMAL(19, 2)      NOT NULL,
    `time`       INT(11) UNSIGNED    NOT NULL
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `live_url`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_url`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`    VARCHAR(10) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movie`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `type`        INT(11) UNSIGNED DEFAULT 0,/*1.电影 2.电视剧 3.动漫 4.综艺*/
    `title`       VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `span`        VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `update_time` INT(10) UNSIGNED DEFAULT 0,
    `play_count`  INT(11) UNSIGNED DEFAULT 0,
    `address`     LONGBLOB,
    `horizontal`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `vertical`    VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `actor`       VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*演员*/
    `child_type`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*子类*/
    `director`    VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*导演*/
    `region`      VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*地区*/
    `year`        VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*年份*/
    `total_part`  INT(10) UNSIGNED DEFAULT 0,/*总集*/
    `details`     BLOB,/*描述*/
    `source`      VARCHAR(255) COLLATE utf8mb4_unicode_ci/*来源*/
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `type`    INT(11) UNSIGNED                        NOT NULL,
    `title`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `content` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `play_details`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `play_details`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `video_id`    INT(11)             NOT NULL,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `play_count`  INT(11) UNSIGNED DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `recommend`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommend`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `pic`     VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `desc`    VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name`    VARCHAR(10) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `index`   INT(11) UNSIGNED                        NOT NULL DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `recommend_movie`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommend_movie`
(
    `id`    INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `ids`   VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `desc`  VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `index` INT(11) UNSIGNED                        NOT NULL DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `sign`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sign`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED             DEFAULT 0,
    `user_id`     INT(10)             NOT NULL,
    `gold`        INT(11)             NOT NULL DEFAULT 0
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `tv_url`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tv_url`
(
    `id`      INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `pic`     VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    `address` VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    `name`    VARCHAR(10) COLLATE utf8mb4_unicode_ci  NOT NULL,
    `index`   INT(11) UNSIGNED                        NOT NULL DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `video_comment`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_comment`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`     INT(11)             NOT NULL,
    `video_id`    INT(11)             NOT NULL,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `content`     VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `video_history`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_history`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_id`     INT(11)          DEFAULT 0,
    `device`      VARCHAR(64)      DEFAULT NULL COLLATE utf8mb4_unicode_ci,
    `video_id`    INT(11)             NOT NULL,
    `video_type`  INT(11)             NOT NULL,/* 1.视频, 2.影视*/
    `update_time` INT(10) UNSIGNED DEFAULT 0,
    `content`     VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `video_praise`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_praise`
(
    `id`         INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `user_video` VARCHAR(255)        NOT NULL UNIQUE
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `video_type`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_type`
(
    `id`    INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `title` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `pid`   INT(11) DEFAULT 0,
    `pic`   VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `t_account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_account`
(
    `id`                  INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `account_name`        VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `password`            VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `role_id`             INT(10) UNSIGNED DEFAULT 0,
    `salt`                VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `create_time`         INT(10) UNSIGNED DEFAULT 0,
    `last_time`           INT(10) UNSIGNED DEFAULT 0,
    `last_address`        VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `account_status`      INT(10) UNSIGNED DEFAULT 0,
    `last_login_platform` VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `goods`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `goods`
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
    `status`      INT(10) UNSIGNED                                 DEFAULT 0,
    `pay_time`    INT(10) UNSIGNED                                 DEFAULT 0,
    `pay_type`    INT(10) UNSIGNED                                 DEFAULT 0,
    `details`     VARCHAR(128) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `t_permission`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_permission`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`        VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `description` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `value`       VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `status`      INT(10) UNSIGNED DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `t_role`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_role`
(
    `id`          INT(11) PRIMARY KEY                     NOT NULL AUTO_INCREMENT UNIQUE,
    `name`        VARCHAR(128) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
    `description` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `permissions` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `status`      INT(10) UNSIGNED DEFAULT 0
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

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

INSERT INTO `account`
VALUES (10000, '130@1.com', '09ab3ef90da908aff3ce4cdd302f103f', 'ozhr4k19ts1re76nkhtpvehfxsjkd2hk', NULL, 'zz0000', 0,
        1613813625, 1617021146, '127.0.0.1', 0, NULL, '8888', 1000000);
INSERT INTO `agent`
VALUES (1, 0, 10000, NULL, '', 10000, -1, -1, 1, '');
INSERT INTO `notice`
VALUES (1, 1, '跑马灯', '欢迎来到大米影院，最新下载地址:dm1.tv，如不能正常打开app或苹果掉签，重新下载即可!'),
       (2, 2, '大米影院 dm1.tv',
        '官网dm1.tv，请各位影友保存我们最新官网，以免发生app卸载后找不到网址，如果在使用过程中遇到任何问题请及时向我们反馈!');
INSERT INTO `t_account`
VALUES (1, 'admin', 'a38c74395ec7839349284e61feb64deb', 1, 'b76bxubllbmkrbx75nxk2hcix66wan6n', 0, 1616744675,
        '127.0.0.1', 0, '');
INSERT INTO `t_role`
VALUES (1, 'admin', '管理员', 0, '', 0),
       (2, 'agent', '用于登录代理系统', 1591809860, '', 0);

