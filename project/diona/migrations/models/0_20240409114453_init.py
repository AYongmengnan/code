from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `animes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '动漫ID',
    `title` VARCHAR(255) NOT NULL  COMMENT '标题',
    `description` LONGTEXT   COMMENT '描述',
    `cover_image` VARCHAR(255)   COMMENT '封面图片',
    `rating` DOUBLE   COMMENT '评分',
    `release_date` DATE   COMMENT '发布日期',
    `genre` VARCHAR(100)   COMMENT '类型',
    `studio` VARCHAR(100)   COMMENT '制作公司',
    `director` VARCHAR(100)   COMMENT '导演',
    `characters` LONGTEXT   COMMENT '人物角色',
    `status` VARCHAR(50)   COMMENT '播放状态',
    `episodes` INT NOT NULL  COMMENT '集数',
    `source` VARCHAR(100)   COMMENT '来源',
    `watch_link` VARCHAR(255)   COMMENT '观看链接',
    `tags` LONGTEXT   COMMENT '标签'
) CHARACTER SET utf8mb4 COMMENT='动漫表';
CREATE TABLE IF NOT EXISTS `anime_videos` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL  COMMENT '视频文件名',
    `file_path` VARCHAR(255) NOT NULL  COMMENT '视频存放路径',
    `episode` INT NOT NULL  COMMENT '第几集',
    `anime_id` INT NOT NULL COMMENT '动漫id',
    CONSTRAINT `fk_anime_vi_animes_45fa1605` FOREIGN KEY (`anime_id`) REFERENCES `animes` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL  COMMENT '姓名',
    `email` VARCHAR(20) NOT NULL  COMMENT '电子邮件',
    `phone` VARCHAR(20) NOT NULL  COMMENT '电话号码',
    `password` VARCHAR(200) NOT NULL  COMMENT '密码'
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
