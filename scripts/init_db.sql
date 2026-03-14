-- PostgreSQL schema for ASYLUM MVP
CREATE TABLE IF NOT EXISTS help_requests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    help_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    contact_info VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ngos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    services VARCHAR(500) NOT NULL,
    location VARCHAR(255) NOT NULL,
    contact_info VARCHAR(500) NOT NULL
);
