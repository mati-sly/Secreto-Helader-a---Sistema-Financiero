-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: mysql-container:3306
-- Tiempo de generación: 25-09-2025 a las 15:59:02
-- Versión del servidor: 9.4.0
-- Versión de PHP: 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `secreto_heladeria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add categoria', 7, 'add_categoria'),
(26, 'Can change categoria', 7, 'change_categoria'),
(27, 'Can delete categoria', 7, 'delete_categoria'),
(28, 'Can view categoria', 7, 'view_categoria'),
(29, 'Can add producto', 8, 'add_producto'),
(30, 'Can change producto', 8, 'change_producto'),
(31, 'Can delete producto', 8, 'delete_producto'),
(32, 'Can view producto', 8, 'view_producto'),
(33, 'Can add transaccion', 9, 'add_transaccion'),
(34, 'Can change transaccion', 9, 'change_transaccion'),
(35, 'Can delete transaccion', 9, 'delete_transaccion'),
(36, 'Can view transaccion', 9, 'view_transaccion'),
(37, 'Can add Código de Recuperación', 10, 'add_codigorecuperacion'),
(38, 'Can change Código de Recuperación', 10, 'change_codigorecuperacion'),
(39, 'Can delete Código de Recuperación', 10, 'delete_codigorecuperacion'),
(40, 'Can view Código de Recuperación', 10, 'view_codigorecuperacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_spanish_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_spanish_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$Lr9O413TyZ4jxN90NDz0CQ$+Aq/SBctrTiM8SiKCs7y8oCv6PDuJnIBiiwk2wv4iHI=', '2025-09-25 14:54:00.632619', 1, 'Matias', '', '', 'matias34890@gmail.com', 1, 1, '2025-09-25 01:38:05.853232');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_spanish_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_spanish_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_spanish_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'finanzas', 'categoria'),
(10, 'finanzas', 'codigorecuperacion'),
(8, 'finanzas', 'producto'),
(9, 'finanzas', 'transaccion'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-09-25 01:13:32.462446'),
(2, 'auth', '0001_initial', '2025-09-25 01:13:33.082448'),
(3, 'admin', '0001_initial', '2025-09-25 01:13:33.221330'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-09-25 01:13:33.228842'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-25 01:13:33.238603'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-09-25 01:13:33.333652'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-09-25 01:13:33.396353'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-09-25 01:13:33.431547'),
(9, 'auth', '0004_alter_user_username_opts', '2025-09-25 01:13:33.439043'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-09-25 01:13:33.497547'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-09-25 01:13:33.503753'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-09-25 01:13:33.511667'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-09-25 01:13:33.575020'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-09-25 01:13:33.641173'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-09-25 01:13:33.666302'),
(16, 'auth', '0011_update_proxy_permissions', '2025-09-25 01:13:33.675286'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-09-25 01:13:33.737812'),
(18, 'finanzas', '0001_initial', '2025-09-25 01:13:33.912086'),
(19, 'finanzas', '0002_codigorecuperacion', '2025-09-25 01:13:33.939847'),
(20, 'sessions', '0001_initial', '2025-09-25 01:13:33.982675');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_spanish_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_spanish_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('kbnmsv0xrow7dz6ux6pw50tw8x1in40e', '.eJxVjDsOwjAQBe_iGll2jNe7lPQ5g7X-4QBypDipEHeHSCmgfTPzXsLztla_9bz4KYmL0OL0uwWOj9x2kO7cbrOMc1uXKchdkQftcpxTfl4P9--gcq_fujgqTFQiWEYqNhij6UzRRYQBjeOABEUrUOBUsAjGDZw0JmCOCot4fwDXcDdr:1v1nM8:XeCCsCQ9n1Zmfr-wDDmBRVBhHJCm5-cOFqMhDbX88IE', '2025-10-09 14:54:00.636551');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `finanzas_categoria`
--

CREATE TABLE `finanzas_categoria` (
  `id` bigint NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `tipo` varchar(10) COLLATE utf8mb4_spanish_ci NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `finanzas_categoria`
--

INSERT INTO `finanzas_categoria` (`id`, `nombre`, `tipo`, `created_at`) VALUES
(1, 'Helados', 'Producto', NULL),
(2, 'Bebidas', 'Producto', NULL),
(3, 'Snacks', 'Producto', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `finanzas_codigorecuperacion`
--

CREATE TABLE `finanzas_codigorecuperacion` (
  `id` bigint NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_spanish_ci NOT NULL,
  `codigo` varchar(4) COLLATE utf8mb4_spanish_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `usado` tinyint(1) NOT NULL,
  `intentos` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `finanzas_producto`
--

CREATE TABLE `finanzas_producto` (
  `id` bigint NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `categoria` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `costo_unitario` decimal(8,2) NOT NULL,
  `precio_venta` decimal(8,2) NOT NULL,
  `stock` int NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `finanzas_producto`
--

INSERT INTO `finanzas_producto` (`id`, `nombre`, `categoria`, `costo_unitario`, `precio_venta`, `stock`, `activo`) VALUES
(1, 'Helado Vainilla', 'Helados', 500.00, 1000.00, 10, 1),
(2, 'Helado Chocolate', 'Helados', 600.00, 1200.00, 15, 1),
(3, 'Helado Frutilla', 'Helados', 550.00, 1100.00, 12, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `finanzas_transaccion`
--

CREATE TABLE `finanzas_transaccion` (
  `id` bigint NOT NULL,
  `tipo` varchar(10) COLLATE utf8mb4_spanish_ci NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `categoria_id` bigint NOT NULL,
  `usuario_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `finanzas_transaccion`
--

INSERT INTO `finanzas_transaccion` (`id`, `tipo`, `monto`, `descripcion`, `fecha`, `categoria_id`, `usuario_id`) VALUES
(1, 'Venta', 2000.00, 'Helado Chocolate', '2025-09-25 01:42:37.000000', 1, 1),
(2, 'Venta', 700.00, 'Jugo Naranja', '2025-09-25 01:42:37.000000', 2, 1),
(3, 'Venta', 1500.00, 'Snack Chips', '2025-09-25 01:42:37.000000', 3, 1),
(4, 'Venta', 2000.00, 'Helado Chocolate', '2025-09-25 01:48:29.000000', 1, 1),
(5, 'Venta', 1500.00, 'Helado Vainilla', '2025-09-25 01:48:29.000000', 1, 1),
(6, 'Venta', 1800.00, 'Helado Fresa', '2025-09-25 01:48:29.000000', 1, 1),
(7, 'Gasto', 500.00, 'Compra de toppings', '2025-09-25 01:48:29.000000', 1, 1),
(8, 'Gasto', 300.00, 'Compra de conos', '2025-09-25 01:48:29.000000', 1, 1),
(9, 'Gasto', 200.00, 'Compra de servilletas', '2025-09-25 01:48:29.000000', 1, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `finanzas_categoria`
--
ALTER TABLE `finanzas_categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `finanzas_codigorecuperacion`
--
ALTER TABLE `finanzas_codigorecuperacion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `finanzas_producto`
--
ALTER TABLE `finanzas_producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `finanzas_transaccion`
--
ALTER TABLE `finanzas_transaccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finanzas_transaccion_categoria_id_67c59f21_fk_finanzas_` (`categoria_id`),
  ADD KEY `finanzas_transaccion_usuario_id_b6aebf5e_fk_auth_user_id` (`usuario_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `finanzas_categoria`
--
ALTER TABLE `finanzas_categoria`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `finanzas_codigorecuperacion`
--
ALTER TABLE `finanzas_codigorecuperacion`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `finanzas_producto`
--
ALTER TABLE `finanzas_producto`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `finanzas_transaccion`
--
ALTER TABLE `finanzas_transaccion`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `finanzas_transaccion`
--
ALTER TABLE `finanzas_transaccion`
  ADD CONSTRAINT `finanzas_transaccion_categoria_id_67c59f21_fk_finanzas_` FOREIGN KEY (`categoria_id`) REFERENCES `finanzas_categoria` (`id`),
  ADD CONSTRAINT `finanzas_transaccion_usuario_id_b6aebf5e_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
