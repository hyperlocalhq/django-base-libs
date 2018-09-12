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
INSERT IGNORE INTO `shop_shopproducttype` (`id`, `slug`, `parent_id`, `title`, `title_de`, `title_en`, `title_fr`, `title_pl`, `title_tr`, `title_es`, `title_it`, `lft`, `rght`, `tree_id`, `level`) VALUES
	(2, 'katalog', NULL, 'Katalog', 'Katalog', 'Catalogue', '', '', '', '', '', 1, 6, 9, 0),
	(3, 'souvenir-geschenkartikel', NULL, 'Souvenir, Geschenkartikel', 'Souvenir, Geschenkartikel', 'Souvenir, gift', '', '', '', '', '', 1, 8, 2, 0),
	(4, 'spiel', 3, 'Spiel', 'Spiel', 'Game', '', '', '', '', '', 2, 3, 2, 1),
	(5, 'cd', NULL, 'CD', 'CD', 'CD', '', '', '', '', '', 1, 2, 3, 0),
	(6, 'stadtplan', NULL, 'Stadtplan', 'Stadtplan', 'City map', '', '', '', '', '', 1, 2, 4, 0),
	(7, 'horbuch', NULL, 'Hörbuch', 'Hörbuch', 'Audiobook', '', '', '', '', '', 1, 2, 5, 0),
	(8, 'ausstellungskatalog', 2, 'Ausstellungskatalog', 'Ausstellungskatalog', 'Exhibition catalogue', '', '', '', '', '', 4, 5, 9, 1),
	(9, 'jutebeutel', 3, 'Jutebeutel', 'Jutebeutel', 'Jute bag', '', '', '', '', '', 4, 5, 2, 1),
	(10, 'buchstutze', 3, 'Buchstütze', 'Buchstütze', 'Bookend', '', '', '', '', '', 6, 7, 2, 1),
	(11, 'katalog-zur-dauerausstellung', 2, 'Katalog zur Dauerausstellung', 'Katalog zur Dauerausstellung', 'Permanent exhibition catalogue', '', '', '', '', '', 2, 3, 9, 1),
	(12, 'produkt-fur-kinder', NULL, 'Produkt für Kinder', 'Produkt für Kinder', 'Product for children', '', '', '', '', '', 1, 2, 8, 0);
/*!40000 ALTER TABLE `shop_shopproducttype` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
