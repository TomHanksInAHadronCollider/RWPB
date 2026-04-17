-- Breached Organization: AcmeCorp Internal Database
-- Date of Breach: March 2026
-- Table: users

INSERT INTO users (id, username, email, password_hash, hash_type) VALUES
(1, 'jsmith', 'jsmith@acmecorp.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'md5'),
(2, 'ajones', 'ajones@acmecorp.com', 'e10adc3949ba59abbe56e057f20f883e', 'md5'),
(3, 'bwilson', 'bwilson@acmecorp.com', '25f9e794323b453885f5181f1b624d0b', 'md5'),
(4, 'mlee', 'mlee@acmecorp.com', '7c4a8d09ca3762af61e59520943dc26476143577', 'sha1'),
(5, 'tdavis', 'tdavis@acmecorp.com', 'f7c3bc1d808e04732adf679965ccc34ca7ae3441', 'sha1'),
(6, 'rgarcia', 'rgarcia@acmecorp.com', 'b1b3773a05c0ed0176787a4f1574ff0075f7521e', 'sha1'),
(7, 'kpatel', 'kpatel@acmecorp.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBPj/oG5KZ6S6', 'bcrypt'),
(8, 'nthompson', 'nthompson@acmecorp.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'bcrypt');

-- Hash reference (for documentation purposes only):
-- MD5 hashes:    password, 123456, 123456789
-- SHA-1 hashes:  password, abc123, iloveyou
-- bcrypt hashes: weak passwords intentionally chosen for demo
