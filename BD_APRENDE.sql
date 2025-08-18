-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla database_apremaynas.curso
CREATE TABLE IF NOT EXISTS `curso` (
  `cur_id` int NOT NULL AUTO_INCREMENT,
  `cur_nombre` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cur_descripcion` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`cur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.curso: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.examen
CREATE TABLE IF NOT EXISTS `examen` (
  `exa_id` int NOT NULL AUTO_INCREMENT,
  `exa_titulo` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cur_id` int NOT NULL,
  `nivel_id` int NOT NULL,
  PRIMARY KEY (`exa_id`),
  KEY `Examen_cur_id_fkey` (`cur_id`),
  KEY `Examen_nivel_id_fkey` (`nivel_id`),
  CONSTRAINT `Examen_cur_id_fkey` FOREIGN KEY (`cur_id`) REFERENCES `curso` (`cur_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Examen_nivel_id_fkey` FOREIGN KEY (`nivel_id`) REFERENCES `nivel` (`niv_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.examen: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.intentoexamen
CREATE TABLE IF NOT EXISTS `intentoexamen` (
  `int_id` int NOT NULL AUTO_INCREMENT,
  `usu_id` int NOT NULL,
  `exa_id` int NOT NULL,
  `puntaje` double NOT NULL,
  `fecha` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`int_id`),
  KEY `IntentoExamen_usu_id_fkey` (`usu_id`),
  KEY `IntentoExamen_exa_id_fkey` (`exa_id`),
  CONSTRAINT `IntentoExamen_exa_id_fkey` FOREIGN KEY (`exa_id`) REFERENCES `examen` (`exa_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `IntentoExamen_usu_id_fkey` FOREIGN KEY (`usu_id`) REFERENCES `usuario` (`usu_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.intentoexamen: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.leccion
CREATE TABLE IF NOT EXISTS `leccion` (
  `lec_id` int NOT NULL AUTO_INCREMENT,
  `lec_titulo` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cur_id` int NOT NULL,
  `nivel_id` int NOT NULL,
  PRIMARY KEY (`lec_id`),
  KEY `Leccion_cur_id_fkey` (`cur_id`),
  KEY `Leccion_nivel_id_fkey` (`nivel_id`),
  CONSTRAINT `Leccion_cur_id_fkey` FOREIGN KEY (`cur_id`) REFERENCES `curso` (`cur_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Leccion_nivel_id_fkey` FOREIGN KEY (`nivel_id`) REFERENCES `nivel` (`niv_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.leccion: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.nivel
CREATE TABLE IF NOT EXISTS `nivel` (
  `niv_id` int NOT NULL AUTO_INCREMENT,
  `niv_nombre` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`niv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.nivel: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.pregunta
CREATE TABLE IF NOT EXISTS `pregunta` (
  `pre_id` int NOT NULL AUTO_INCREMENT,
  `pre_texto` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cur_id` int NOT NULL,
  `nivel_id` int NOT NULL,
  PRIMARY KEY (`pre_id`),
  KEY `Pregunta_cur_id_fkey` (`cur_id`),
  KEY `Pregunta_nivel_id_fkey` (`nivel_id`),
  CONSTRAINT `Pregunta_cur_id_fkey` FOREIGN KEY (`cur_id`) REFERENCES `curso` (`cur_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Pregunta_nivel_id_fkey` FOREIGN KEY (`nivel_id`) REFERENCES `nivel` (`niv_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.pregunta: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.respuesta
CREATE TABLE IF NOT EXISTS `respuesta` (
  `res_id` int NOT NULL AUTO_INCREMENT,
  `res_texto` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `es_correcta` tinyint(1) NOT NULL,
  `pre_id` int NOT NULL,
  PRIMARY KEY (`res_id`),
  KEY `Respuesta_pre_id_fkey` (`pre_id`),
  CONSTRAINT `Respuesta_pre_id_fkey` FOREIGN KEY (`pre_id`) REFERENCES `pregunta` (`pre_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.respuesta: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.respuestausuario
CREATE TABLE IF NOT EXISTS `respuestausuario` (
  `run_id` int NOT NULL AUTO_INCREMENT,
  `int_id` int NOT NULL,
  `pre_id` int NOT NULL,
  `res_id` int NOT NULL,
  `usu_id` int NOT NULL,
  PRIMARY KEY (`run_id`),
  KEY `RespuestaUsuario_int_id_fkey` (`int_id`),
  KEY `RespuestaUsuario_pre_id_fkey` (`pre_id`),
  KEY `RespuestaUsuario_res_id_fkey` (`res_id`),
  KEY `RespuestaUsuario_usu_id_fkey` (`usu_id`),
  CONSTRAINT `RespuestaUsuario_int_id_fkey` FOREIGN KEY (`int_id`) REFERENCES `intentoexamen` (`int_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `RespuestaUsuario_pre_id_fkey` FOREIGN KEY (`pre_id`) REFERENCES `pregunta` (`pre_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `RespuestaUsuario_res_id_fkey` FOREIGN KEY (`res_id`) REFERENCES `respuesta` (`res_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `RespuestaUsuario_usu_id_fkey` FOREIGN KEY (`usu_id`) REFERENCES `usuario` (`usu_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.respuestausuario: ~0 rows (aproximadamente)

-- Volcando estructura para tabla database_apremaynas.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `usu_id` int NOT NULL AUTO_INCREMENT,
  `usu_nombre` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usu_email` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usu_password` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usu_colegio` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usu_grado` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_registro` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `usu_apellidos` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`usu_id`),
  UNIQUE KEY `Usuario_usu_email_key` (`usu_email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas.usuario: ~0 rows (aproximadamente)
REPLACE INTO `usuario` (`usu_id`, `usu_nombre`, `usu_email`, `usu_password`, `usu_colegio`, `usu_grado`, `fecha_registro`, `usu_apellidos`) VALUES
	(2, 'Carlos', 'carlos@email.com', '$2b$10$5dl5pD77zgqIb.dQBNh1BeAgn5XyQaMhoovWwFoa.oF37IrtWLSCe', 'Colegio Nacional', '5to grado', '2025-08-04 17:46:39.891', 'Pilco Ramirez');

-- Volcando estructura para tabla database_apremaynas._prisma_migrations
CREATE TABLE IF NOT EXISTS `_prisma_migrations` (
  `id` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `checksum` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `finished_at` datetime(3) DEFAULT NULL,
  `migration_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `logs` text COLLATE utf8mb4_unicode_ci,
  `rolled_back_at` datetime(3) DEFAULT NULL,
  `started_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `applied_steps_count` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla database_apremaynas._prisma_migrations: ~0 rows (aproximadamente)
REPLACE INTO `_prisma_migrations` (`id`, `checksum`, `finished_at`, `migration_name`, `logs`, `rolled_back_at`, `started_at`, `applied_steps_count`) VALUES
	('3c34fa06-7bf0-4b98-8a38-04377ff8c90f', 'd80be5bbc2f9a24110620da0518785cde6eaacb1221561f38af27ead6b595516', '2025-08-01 20:55:05.119', '20250801205504_first_migrate', NULL, NULL, '2025-08-01 20:55:04.759', 1),
	('6b34e3e9-38d3-4b4c-b2c9-ced2bbb3d42f', 'e4e2dc3439a7751db60977e26271a3dd51169453d7c96127f3b7270e01787497', '2025-08-04 14:52:12.226', '20250804145212_agregar_apellido', NULL, NULL, '2025-08-04 14:52:12.208', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
