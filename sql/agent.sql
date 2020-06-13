DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent`
(
    `id`          INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    `create_time` INT(10) UNSIGNED DEFAULT 0,
    `user_id`     INT(10)             NOT NULL UNIQUE,
    `parent_id`   INT(10),
    `parent_ids`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `top_id`      INT(10)             NOT NULL,
    `min`         INT(11)             NOT NULL DEFAULT 0,
    `total_min`   INT(11)             NOT NULL DEFAULT 0,
    `status`      INT(1)              NOT NULL DEFAULT 0,
    `contact`     VARCHAR(255) COLLATE utf8mb4_unicode_ci
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;