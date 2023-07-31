-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-07-2023 a las 04:55:25
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `consultas_iub`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `identificacion_admin` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `cargo` varchar(20) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `contraseña` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consulta`
--

CREATE TABLE `consulta` (
  `id_consulta` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `descripcion` varchar(200) NOT NULL,
  `id_modulo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consulta`
--

INSERT INTO `consulta` (`id_consulta`, `id_estudiante`, `id_profesor`, `fecha`, `descripcion`, `id_modulo`) VALUES
(1, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(3, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(4, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(5, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(6, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(7, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(8, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(9, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(10, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(11, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(12, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(13, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(14, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(15, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(16, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(17, 1, 1, '2023-07-14 00:00:00', 'Descripción de la consulta', 2),
(18, 2, 1, '2023-07-13 21:24:00', 'hdfhf', 3),
(19, 2, 2, '2023-07-21 21:27:00', '2323', 3),
(20, 2, 1, '2023-07-13 07:55:00', 'Problemas en notas', 2),
(21, 2, 2, '2023-07-13 07:56:00', 'Error en larea', 3),
(22, 2, 1, '2023-07-13 08:12:00', 'No puedo ir hoy a clase', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `tipo_documento` varchar(11) NOT NULL,
  `programa` varchar(30) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `contraseña` varchar(20) NOT NULL,
  `numero_estudiante` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiante`
--

INSERT INTO `estudiante` (`id`, `nombre`, `apellido`, `tipo_documento`, `programa`, `correo`, `contraseña`, `numero_estudiante`) VALUES
(1, 'Daniela', 'Pantoja', 'CC', 'Redes', 'Pantojadaniela@gmail.com', '12345', 123456),
(2, 'Maria', 'duarte', 'CC', 'sistemas', 'jose@gmail.com', '12345', 456789),
(3, 'Papi', 'Ama', 'CC', 'Programción', 'l@i.com', '12345', 34567890),
(4, 'iiii', '7777', 'TI', 'Redes 1', 'j@i.com', '456789', 788766),
(5, 'iiii', '7777', 'TI', 'Redes 1', 'j@i.com', '456789', 788766);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modulo`
--

CREATE TABLE `modulo` (
  `id_modulo` int(11) NOT NULL,
  `codigo_modulo` varchar(200) NOT NULL,
  `nombre_modulo` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modulo`
--

INSERT INTO `modulo` (`id_modulo`, `codigo_modulo`, `nombre_modulo`) VALUES
(2, 'com22', 'base de datos'),
(3, 'apa23', 'redes 2'),
(4, 'efe15', 'pin2'),
(5, 'ser', 'pagina web');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesor`
--

CREATE TABLE `profesor` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesor`
--

INSERT INTO `profesor` (`id`, `nombre`, `apellido`, `correo`, `password`) VALUES
(1, 'Luis', 'Lobo', 'llobo@gmail.com', '12345'),
(2, 'Malena', 'Castro', 'mcastro@gmail.com', '12345');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programas`
--

CREATE TABLE `programas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `programas`
--

INSERT INTO `programas` (`id`, `nombre`) VALUES
(1, 'Programción'),
(2, 'Redes 1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `res_consulta`
--

CREATE TABLE `res_consulta` (
  `id` int(11) NOT NULL,
  `id_consultas` int(11) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `modalidad` varchar(20) NOT NULL,
  `asunto` varchar(200) NOT NULL,
  `identificacion_estudiante` int(11) NOT NULL,
  `identificacion_profesor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sedes`
--

CREATE TABLE `sedes` (
  `iub_barranquilla` varchar(10) NOT NULL,
  `iub_soledad` varchar(10) NOT NULL,
  `teams` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`identificacion_admin`);

--
-- Indices de la tabla `consulta`
--
ALTER TABLE `consulta`
  ADD PRIMARY KEY (`id_consulta`),
  ADD KEY `identificacion_estudiante` (`id_estudiante`),
  ADD KEY `identificacion_profesor` (`id_profesor`),
  ADD KEY `id_modulo` (`id_modulo`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modulo`
--
ALTER TABLE `modulo`
  ADD PRIMARY KEY (`id_modulo`);

--
-- Indices de la tabla `profesor`
--
ALTER TABLE `profesor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `programas`
--
ALTER TABLE `programas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `res_consulta`
--
ALTER TABLE `res_consulta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_consultas` (`id_consultas`),
  ADD KEY `identificacion_estudiante` (`identificacion_estudiante`,`identificacion_profesor`),
  ADD KEY `identificacion_profesor` (`identificacion_profesor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `consulta`
--
ALTER TABLE `consulta`
  MODIFY `id_consulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `modulo`
--
ALTER TABLE `modulo`
  MODIFY `id_modulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `res_consulta`
--
ALTER TABLE `res_consulta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `consulta`
--
ALTER TABLE `consulta`
  ADD CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_3` FOREIGN KEY (`id_modulo`) REFERENCES `modulo` (`id_modulo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_4` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_5` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_6` FOREIGN KEY (`id_modulo`) REFERENCES `modulo` (`id_modulo`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_7` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_8` FOREIGN KEY (`id_profesor`) REFERENCES `profesor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `consulta_ibfk_9` FOREIGN KEY (`id_modulo`) REFERENCES `modulo` (`id_modulo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `res_consulta`
--
ALTER TABLE `res_consulta`
  ADD CONSTRAINT `res_consulta_ibfk_2` FOREIGN KEY (`identificacion_estudiante`) REFERENCES `estudiante` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `res_consulta_ibfk_3` FOREIGN KEY (`identificacion_profesor`) REFERENCES `profesor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `res_consulta_ibfk_4` FOREIGN KEY (`id_consultas`) REFERENCES `consulta` (`id_consulta`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
