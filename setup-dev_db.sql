-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS usource_dev_db;
SET GLOBAL validate_password.policy=LOW;
CREATE USER IF NOT EXISTS 'usource_dev'@'localhost' IDENTIFIED BY 'usource_dev_pwd';
GRANT ALL PRIVILEGES ON `usource_dev_db`.* TO 'usource_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'usource_dev'@'localhost';
FLUSH PRIVILEGES;
