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
# user: User
CREATE_USER = """
INSERT INTO users(username, email, password) VALUES(user.username, user.email, user.password);
"""
