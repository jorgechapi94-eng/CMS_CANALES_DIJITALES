-- Portal CMS UPEC — DDL MySQL 8.0 (modelo 3FN corregido)
-- Charset institucional: utf8mb4

CREATE DATABASE IF NOT EXISTS upec_cms_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE upec_cms_db;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200) NULL
) ENGINE=InnoDB;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_users_email_domain CHECK (email LIKE '%@upec.edu.ec')
) ENGINE=InnoDB;

CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    slug VARCHAR(350) NOT NULL UNIQUE,
    content_html TEXT NOT NULL,
    excerpt VARCHAR(500) NULL,
    cover_image_url VARCHAR(500) NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    author_id INT NOT NULL,
    published_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_news_status CHECK (status IN ('draft', 'published', 'archived')),
    CONSTRAINT fk_news_author FOREIGN KEY (author_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE INDEX idx_news_status_published ON news (status, published_at);

CREATE TABLE news_categories (
    news_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (news_id, category_id),
    CONSTRAINT fk_news_categories_news
        FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE,
    CONSTRAINT fk_news_categories_category
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE newspapers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    pdf_url VARCHAR(500) NOT NULL,
    cover_thumbnail_url VARCHAR(500) NULL,
    uploaded_by INT NOT NULL,
    publication_date DATE NOT NULL,
    file_size_bytes INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_newspapers_uploader FOREIGN KEY (uploaded_by) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE INDEX idx_newspapers_pub_date ON newspapers (publication_date);

CREATE TABLE programs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    description TEXT NULL,
    modality VARCHAR(50) NOT NULL DEFAULT 'presencial',
    level VARCHAR(50) NOT NULL DEFAULT 'grado',
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_program_modality CHECK (modality IN ('presencial', 'virtual', 'hibrido')),
    CONSTRAINT chk_program_level CHECK (level IN ('grado', 'maestria', 'doctorado', 'tecnico'))
) ENGINE=InnoDB;

CREATE TABLE program_teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    title_degree VARCHAR(200) NULL,
    email VARCHAR(120) NULL,
    photo_url VARCHAR(500) NULL,
    CONSTRAINT fk_teachers_program
        FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE program_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    enrollment_year VARCHAR(4) NULL,
    CONSTRAINT fk_students_program
        FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE program_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT NULL,
    link_url VARCHAR(500) NULL,
    CONSTRAINT fk_projects_program
        FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO roles (name, description) VALUES
    ('superadmin', 'Gestión total del CMS, usuarios y configuración'),
    ('editor', 'CRUD de noticias y periódicos digitales'),
    ('gestor_programas', 'CRUD del directorio de programas académicos');
