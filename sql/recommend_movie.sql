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