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
    `actor`       VARCHAR(1024) COLLATE utf8mb4_unicode_ci,/*演员*/
    `child_type`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*子类*/
    `director`    VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*导演*/
    `region`      VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*地区*/
    `year`        VARCHAR(255) COLLATE utf8mb4_unicode_ci,/*年份*/
    `total_part`  INT(10) UNSIGNED DEFAULT 0,/*总集*/
    `details`     BLOB,/*描述*/
    `source`      VARCHAR(255) COLLATE utf8mb4_unicode_ci/*来源*/
) ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;