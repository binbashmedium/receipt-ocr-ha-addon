-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: core-mariadb:3306
-- Erstellungszeit: 19. Dez 2025 um 10:23
-- Server-Version: 10.11.6-MariaDB
-- PHP-Version: 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `receipts`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `article_alias`
--

CREATE TABLE `article_alias` (
  `id` int(10) UNSIGNED NOT NULL,
  `pattern` varchar(255) DEFAULT NULL,
  `canonical_name` varchar(100) NOT NULL,
  `priority` int(11) NOT NULL DEFAULT 100,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `category` varchar(50) NOT NULL DEFAULT 'Sonstiges'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Daten für Tabelle `article_alias`
--

INSERT INTO `article_alias` (`id`, `pattern`, `canonical_name`, `priority`, `active`, `created_at`, `category`) VALUES
(1, '%APFEL%', 'Apfel', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(2, '%BIRNE%', 'Birne', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(3, '%KIWI%', 'Kiwi', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(4, '%CLEMENTINE%', 'Clementine', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(5, '%TRAUBE%', 'Traube', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(6, '%AVOCADO%', 'Avocado', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(7, '%KAKI%', 'Kaki', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(8, '%PFLAUME%', 'Pflaume', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(9, '%PHYSALIS%', 'Physalis', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(10, '%HEIDEL%', 'Beeren', 90, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(11, '%BEEREN%', 'Beeren', 100, 1, '2025-12-19 06:44:24', 'Lebensmittel'),
(12, '%ZWIEBEL%', 'Zwiebel', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(13, '%KAROT%', 'Karotte', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(14, '%BROCCOLI%', 'Brokkoli', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(15, '%BLUMENKOHL%', 'Blumenkohl', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(16, '%KOHLRABI%', 'Kohlrabi', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(17, '%LAUCH%', 'Lauch', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(18, '%RADIES%', 'Radieschen', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(19, '%TOMATE%', 'Tomate', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(20, '%CHAMPIGN%', 'Champignon', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(21, '%KÜRBIS%', 'Kürbis', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(22, '%KNOBLAUCH%', 'Knoblauch', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(23, '%SPINAT%', 'Spinat', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(24, '%SELLER%', 'Sellerie', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(25, '%ZUCCHINI%', 'Zucchini', 100, 1, '2025-12-19 06:44:34', 'Lebensmittel'),
(26, '%HAFER%DR%', 'Haferdrink', 50, 1, '2025-12-19 06:44:47', 'Lebensmittel'),
(27, '%HAFERDR%', 'Haferdrink', 50, 1, '2025-12-19 06:44:47', 'Lebensmittel'),
(28, '%MANDEL%DR%', 'Mandeldrink', 50, 1, '2025-12-19 06:44:47', 'Lebensmittel'),
(29, '%KOKO%DR%', 'Kokosdrink', 50, 1, '2025-12-19 06:44:47', 'Lebensmittel'),
(30, '%KEFIR%', 'Kefir', 100, 1, '2025-12-19 06:44:47', 'Lebensmittel'),
(31, '%HAFERFLOCK%', 'Haferflocken', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(32, '%SPAGHET%', 'Pasta', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(33, '%LASAGNE%', 'Pasta', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(34, '%PASTA%', 'Pasta', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(35, '%BROT%', 'Brot', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(36, '%BAGUETTE%', 'Brot', 100, 1, '2025-12-19 06:45:00', 'Lebensmittel'),
(37, '%MUELLBEUTEL%', 'Muellbeutel', 100, 1, '2025-12-19 06:45:13', 'Haushaltswaren'),
(38, '%GESCHIRRTABS%', 'Geschirrtabs', 100, 1, '2025-12-19 06:45:13', 'Haushaltswaren'),
(39, '%BACKPAPIER%', 'Backpapier', 100, 1, '2025-12-19 06:45:13', 'Haushaltswaren'),
(40, '%SEIFE%', 'Seife', 100, 1, '2025-12-19 06:45:13', 'Haushaltsmittel'),
(41, '%TOIPA%', 'Toilettenpapier', 100, 1, '2025-12-19 06:45:13', 'Haushaltswaren'),
(42, '%FARBFANG%', 'Farbfangtuch', 100, 1, '2025-12-19 06:45:13', 'Haushaltswaren'),
(43, '%PFAND%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(44, '%KARTE%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(45, '%SUM%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(46, '%MWST%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(47, '%TERMINAL%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(48, '%RUECKGELD%', '__IGNORE__', 1, 1, '2025-12-19 06:45:45', 'Sonstiges'),
(49, '%*  X%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(50, '%*B VEG. TEEWURST FEIN%', 'Vegane Teewurst', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(51, '%*C BIO TOFU SCHWARZWALD%', 'Tofu', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(52, '%1=%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(53, '%17:12 WEIBE SCHOKO-HIMBEER%', 'Schokolade', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(54, '%2 - X%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(55, '%2=%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(56, '%WEICHSP%', 'Weichspüler', 50, 1, '2025-12-19 09:42:13', 'Haushaltswaren'),
(57, '%KAFFEE%', 'Kaffee', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(58, '%BEDDA HIRTE BLOCK PESRS%', 'Veganer Feta', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(59, '%BERGAD.MINILAIB 300G%', 'Käse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(60, '%BIO ALN.HAFERCREME CUI%', 'Hafercuisine', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(62, '%BIO BERGKASE%', 'Bergkase', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(64, '%BIO KORO ERDNUSSM%', 'Erdnussmus', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(65, '%BIO SOJA SAUCE%', 'Soja Sauce', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(66, '%BIO SPEISEKART%', 'Kartoffel', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(67, '%TOFU%', 'Tofu', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(69, '%BIO TEGUT VEGAN%', 'BIO tegut vegan', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(70, '%BIO TG K1P MOHREN%', 'Karotte', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(71, '%SAUERKRAUT%', 'Sauerkraut', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(72, '%BIO WINI-ROMANASALAT%', 'Romanasalat', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(73, '%BIO YOGI TEA CHAI%', 'Tee', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(74, '%INGWER%', 'Ingwer', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(76, '%DONUT%', 'Donuts', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(78, '%BOTATO KARTOFFELPUFFER 600G%', 'Kartoffelpuffer', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(79, '%BR JODSALZ FLOURID/FOLSAE.5009%', 'Jodsalz', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(80, '%BRAUSETABLETTEN 17ST 102G%', 'Brausetabletten', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(81, '%CASHEWKERNE NATUR%', 'Cashewkerne natur', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(82, '%CHEESEPOP GOUDA%', 'GOUDA', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(83, '%CHERRY RISPE BIO%', 'Tomate', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(84, '%WALNUSS%', 'Walnuss', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(85, '%CREME FRAICHE%', 'Creme Fraiche', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(86, '%DELI REFORM%', 'Margarine', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(87, '%DELI. BRUEHE%', 'Brühe', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(88, '%DILL%', 'Dill', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(89, '%FETA%', 'Feta', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(90, '%DRINK KOKO. UNGES%', 'Kokosdrink', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(91, '%FILATA, SCHEIBEN%', 'Veganer Käse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(92, '%FRISCHECREME TOSKANA%', 'Frischkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(93, '%FULFIL CHOCO.SALTED-CA%', 'FULFIL Choco.Salted-Ca', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(94, '%FULFIL WHITE CHOC.COOK%', 'FULFIL White Choc.Cook', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(95, '%CHIPS%', 'Chips', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(96, '%G&G HARZER MINIS%', 'Handkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(97, '%GRILLKAESE%', 'Grillkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(98, '%GEGEBEN%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(99, '%GIOTTO HASELNUSS%', 'Giotto Haselnuss', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(100, '%GL HARZER NINIS SORT.115G%', 'Handkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(101, '%WURST%', 'Vegane Wurst', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(103, '%HUMMUS%', 'Hummus', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(104, '%H. PROT. GRIESSPUD%', 'Grießpudding', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(105, '%HANDEINGABE E-BON  HANDKAESE KUEMM%', 'Handkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(106, '%HANDEINGABE E-BON  SENFSAUCE INGWER%', 'Senfsauce', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(107, '%HANFSAMEN GESCHA%', 'Hanfsamen', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(109, '%HUMMUS NATUR%', 'Hummus', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(110, '%IGLO GEM.STAEBCHEN%', 'Vegane Fischstäbchen', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(111, '%J.TAG EIERSPATZLE%', 'Eierspatzle', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(112, '%SMOOTHIE%', 'Smoothie', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(113, '%KAMILLEN TEE%', 'Tee', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(114, '%KARTOFFEL%', 'Kartoffel', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(117, '%KIVI GOLD ST%', 'Kiwi', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(118, '%KUVERTUERE ZB%', 'Kuvertüre', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(119, '%LAUGENSTANGEN%', 'Laugenstange', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(120, '%LEERG. EW E. ST B *  X%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(121, '%LIEBLINGSSTEINOFENBAG250G%', 'Brot', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(122, '%MAGEN-GEL%', 'MAGEN-GEL', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(123, '%MINI PAPRIKA 200G TABALUGA%', 'Paprika', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(124, '%NORMALPREIS%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(125, '%OBST/GEMUSE STK%', 'Obst&Gemuse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(126, '%OBST/GEMUSE WAAGE  X%', 'Obst&Gemuse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(127, '%OBST&GEMUESE ERM%', 'Obst&Gemuse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(128, '%OLIVENMIX150G%', 'Oliven', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(129, '%ZAHNCREME%', 'Zahnpasta', 50, 1, '2025-12-19 09:42:13', 'Haushaltswaren'),
(131, '%PAPRIN. MANG. -FRI%', 'PAPRIN. MANG. -FRI', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(133, '%PETE PRETZEL%', 'PETE PRETZEL', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(134, '%RABATT 25% A INGWER & ZITRONE HONIG SHOT%', 'Ingwer & Zitrone Honig Shot', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(135, '%ROSENKOHL 750G%', 'Rosenkohl', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(136, '%RUCKGELD ZU VERST NETTO%', '__IGNORE__', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(137, '%SAUERKRAUT KLASS%', 'Sauerkraut', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(139, '%SCHLOTTEN%', 'Schalotten', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(140, '%SCHNECKE** APFET-MANDET-SCHNECKE (VEGAN)%', 'Zimtschnecke', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(141, '%SCHUPF%', 'Schupfnudeln', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(142, '%SESAMOEL NATIV%', 'Sesamöl', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(143, '%SIMPLY V GERIEBEN%', 'Veganer Käse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(144, '%SUKME%', '__IGNORE__', 1, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(145, '%SUKME [8]%', '__IGNORE__', 1, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(147, '%SUNKE%', '__IGNORE__', 1, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(148, '%SUWME [13]%', '__IGNORE__', 1, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(149, '%TANT.FLAMMKUCHENT%', 'Flammkuchen Teig', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(150, '%TETESEPT MEERW. NASENS%', 'Nasenspray', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(151, '%TG DLY AYKOS ASIA BOWL%', 'Asia Bowl', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(152, '%HACK%', 'Veganes Hack', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(155, '%VEHAPPYVEGA.CORDONB1.200G%', 'Veganes Cordonbleu', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(156, '%VHYEGA.FLE.FR.S.SORT.200G%', 'Vhyega.Fle.fr.S.sort.200g', 50, 1, '2025-12-19 09:42:13', 'Sonstiges'),
(157, '%VIB. BIO SHOT SORT. 95ML%', 'Shot', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(158, '%VORARLB BERGK%', 'Bergkäse', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel'),
(161, '%WICK BLAU OHNE Z%', 'Bonbons', 50, 1, '2025-12-19 09:42:13', 'Lebensmittel');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `receipts`
--

CREATE TABLE `receipts` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `file` varchar(255) DEFAULT NULL,
  `engine` varchar(50) DEFAULT NULL,
  `store` varchar(100) DEFAULT NULL,
  `total` decimal(12,2) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Tabellenstruktur für Tabelle `receipt_items`
--

CREATE TABLE `receipt_items` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `receipt_id` bigint(20) UNSIGNED DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `qty` decimal(12,3) DEFAULT NULL,
  `price` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `article_alias`
--
ALTER TABLE `article_alias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uniq_pattern` (`pattern`),
  ADD KEY `idx_pattern` (`pattern`),
  ADD KEY `idx_canonical` (`canonical_name`),
  ADD KEY `idx_active_priority` (`active`,`priority`);

--
-- Indizes für die Tabelle `receipts`
--
ALTER TABLE `receipts`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receipt_id` (`receipt_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `article_alias`
--
ALTER TABLE `article_alias`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=176;

--
-- AUTO_INCREMENT für Tabelle `receipts`
--
ALTER TABLE `receipts`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT für Tabelle `receipt_items`
--
ALTER TABLE `receipt_items`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=233;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD CONSTRAINT `receipt_items_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipts` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
