/*
 Navicat Premium Data Transfer

 Source Server         : 10.10.9.120
 Source Server Type    : MariaDB
 Source Server Version : 100400
 Source Host           : 10.10.9.120:3306
 Source Schema         : scanner

 Target Server Type    : MariaDB
 Target Server Version : 100400
 File Encoding         : 65001

 Date: 18/12/2018 14:39:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for nodes
-- ----------------------------
DROP TABLE IF EXISTS `nodes`;
CREATE TABLE `nodes`  (
  `id` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `active` int(8) NULL DEFAULT NULL,
  `ip` int(128) NULL DEFAULT NULL,
  `port` int(128) NULL DEFAULT NULL,
  `key` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `last_activetime` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for plugins
-- ----------------------------
DROP TABLE IF EXISTS `plugins`;
CREATE TABLE `plugins`  (
  `id` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `file` blob NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tasks
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks`  (
  `id` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` int(8) NULL DEFAULT NULL,
  `createtime` bigint(20) NULL DEFAULT NULL,
  `completetime` bigint(20) NULL DEFAULT NULL,
  `progress` float(32, 10) NULL DEFAULT NULL,
  `start_ip` int(128) NULL DEFAULT NULL,
  `end_ip` int(128) NULL DEFAULT NULL,
  `start_port` int(128) NULL DEFAULT NULL,
  `end_port` int(128) NULL DEFAULT NULL,
  `plugins` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `node_id` char(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `scan_result` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
