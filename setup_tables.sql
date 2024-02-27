CREATE TABLE IF NOT EXISTS `library`(
    `id` VARCHAR(60) NOT NULL,
    `name` VARCHAR(35) NOT NULL,
    `user_id` VARCHAR(60) NOT NULL
);
ALTER TABLE
    `library` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `resource`(
    `id` VARCHAR(60) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `type` VARCHAR(255) NOT NULL,
    `content` MULTILINESTRING NOT NULL,
    `rack_id` VARCHAR(60) NOT NULL,
    `public` TINYINT(1) NOT NULL
);
ALTER TABLE
    `resource` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `rack`(
    `id` VARCHAR(60) NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `library_id` VARCHAR(60) NOT NULL
);
ALTER TABLE
    `rack` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `review`(
    `id` VARCHAR(60) NOT NULL,
    `user_id` VARCHAR(60) NOT NULL,
    `content_id` VARCHAR(60) NOT NULL,
    `text` LINESTRING NOT NULL
);
ALTER TABLE
    `review` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `recommendation`(
    `id` VARCHAR(60) NOT NULL,
    `Title` VARCHAR(255) NOT NULL,
    `text` VARCHAR(255) NOT NULL,
    `resource_id` VARCHAR(60) NOT NULL,
    `user_id` VARCHAR(60) NOT NULL
);
ALTER TABLE
    `recommendation` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `sub_rack`(
    `id` VARCHAR(60) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `rack_id` VARCHAR(60) NOT NULL,
    `resource_id` VARCHAR(60) NOT NULL,
    `description` LINESTRING NOT NULL
);
ALTER TABLE
    `sub_rack` ADD PRIMARY KEY(`id`);
CREATE TABLE IF NOT EXISTS `user`(
    `id` VARCHAR(60) NOT NULL,
    `firstname` VARCHAR(35) NOT NULL,
    `lastname` VARCHAR(35) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(35) NOT NULL,
    `username` VARCHAR(35) NOT NULL
);
ALTER TABLE
    `user` ADD PRIMARY KEY(`id`);
ALTER TABLE
    `sub_rack` ADD CONSTRAINT `sub_rack_rack_id_foreign` FOREIGN KEY(`rack_id`) REFERENCES `rack`(`id`);
ALTER TABLE
    `review` ADD CONSTRAINT `review_content_id_foreign` FOREIGN KEY(`content_id`) REFERENCES `resource`(`id`);
ALTER TABLE
    `resource` ADD CONSTRAINT `resource_rack_id_foreign` FOREIGN KEY(`rack_id`) REFERENCES `sub_rack`(`id`);
ALTER TABLE
    `review` ADD CONSTRAINT `review_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `user`(`id`);
ALTER TABLE
    `recommendation` ADD CONSTRAINT `recommendation_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `user`(`id`);
ALTER TABLE
    `rack` ADD CONSTRAINT `rack_library_id_foreign` FOREIGN KEY(`library_id`) REFERENCES `library`(`id`);
ALTER TABLE
    `recommendation` ADD CONSTRAINT `recommendation_resource_id_foreign` FOREIGN KEY(`resource_id`) REFERENCES `resource`(`id`);
ALTER TABLE
    `resource` ADD CONSTRAINT `resource_rack_id_foreign` FOREIGN KEY(`rack_id`) REFERENCES `rack`(`id`);
ALTER TABLE
    `library` ADD CONSTRAINT `library_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `user`(`id`);
