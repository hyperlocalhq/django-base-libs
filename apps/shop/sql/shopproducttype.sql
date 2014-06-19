-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server Version:               5.6.16 - MySQL Community Server (GPL)
-- Server Betriebssystem:        Win32
-- HeidiSQL Version:             8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- Exportiere Daten aus Tabelle studio38_museumsportal.shop_shopproducttype: 11 rows
/*!40000 ALTER TABLE `shop_shopproducttype` DISABLE KEYS */;
INSERT IGNORE INTO `shop_shopproducttype` (`id`, `creation_date`, `modified_date`, `slug`, `parent_id`, `title`, `title_de`, `title_en`, `title_fr`, `title_pl`, `title_tr`, `title_es`, `title_it`, `lft`, `rght`, `tree_id`, `level`) VALUES
	(2, '2014-06-18 00:00:59', '2014-06-18 13:02:21', 'katalog', NULL, 'Katalog', 'Katalog', 'Catalogue', '', '', '', '', '', 1, 6, 9, 0),
	(3, '2014-06-18 00:03:14', NULL, 'souvenir-geschenkartikel', NULL, 'Souvenir, Geschenkartikel', 'Souvenir, Geschenkartikel', 'Souvenir, gift', '', '', '', '', '', 1, 8, 2, 0),
	(4, '2014-06-18 00:03:40', NULL, 'spiel', 3, 'Spiel', 'Spiel', 'Game', '', '', '', '', '', 2, 3, 2, 1),
	(5, '2014-06-18 00:04:48', NULL, 'cd', NULL, 'CD', 'CD', 'CD', '', '', '', '', '', 1, 2, 3, 0),
	(6, '2014-06-18 00:05:18', NULL, 'stadtplan', NULL, 'Stadtplan', 'Stadtplan', 'City map', '', '', '', '', '', 1, 2, 4, 0),
	(7, '2014-06-18 00:05:45', NULL, 'horbuch', NULL, 'Hörbuch', 'Hörbuch', 'Audiobook', '', '', '', '', '', 1, 2, 5, 0),
	(8, '2014-06-18 00:06:17', '2014-06-18 17:07:40', 'ausstellungskatalog', 2, 'Ausstellungskatalog', 'Ausstellungskatalog', 'Exhibition catalogue', '', '', '', '', '', 4, 5, 9, 1),
	(9, '2014-06-18 00:07:33', NULL, 'jutebeutel', 3, 'Jutebeutel', 'Jutebeutel', 'Jute bag', '', '', '', '', '', 4, 5, 2, 1),
	(10, '2014-06-18 00:08:52', '2014-06-18 13:03:10', 'buchstutze', 3, 'Buchstütze', 'Buchstütze', 'Bookend', '', '', '', '', '', 6, 7, 2, 1),
	(11, '2014-06-18 00:09:28', '2014-06-18 17:05:46', 'katalog-zur-dauerausstellung', 2, 'Katalog zur Dauerausstellung', 'Katalog zur Dauerausstellung', 'Permanent exhibition catalogue', '', '', '', '', '', 2, 3, 9, 1),
	(12, '2014-06-18 00:10:07', NULL, 'produkt-fur-kinder', NULL, 'Produkt für Kinder', 'Produkt für Kinder', 'Product for children', '', '', '', '', '', 1, 2, 8, 0);
/*!40000 ALTER TABLE `shop_shopproducttype` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
