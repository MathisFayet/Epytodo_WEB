CREATE DATABASE IF NOT EXISTS `epytodo`;
USE `epytodo`;

CREATE TABLE IF NOT EXISTS `user` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`user_id`)
);

CREATE TABLE IF NOT EXISTS `task` (
    `task_id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `begin` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `end` datetime DEFAULT NULL,
    `status` enum('not started', 'in progress', 'done') NOT NULL DEFAULT 'not started',
    PRIMARY KEY (`task_id`)
);

CREATE TABLE IF NOT EXISTS `user_has_task` (
    `fk_user_id` int(11) NOT NULL,
    `fk_task_id` int(11) NOT NULL
);