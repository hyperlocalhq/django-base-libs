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
-- Exportiere Daten aus Tabelle studio38_museumsportal.shop_shopproductcategory: 11 rows
/*!40000 ALTER TABLE `shop_shopproductcategory` DISABLE KEYS */;
INSERT IGNORE INTO `shop_shopproductcategory` (`id`, `title`, `title_de`, `title_en`, `title_fr`, `title_pl`, `title_tr`, `title_es`, `title_it`, `slug`) VALUES
	(2, 'Kulturen der Welt', 'Kulturen der Welt', 'World cultures', '', '', '', '', '', 'kulturen-der-welt'),
	(3, 'Schlösser und Gärten', 'Schlösser und Gärten', 'Palaces and gardens', '', '', '', '', '', 'schloesser-und-gaerten'),
	(5, 'Bildende Kunst', 'Bildende Kunst', 'Fine arts', '', '', '', '', '', 'bildende-kunst'),
	(6, 'Geschichte', 'Geschichte', 'History', '', '', '', '', '', 'geschichte'),
	(7, 'Kulturgeschichte (1900 bis 1945)', 'Kulturgeschichte (1900 bis 1945)', 'Cultural history  (1900 to 1945)', '', '', '', '', '', 'kulturgeschichte-1900-bis-1945'),
	(8, 'Kulturgeschichte (1945 bis heute)', 'Kulturgeschichte (1945 bis heute)', 'Cultural history (1945 to the present)', '', '', '', '', '', 'kulturgeschichte-1945-bis-heute'),
	(9, 'Architektur', 'Architektur', 'Architecture', '', '', '', '', '', 'architektur'),
	(10, 'Kunstgewerbe', 'Kunstgewerbe', 'Applied Arts and Crafts', '', '', '', '', '', 'kunstgewerbe'),
	(11, 'Design', 'Design', 'Design', '', '', '', '', '', 'design'),
	(12, 'Kulturgeschichte (Berlingeschichte)', 'Kulturgeschichte (Berlingeschichte)', 'Cultural history (History of Berlin)', '', '', '', '', '', 'kulturgeschichte-berlingeschichte'),
	(13, 'Spezialmuseen', 'Spezialmuseen', 'Specialized museums', '', '', '', '', '', 'spezialmuseen');
/*!40000 ALTER TABLE `shop_shopproductcategory` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
