
# Project Title: **SQL Fundamentals — Users & Products Relationship**

---

## Overview

This project introduces **intermediate-level SQL operations** focusing on data manipulation, filtering, aggregation, and relational concepts using a **Users ↔ Products** model.

Students will work with two core tables:

* `users` — representing system users.
* `products` — representing products owned by users.

The database will come pre-populated with sample data.
Students are **not expected to create the initial tables or seed data**, but must **perform queries, updates, and create new entries** according to the tasks provided.

---

## Database Schema

### 🧍`users` Table

| Column       | Type                                                            | Description          |
| ------------ | --------------------------------------------------------------- | -------------------- |
| `id`         | INT (PK, AUTO_INCREMENT)                                        | Unique user ID       |
| `first_name` | VARCHAR(50)                                                     | User’s first name    |
| `last_name`  | VARCHAR(50)                                                     | User’s last name     |
| `email`      | VARCHAR(100), UNIQUE                                            | User’s email address |
| `gender`     | CHAR(1), CHECK (‘M’, ‘F’)                                       | User’s gender        |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP                             | Record creation time |
| `updated_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Record update time   |

---

### `products` Table

| Column         | Type                                                            | Description            |
| -------------- | --------------------------------------------------------------- | ---------------------- |
| `id`           | INT (PK, AUTO_INCREMENT)                                        | Unique product ID      |
| `user_id`      | INT (FK → users.id)                                             | Owner of the product   |
| `product_name` | VARCHAR(100)                                                    | Name of the product    |
| `quantity`     | INT                                                             | Quantity in stock      |
| `unit_price`   | DECIMAL(10,2)                                                   | Price per unit         |
| `created_at`   | TIMESTAMP DEFAULT CURRENT_TIMESTAMP                             | Creation time          |
| `updated_at`   | TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Last modification time |

---

## Database Creation Script

### Task1: Create users table to conform with required fields
### Task 2: Insert 20 Users

(*Pre-populated — students won’t modify this initially*)

```sql
INSERT INTO users (first_name, last_name, email, gender) VALUES
('Alice', 'Johnson', 'alice@example.com', 'F'),
('Benjamin', 'Smith', 'benjamin@example.com', 'M'),
('Chidera', 'Okafor', 'chidera@example.com', 'F'),
('David', 'George', 'david@example.com', 'M'),
('Emily', 'Adams', 'emily@example.com', 'F'),
('Frank', 'Adeyemi', 'frank@example.com', 'M'),
('Grace', 'Lawal', 'grace@example.com', 'F'),
('Henry', 'Ogunleye', 'henry@example.com', 'M'),
('Ifeoma', 'Ojo', 'ifeoma@example.com', 'F'),
('John', 'Eze', 'john@example.com', 'M'),
('Kemi', 'Afolabi', 'kemi@example.com', 'F'),
('Luka', 'Bello', 'luka@example.com', 'M'),
('Mary', 'Ogunbiyi', 'mary@example.com', 'F'),
('Nathan', 'Olawale', 'nathan@example.com', 'M'),
('Oluwatobi', 'Okon', 'oluwatobi@example.com', 'M'),
('Peace', 'Anyanwu', 'peace@example.com', 'F'),
('Queen', 'Mohammed', 'queen@example.com', 'F'),
('Richard', 'Adeniran', 'richard@example.com', 'M'),
('Stella', 'Ibrahim', 'stella@example.com', 'F'),
('Tunde', 'Adewale', 'tunde@example.com', 'M');
```

---

### 3️⃣ Insert 500 Products

To avoid manual repetition, you can use a **loop or random generator** (for SQL instructors):

Example (MySQL procedure):

```sql
DELIMITER //
CREATE PROCEDURE populate_products()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE userId INT;
    WHILE i <= 500 DO
        SET userId = FLOOR(1 + RAND() * 20);
        INSERT INTO products (user_id, product_name, quantity, unit_price, created_at)
        VALUES (
            userId,
            CONCAT('Product_', i),
            FLOOR(1 + RAND() * 100),
            ROUND(10 + RAND() * 1000, 2),
            NOW() - INTERVAL FLOOR(RAND() * 365) DAY
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

CALL populate_products();
```

This gives each user a variety of products created on random dates, with realistic prices and quantities.

---

## 🎯 STUDENT TASKS

Each student should **fork or clone** the repo and complete the following tasks.

---

### Task 3: Get Products by a Particular Quantity

> Retrieve all products that have a specific quantity (e.g., 50 units).
---

### Task 4: Get Products Created Within a Date Range

> Find all products created between January 1, 2025, and March 31, 2025.

---

### Task 5: Sum Quantity Based on Product Name

> Compute the total quantity available for each product name.

---

### Task 6: Calculate Total Stock Value per User

> For each user, calculate the total stock value = `(quantity * unit_price)`.

---

### Task 7: Update Product or User Records

> Example 1: Update all products below quantity 5 to quantity 10.

> Example 2: Update user email format to a new domain: `@dbmaniac.com`

---

### Task 8: Order and Group by Creation Date

> Get all products grouped by creation date, showing count per day.

---

## MORE TASKS

1. Add a **new user** and at least **5 products** for them.
2. Delete all products created before a specific year.
3. Find the **average price** of products per user.
4. Identify the **top 5 users** with the highest total product stock value.