-- One schema + least-privilege user per MySQL-backed service (dev passwords only).
CREATE DATABASE IF NOT EXISTS identity;
CREATE USER IF NOT EXISTS 'identity'@'%' IDENTIFIED BY 'identity';
GRANT ALL PRIVILEGES ON identity.* TO 'identity'@'%';
FLUSH PRIVILEGES;
