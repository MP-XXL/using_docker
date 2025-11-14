from ..models.models import User
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username VARCHAR(25) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL  
);
"""
CREATE_USER = """
INSERT INTO users(username, email, password) VALUES(%s, %s, %s);
"""

CREATE_POSTS_TABLE = """
CREATE TABLE IF NOT EXISTS posts(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    title VARCHAR(255) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

CREATE_POST = """
INSERT INTO posts(title, user_id) VALUES(%s, %s);
"""
UPDATE_POST = """
UPDATE posts SET title = %s WHERE user_id = %s;
"""
GET_ALL_POSTS = """
SELECT * FROM posts;
"""

UPDATE_USER = """
UPDATE users SET username = %s,  email = %s, password = %s WHERE id = %s ;
"""
DELETE_USER = """
DELETE FROM users WHERE id = %s;
"""

GET_ALL_USERS = """
SELECT id, username, email FROM users;
"""
