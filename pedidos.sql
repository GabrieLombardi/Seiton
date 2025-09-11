-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-04-2025 a las 03:22:14
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- Base de datos: `pedidos`

-- --------------------------------------------------------

-- Estructura de tabla para la tabla `chofer`
CREATE TABLE `chofer` (
  `id` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `cuit` int(50) NOT NULL,
  `dni` int(8) NOT NULL,
  `fn` date NOT NULL,
  `telefono` int(50) NOT NULL,
  `direccion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

-- Estructura de tabla para la tabla `ciudad`
CREATE TABLE `ciudad` (
  `id` int(10) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `cod_postal` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

-- Estructura de tabla para la tabla `clientes`
CREATE TABLE `clientes` (
  `id` int(10) NOT NULL,
  `cliente` varchar(50) NOT NULL,
  `cuit` int(50) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `telefono` int(50) NOT NULL,
  `dni` int(8) NOT NULL,
  `id_ciudad` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_planilla`
CREATE TABLE `detalle_planilla` (
  `id_detalle` int(10) NOT NULL,
  `id_vehiculo` int(10) NOT NULL,
  `id_planilla` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_producto`
CREATE TABLE `detalle_producto` (
  `id_cliente` int(10) NOT NULL,
  `id_producto` int(10) NOT NULL,
  `cantidad` int(10) NOT NULL,
  `subtotal` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago`
CREATE TABLE `pago` (
  `id_pago` int(10) NOT NULL,
  `pago_completo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planilla`
CREATE TABLE `planilla` (
  `id_planilla` int(10) NOT NULL,
  `fecha` date NOT NULL,
  `id_chofer` int(10) NOT NULL,
  `id_ciudad` int(10) NOT NULL,
  `id_pago` tinyint(1) NOT NULL,
  `total` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
CREATE TABLE `producto` (
  `id_producto` int(10) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `cod_producto` int(20) NOT NULL,
  `precio_unit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
CREATE TABLE `usuario` (
  `id_usuario` int(10) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contraseña` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
CREATE TABLE `vehiculo` (
  `id_vehiculo` int(10) NOT NULL,
  `matricula` int(10) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `disponobilidad` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas


--
-- Indices de la tabla `chofer`
ALTER TABLE `chofer`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `detalle_planilla`
--
ALTER TABLE `detalle_planilla`
  ADD PRIMARY KEY (`id_detalle`);

--
-- Indices de la tabla `pago`
--
ALTER TABLE `pago`
  ADD PRIMARY KEY (`id_pago`);

--
-- Indices de la tabla `planilla`
--
ALTER TABLE `planilla`
  ADD PRIMARY KEY (`id_planilla`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- Indices de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD PRIMARY KEY (`id_vehiculo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `chofer`
--
ALTER TABLE `chofer`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ciudad`
--
ALTER TABLE `ciudad`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_planilla`
--
ALTER TABLE `detalle_planilla`
  MODIFY `id_detalle` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pago`
--
ALTER TABLE `pago`
  MODIFY `id_pago` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `planilla`
--
ALTER TABLE `planilla`
  MODIFY `id_planilla` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  MODIFY `id_vehiculo` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
