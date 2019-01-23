-- phpMyAdmin SQL Dump 
-- version 3.1.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 03. Februar 2009 um 14:12
-- Server Version: 5.1.30
-- PHP-Version: 5.2.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Datenbank: `ccb2008`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `forum_forum`
--

DROP TABLE IF EXISTS `forum_forum`;
CREATE TABLE `forum_forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_rte` tinyint(1) NOT NULL,
  `creation_date` datetime NOT NULL,
  `modified_date` datetime DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `modifier_id` int(11) DEFAULT NULL,
  `sort_order` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `path` varchar(8192) DEFAULT NULL,
  `container_id` int(11) NOT NULL,
  `title` varchar(512) NOT NULL,
  `short_title` varchar(32) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_forum_creator_id` (`creator_id`),
  KEY `forum_forum_modifier_id` (`modifier_id`),
  KEY `forum_forum_parent_id` (`parent_id`),
  KEY `forum_forum_container_id` (`container_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=65 ;

--
-- Daten für Tabelle `forum_forum`
--

INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(34, 1, '2009-02-03 10:50:57', '2009-02-03 12:38:37', 1, 1, 9, 32, '000001_800003/27_800004/30_800005/32_800009/', 1, 'Mail, Contacts and Calendar', 'Mail, Contacts and Calendar', 'mail_contacts_and_calendar', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(32, 1, '2009-02-03 10:50:04', '2009-02-03 12:38:37', 1, 1, 5, 30, '000001_800003/27_800004/30_800005/', 1, 'Using iPhone', 'Using iPhone', 'using_iphone', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(33, 1, '2009-02-03 10:50:21', '2009-02-03 12:38:37', 1, 1, 8, 32, '000001_800003/27_800004/30_800005/32_800008/', 1, 'Music and Video', 'Music and Video', 'music_and_video', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(59, 1, '2009-02-03 12:35:55', '2009-02-03 12:38:37', 1, 1, 6, 32, '000001_800003/27_800004/30_800005/32_800006/', 1, 'Phone', 'Phone', 'phone', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(30, 1, '2009-02-03 10:46:14', '2009-02-03 12:38:37', 1, 1, 4, 27, '000001_800003/27_800004/', 1, 'iPhone', 'iPhone', 'iphone_2', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(27, 1, '2009-02-03 10:45:00', '2009-02-03 12:38:36', 1, 1, 3, NULL, '000001_800003/', 1, 'iPhone', 'iPhone', 'iphone', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(28, 1, '2009-02-03 10:45:27', '2009-02-03 12:38:37', 1, 1, 22, NULL, '000001_800016/', 1, 'iWork', 'iWork', 'iwork', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(35, 1, '2009-02-03 10:51:18', '2009-02-03 12:38:37', 1, 1, 10, 32, '000001_800003/27_800004/30_800005/32_80000a/', 1, 'Internet and Networking', 'Internet and Networking', 'internet_and_networking', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(36, 1, '2009-02-03 10:51:39', '2009-02-03 12:38:37', 1, 1, 11, 32, '000001_800003/27_800004/30_800005/32_80000b/', 1, 'Camera and Photos', 'Camera and Photos', 'camera_and_photos', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(37, 1, '2009-02-03 10:52:01', '2009-02-03 12:38:37', 1, 1, 12, 32, '000001_800003/27_800004/30_800005/32_80000c/', 1, 'Installing and Using iPhone Applications ', 'Installing and Using iPhone', 'installing_and_using_iphone_applications', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(38, 1, '2009-02-03 10:52:25', '2009-02-03 12:38:37', 1, 1, 13, 32, '000001_800003/27_800004/30_800005/32_80000d/', 1, 'Integrating iPhone into your Digital Life ', 'Integrating iPhone into your', 'integrating_iphone_into_your_digital_life', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(39, 1, '2009-02-03 12:14:14', '2009-02-03 12:38:37', 1, 1, 14, 30, '000001_800003/27_800004/30_80000e/', 1, 'iPhone Hardware ', 'iPhone Hardware ', 'iphone_hardware', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(40, 1, '2009-02-03 12:14:40', '2009-02-03 12:38:37', 1, 1, 15, 39, '000001_800003/27_800004/30_80000e/39_80000f/', 1, 'Original iPhone ', 'Original iPhone ', 'original_iphone', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(41, 1, '2009-02-03 12:15:02', '2009-02-03 12:38:37', 1, 1, 16, 39, '000001_800003/27_800004/30_80000e/39_800010/', 1, 'iPhone 3G ', 'iPhone 3G ', 'iphone_3g', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(42, 1, '2009-02-03 12:15:25', '2009-02-03 12:38:37', 1, 1, 17, 39, '000001_800003/27_800004/30_80000e/39_800011/', 1, 'Bluetooth Headset ', 'Bluetooth Headset ', 'bluetooth_headset', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(43, 1, '2009-02-03 12:15:58', '2009-02-03 12:38:37', 1, 1, 18, 30, '000001_800003/27_800004/30_800012/', 1, 'iPhone in the Enterprise ', 'iPhone in the Enterprise ', 'iphone_in_the_enterprise', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(44, 1, '2009-02-03 12:16:32', '2009-02-03 12:38:37', 1, 1, 19, 43, '000001_800003/27_800004/30_800012/43_800013/', 1, 'Enterprise Networking ', 'Enterprise Networking ', 'enterprise_networking', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(45, 1, '2009-02-03 12:16:50', '2009-02-03 12:38:37', 1, 1, 20, 43, '000001_800003/27_800004/30_800012/43_800014/', 1, 'Mail, Contacts and Calendars in the Enterprise ', 'Mail, Contacts and Calendars in', 'mail_contacts_and_calendars_in_the_enterprise', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(46, 1, '2009-02-03 12:17:11', '2009-02-03 12:38:37', 1, 1, 21, 43, '000001_800003/27_800004/30_800012/43_800015/', 1, 'Integrating iPhone into your business ', 'Integrating iPhone into your', 'integrating_iphone_into_your_business', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(47, 1, '2009-02-03 12:19:29', '2009-02-03 12:38:37', 1, 1, 24, 48, '000001_800016/28_800017/48_800018/', 1, 'Pages ''09 ', 'Pages ''09 ', 'pages_09', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(48, 1, '2009-02-03 12:20:01', '2009-02-03 12:38:37', 1, 1, 23, 28, '000001_800016/28_800017/', 1, 'iWork ''09 ', 'iWork ''09 ', 'iwork_09', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(49, 1, '2009-02-03 12:26:53', '2009-02-03 12:38:37', 1, 1, 25, 48, '000001_800016/28_800017/48_800019/', 1, 'Numbers ''09 ', 'Numbers ''09 ', 'numbers_09', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(50, 1, '2009-02-03 12:27:17', '2009-02-03 12:38:37', 1, 1, 26, 48, '000001_800016/28_800017/48_80001a/', 1, 'Keynote ''09 ', 'Keynote ''09 ', 'keynote_09', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(51, 1, '2009-02-03 12:27:37', '2009-02-03 12:38:37', 1, 1, 27, 48, '000001_800016/28_800017/48_80001b/', 1, 'iWork.com beta ', 'iWork.com beta ', 'iworkcom_beta', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(52, 1, '2009-02-03 12:28:07', '2009-02-03 12:38:37', 1, 1, 28, 28, '000001_800016/28_80001c/', 1, 'iWork ''08 ', 'iWork ''08 ', 'iwork_08', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(53, 1, '2009-02-03 12:28:31', '2009-02-03 12:38:37', 1, 1, 29, 52, '000001_800016/28_80001c/52_80001d/', 1, 'Numbers ', 'Numbers ', 'numbers', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(54, 1, '2009-02-03 12:28:47', '2009-02-03 12:38:37', 1, 1, 30, 52, '000001_800016/28_80001c/52_80001e/', 1, 'Keynote ''08 ', 'Keynote ''08 ', 'keynote_08', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(55, 1, '2009-02-03 12:29:11', '2009-02-03 12:38:37', 1, 1, 31, 52, '000001_800016/28_80001c/52_80001f/', 1, 'Pages ''08 ', 'Pages ''08 ', 'pages_08', ' Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(56, 1, '2009-02-03 12:29:39', '2009-02-03 12:38:37', 1, 1, 32, 28, '000001_800016/28_800020/', 1, 'iWork (previous to iWork ''08) ', 'iWork (previous to iWork ''08) ', 'iwork_previous_to_iwork_08', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(57, 1, '2009-02-03 12:30:02', '2009-02-03 12:38:37', 1, 1, 33, 56, '000001_800016/28_800020/56_800021/', 1, 'Keynote ', 'Keynote ', 'keynote', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(58, 1, '2009-02-03 12:30:20', '2009-02-03 12:38:37', 1, 1, 34, 56, '000001_800016/28_800020/56_800022/', 1, 'Pages ', 'Pages ', 'pages', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(61, 1, '2009-02-03 13:26:57', NULL, 1, NULL, 35, NULL, '000002_800023/', 2, 'Discussion Board', 'Discussion Board', 'discussion_board', '', 0);
INSERT INTO `forum_forum` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `container_id`, `title`, `short_title`, `slug`, `description`, `status`) VALUES(62, 1, '2009-02-03 14:02:42', NULL, 1, NULL, 36, NULL, '000001_800024/', 1, 'Test', 'Test', 'test', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `forum_forumcontainer`
--

DROP TABLE IF EXISTS `forum_forumcontainer`;
CREATE TABLE `forum_forumcontainer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `modified_date` datetime DEFAULT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` varchar(255) NOT NULL,
  `sysname` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `allow_bumping` tinyint(1) NOT NULL,
  `max_level` int(11) NOT NULL,
  `title_de` varchar(255) NOT NULL,
  `title_en` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_forumcontainer_content_type_id` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Daten für Tabelle `forum_forumcontainer`
--

INSERT INTO `forum_forumcontainer` (`id`, `creation_date`, `modified_date`, `content_type_id`, `object_id`, `sysname`, `title`, `allow_bumping`, `max_level`, `title_de`, `title_en`) VALUES(1, '2009-01-09 15:59:27', '2009-02-03 10:57:59', NULL, '', 'forum', 'General Forum', 1, 4, 'General Forum', 'Test Forum General');
INSERT INTO `forum_forumcontainer` (`id`, `creation_date`, `modified_date`, `content_type_id`, `object_id`, `sysname`, `title`, `allow_bumping`, `max_level`, `title_de`, `title_en`) VALUES(2, '2009-01-09 17:30:50', '2009-02-03 13:26:47', 58, '2', 'forum', 'Test Forum for Aidas', 0, 0, '', 'Test Forum for Aidas');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `forum_forumcontainer_sites`
--

DROP TABLE IF EXISTS `forum_forumcontainer_sites`;
CREATE TABLE `forum_forumcontainer_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forumcontainer_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forumcontainer_id` (`forumcontainer_id`,`site_id`),
  KEY `site_id_refs_id_47a8e9ab` (`site_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Daten für Tabelle `forum_forumcontainer_sites`
--


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `forum_forumreply`
--

DROP TABLE IF EXISTS `forum_forumreply`;
CREATE TABLE `forum_forumreply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_rte` tinyint(1) NOT NULL,
  `creation_date` datetime NOT NULL,
  `modified_date` datetime DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `modifier_id` int(11) DEFAULT NULL,
  `sort_order` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `path` varchar(8192) DEFAULT NULL,
  `thread_id` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_forumreply_creator_id` (`creator_id`),
  KEY `forum_forumreply_modifier_id` (`modifier_id`),
  KEY `forum_forumreply_parent_id` (`parent_id`),
  KEY `forum_forumreply_thread_id` (`thread_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=20 ;

--
-- Daten für Tabelle `forum_forumreply`
--

INSERT INTO `forum_forumreply` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `sort_order`, `parent_id`, `path`, `thread_id`, `subject`, `slug`, `message`) VALUES(19, 1, '2009-02-03 12:57:48', NULL, 1, NULL, 7, NULL, '800007/', 42, 'my 1st reply to the 2nd thread in the "Phone" ...', 'reply_1', 'my 1st reply to the 2nd thread in the "Phone" forum');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `forum_forumthread`
--

DROP TABLE IF EXISTS `forum_forumthread`;
CREATE TABLE `forum_forumthread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_rte` tinyint(1) NOT NULL,
  `creation_date` datetime NOT NULL,
  `modified_date` datetime DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `modifier_id` int(11) DEFAULT NULL,
  `views` int(11) NOT NULL,
  `forum_id` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `is_sticky` tinyint(1) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_forumthread_creator_id` (`creator_id`),
  KEY `forum_forumthread_modifier_id` (`modifier_id`),
  KEY `forum_forumthread_forum_id` (`forum_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=55 ;

--
-- Daten für Tabelle `forum_forumthread`
--

INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(48, 1, '2009-02-03 13:28:01', NULL, 1, NULL, 2, 61, 'Aidas first thread in his discussion board', 'thread_12', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(49, 1, '2009-02-03 13:28:35', NULL, 1, NULL, 0, 61, 'Aidas first sticky thread in his discusssion board', 'thread_13', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 1, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(50, 1, '2009-02-03 13:30:34', NULL, 1, NULL, 0, 61, 'Aidas first thread in his discussion board', 'thread_14', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(41, 1, '2009-02-03 12:52:26', NULL, 1, NULL, 3, 59, 'my 1st thread in the "Phone" forum', 'thread_1', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(42, 1, '2009-02-03 12:54:12', NULL, 1, NULL, 9, 59, 'my 2nd thread in the "Phone" forum', 'thread_6', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(43, 1, '2009-02-03 13:01:55', '2009-02-03 13:02:29', 1, 1, 4, 59, 'The 1st sticky thread in forum "Phone"', 'thread_7', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 1, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(44, 1, '2009-02-03 13:15:09', NULL, 1, NULL, 0, 59, 'my 3rd thread in the "Phone" forummy 2nd thread in the "Phone" forum', 'thread_8', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(45, 1, '2009-02-03 13:20:05', NULL, 1, NULL, 0, 59, 'my 4th thread in the "Phone" forum', 'thread_9', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(46, 1, '2009-02-03 13:20:39', NULL, 1, NULL, 0, 59, 'my 5th thread in the "Phone" forum', 'thread_10', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(47, 1, '2009-02-03 13:24:39', NULL, 1, NULL, 0, 33, 'my 1st thread in the "Music and Video" forum', 'thread_11', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(52, 1, '2009-02-03 14:10:19', NULL, 1, NULL, 0, 62, 'first test thread', 'thread_15', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 1, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(53, 1, '2009-02-03 14:11:21', NULL, 1, NULL, 0, 62, 'second test thread', 'thread_16', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 0, 0);
INSERT INTO `forum_forumthread` (`id`, `is_rte`, `creation_date`, `modified_date`, `creator_id`, `modifier_id`, `views`, `forum_id`, `subject`, `slug`, `message`, `is_sticky`, `status`) VALUES(54, 1, '2009-02-03 14:11:54', NULL, 1, NULL, 0, 62, 'a sticky test thread', 'thread_17', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 1, 0);

-- forum.forum
ALTER TABLE `forum_forum` DROP `is_rte`;
ALTER TABLE `forum_forum` ADD `description_markup_type` VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL AFTER `description`;

-- forum.forumthread
ALTER TABLE `forum_forumthread` DROP `is_rte`;
ALTER TABLE `forum_forumthread` ADD `message_markup_type` VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL AFTER `message`;

-- forum.forumreply
ALTER TABLE `forum_forumreply` DROP `is_rte`;
ALTER TABLE `forum_forumreply` ADD `message_markup_type` VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL AFTER `message`;
