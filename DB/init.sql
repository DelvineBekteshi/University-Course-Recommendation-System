-- 1. Tabela User (Sipas ERD: ID, Name, LastName, Email, Password, Role)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50)
);

-- 2. Tabela Course (Sipas ERD: ID, Title, Category, Description)
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT
);

-- 3. Tabela Enrollment (Lidh User me Course)
CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela Ratings (Lidh User me Course)
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    score INT CHECK (score >= 1 AND score <= 5)
);

-- 5. Tabela Recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    course_id INT REFERENCES courses(id),
    confidence_score FLOAT
);

-- 6. Tabela AuditLogs 
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);