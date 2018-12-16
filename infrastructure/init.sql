/*
 Navicat Premium Data Transfer

 Source Server         : sqlite
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 12/12/2018 11:34:30
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for nodes
-- ----------------------------
CREATE TABLE IF NOT EXISTS "nodes" (
  "id" text NOT NULL,
  "name" text,
  "active" integer ,
  "ip" integer,
  "port" integer,
  "key" text,
  "last_activetime" integer,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for plugins
-- ----------------------------
CREATE TABLE IF NOT EXISTS "plugins" (
  "id" text NOT NULL,
  "name" TEXT,
  "description" TEXT,
  "file" blob,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for tasks
-- ----------------------------
CREATE TABLE IF NOT EXISTS "tasks" (
  "id" text NOT NULL,
  "name" TEXT,
  "status" integer,
  "createtime" integer,
  "completetime" integer,
  "progress" real,
  "start_ip" integer,
  "end_ip" integer,
  "plugins" text,
  "node_id" TEXT,
  "scan_result" TEXT,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
