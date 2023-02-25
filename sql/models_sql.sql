
-- Create model Dashboard
CREATE TABLE `dashboard` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_statistics` json NULL,
    `inventory_statistics` json NULL,
    `menu_statistics` json NULL);

-- Create model Inventory
CREATE TABLE `inventory` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ingredient` varchar(30) NOT NULL, 
    `slug` varchar(30) NOT NULL UNIQUE,
    `quantity` integer NOT NULL,
    `unit_price` numeric(5, 2) NOT NULL,
    `image` varchar(100) NOT NULL);

-- Create model Menu
CREATE TABLE `menu` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(50) NOT NULL,
    `slug` varchar(30) NOT NULL UNIQUE,
    `image` varchar(100) NULL,
    `description` longtext NOT NULL,
    `ingredients_cost` numeric(5, 2) NOT NULL,
    `price` numeric(5, 2) NULL);

-- Create model Order
CREATE TABLE `orders` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `notes` varchar(300) NULL,
    `ordered_at` datetime(6) NOT NULL,
    `prepared` bool NOT NULL,
    `prepared_at` datetime(6) NULL,
    `delivered` bool NOT NULL,
    `delivered_at` datetime(6) NULL,
    `complete` bool NULL);

-- Create model OrderMenu
CREATE TABLE `orders_menu` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `quantity` smallint UNSIGNED NULL CHECK (`quantity` >= 0),
    `menu_id` bigint NOT NULL,
    `order_id` bigint NOT NULL);

-- Create model MenuInventory
CREATE TABLE `menu_inventory` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `units` numeric(5, 2) NULL,
    `inventory_id` bigint NOT NULL,
    `menu_id` bigint NOT NULL);

-- Add foreign key constraints for orders_menu custom through model
ALTER TABLE `orders_menu` 
    ADD CONSTRAINT `orders_menu_menu_id_6bfc8338_fk_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`);
ALTER TABLE `orders_menu`
    ADD CONSTRAINT `orders_menu_order_id_047664ae_fk_orders_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

-- Add foreign key constraints for menu_inventory custom through model
ALTER TABLE `menu_inventory`
    ADD CONSTRAINT `menu_inventory_inventory_id_66ebb2e0_fk_inventory_id` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`id`);
ALTER TABLE `menu_inventory`
    ADD CONSTRAINT `menu_inventory_menu_id_68ab330b_fk_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`);

-- Create model MyUser
CREATE TABLE `myuser` (
    `password` varchar(128) NOT NULL, 
    `last_login` datetime(6) NULL,
    `is_superuser` bool NOT NULL,
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `email` varchar(255) NOT NULL UNIQUE,
    `is_active` bool NOT NULL,
    `is_admin` bool NOT NULL,
    `is_staff` bool NOT NULL);

-- Create through model myuser_groups
CREATE TABLE `myuser_groups` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `myuser_id` bigint NOT NULL,
    `group_id` integer NOT NULL);

-- Create through model myuser_user_permissions
CREATE TABLE `myuser_user_permissions` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `myuser_id` bigint NOT NULL,
    `permission_id` integer NOT NULL);

-- Create model MyStaff
CREATE TABLE `mystaff` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `join_date` date NOT NULL,
    `role` varchar(50) NOT NULL,
    `staff_id` bigint NOT NULL UNIQUE);


-- Add my_user_groups foreign key constraints
ALTER TABLE `myuser_groups` ADD CONSTRAINT `myuser_groups_myuser_id_55ad36f0_fk_myuser_id` FOREIGN KEY (`myuser_id`) REFERENCES `myuser` (`id`);
ALTER TABLE `myuser_groups` ADD CONSTRAINT `myuser_groups_group_id_855619de_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `myuser_groups` ADD CONSTRAINT `myuser_groups_myuser_id_group_id_b128f544_uniq` UNIQUE (`myuser_id`, `group_id`);


-- Add my_user_permissions foreign key constraints
ALTER TABLE `myuser_user_permissions` ADD CONSTRAINT `myuser_user_permissions_myuser_id_89619f91_fk_myuser_id` FOREIGN KEY (`myuser_id`) REFERENCES `myuser` (`id`);
ALTER TABLE `myuser_user_permissions` ADD CONSTRAINT `myuser_user_permissi_permission_id_a0204c78_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `myuser_user_permissions` ADD CONSTRAINT `myuser_user_permissions_myuser_id_permission_id_f71501c6_uniq` UNIQUE (`myuser_id`, `permission_id`);

-- Add foreign key constraint
ALTER TABLE `mystaff` ADD CONSTRAINT `mystaff_staff_id_a85f2966_fk_myuser_id` FOREIGN KEY (`staff_id`) REFERENCES `myuser` (`id`);

