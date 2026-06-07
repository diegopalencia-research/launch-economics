-- ============================================================
-- PROJECT ALPHA: LAUNCH ECONOMICS
-- Sacred Database Schema for SpaceX Falcon 9 Analysis
-- ============================================================

-- Create database
CREATE DATABASE IF NOT EXISTS spacex_launch_economics;
USE spacex_launch_economics;

-- ============================================================
-- TABLE 1: LAUNCHES (Core Fact Table)
-- ============================================================
CREATE TABLE IF NOT EXISTS launches (
    flight_number INT PRIMARY KEY,
    launch_date DATE NOT NULL,
    booster_version VARCHAR(50) NOT NULL,
    payload_mass_kg DECIMAL(10,2),
    orbit_type VARCHAR(20) NOT NULL,
    launch_site VARCHAR(50) NOT NULL,
    outcome VARCHAR(50),
    grid_fins BOOLEAN DEFAULT FALSE,
    reused BOOLEAN DEFAULT FALSE,
    legs BOOLEAN DEFAULT FALSE,
    landing_pad VARCHAR(50),
    block_version DECIMAL(3,1),
    reused_count INT DEFAULT 0,
    serial_number VARCHAR(20),
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),
    launch_year INT GENERATED ALWAYS AS (YEAR(launch_date)) STORED,
    launch_month INT GENERATED ALWAYS AS (MONTH(launch_date)) STORED,
    launch_quarter INT GENERATED ALWAYS AS (QUARTER(launch_date)) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE 2: ECONOMICS (Cost Analysis Dimension)
-- ============================================================
CREATE TABLE IF NOT EXISTS economics (
    flight_number INT PRIMARY KEY,
    estimated_cost_million DECIMAL(6,2) DEFAULT 62.00,
    competitor_cost_million DECIMAL(6,2) DEFAULT 165.00,
    cost_per_kg DECIMAL(12,2),
    cumulative_savings_million DECIMAL(10,2),
    FOREIGN KEY (flight_number) REFERENCES launches(flight_number)
);

-- ============================================================
-- TABLE 3: PERFORMANCE METRICS (Success & Learning Curve)
-- ============================================================
CREATE TABLE IF NOT EXISTS performance_metrics (
    flight_number INT PRIMARY KEY,
    success BOOLEAN,
    days_since_first_launch INT,
    cumulative_launches INT,
    rolling_success_rate DECIMAL(5,4),
    FOREIGN KEY (flight_number) REFERENCES launches(flight_number)
);

-- ============================================================
-- TABLE 4: ORBITAL CLASSIFICATION (Dimension Table)
-- ============================================================
CREATE TABLE IF NOT EXISTS orbital_classification (
    orbit_type VARCHAR(20) PRIMARY KEY,
    altitude_km_min DECIMAL(8,2),
    altitude_km_max DECIMAL(8,2),
    inclination_degrees DECIMAL(5,2),
    typical_payload_mass_kg DECIMAL(10,2),
    mission_complexity_score INT CHECK (mission_complexity_score BETWEEN 1 AND 10),
    description TEXT
);

-- ============================================================
-- TABLE 5: LAUNCH SITES (Dimension Table)
-- ============================================================
CREATE TABLE IF NOT EXISTS launch_sites (
    site_name VARCHAR(50) PRIMARY KEY,
    site_code VARCHAR(20),
    location VARCHAR(100),
    country VARCHAR(50),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    first_launch_date DATE,
    total_launches INT DEFAULT 0,
    success_rate DECIMAL(5,4),
    operational_status VARCHAR(20) DEFAULT 'Active'
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_launch_date ON launches(launch_date);
CREATE INDEX idx_orbit ON launches(orbit_type);
CREATE INDEX idx_launch_site ON launches(launch_site);
CREATE INDEX idx_reused ON launches(reused);
CREATE INDEX idx_year ON launches(launch_year);
CREATE INDEX idx_block ON launches(block_version);

-- ============================================================
-- VIEWS FOR ANALYTICS
-- ============================================================

-- View 1: Annual Launch Summary
CREATE OR REPLACE VIEW v_annual_summary AS
SELECT 
    launch_year AS year,
    COUNT(*) AS total_launches,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful_launches,
    ROUND(AVG(CASE WHEN success THEN 1 ELSE 0 END) * 100, 2) AS success_rate_pct,
    ROUND(AVG(payload_mass_kg), 2) AS avg_payload_mass_kg,
    SUM(CASE WHEN reused THEN 1 ELSE 0 END) AS reused_boosters,
    ROUND(AVG(e.cost_per_kg), 2) AS avg_cost_per_kg,
    ROUND(SUM(e.competitor_cost_million - e.estimated_cost_million), 2) AS annual_savings_million
FROM launches l
LEFT JOIN performance_metrics p ON l.flight_number = p.flight_number
LEFT JOIN economics e ON l.flight_number = e.flight_number
GROUP BY launch_year
ORDER BY launch_year;

-- View 2: Reusability Economics
CREATE OR REPLACE VIEW v_reusability_economics AS
SELECT 
    reused_count,
    COUNT(*) AS flight_count,
    ROUND(AVG(CASE WHEN success THEN 1 ELSE 0 END) * 100, 2) AS success_rate_pct,
    ROUND(AVG(e.cost_per_kg), 2) AS avg_cost_per_kg,
    ROUND(MIN(e.cost_per_kg), 2) AS min_cost_per_kg,
    ROUND(MAX(e.cost_per_kg), 2) AS max_cost_per_kg,
    ROUND(AVG(payload_mass_kg), 2) AS avg_payload_mass_kg
FROM launches l
LEFT JOIN performance_metrics p ON l.flight_number = p.flight_number
LEFT JOIN economics e ON l.flight_number = e.flight_number
GROUP BY reused_count
ORDER BY reused_count;

-- View 3: Orbital Performance Matrix
CREATE OR REPLACE VIEW v_orbital_performance AS
SELECT 
    orbit_type,
    COUNT(*) AS total_missions,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful_missions,
    ROUND(AVG(CASE WHEN success THEN 1 ELSE 0 END) * 100, 2) AS success_rate_pct,
    ROUND(AVG(payload_mass_kg), 2) AS avg_payload_mass_kg,
    ROUND(AVG(e.cost_per_kg), 2) AS avg_cost_per_kg,
    ROUND(AVG(block_version), 2) AS avg_block_version
FROM launches l
LEFT JOIN performance_metrics p ON l.flight_number = p.flight_number
LEFT JOIN economics e ON l.flight_number = e.flight_number
GROUP BY orbit_type
ORDER BY success_rate_pct DESC;

-- View 4: Launch Site Analytics
CREATE OR REPLACE VIEW v_site_analytics AS
SELECT 
    launch_site,
    COUNT(*) AS total_launches,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful_launches,
    ROUND(AVG(CASE WHEN success THEN 1 ELSE 0 END) * 100, 2) AS success_rate_pct,
    ROUND(AVG(payload_mass_kg), 2) AS avg_payload_mass_kg,
    SUM(CASE WHEN reused THEN 1 ELSE 0 END) AS reused_launches,
    ROUND(AVG(e.cost_per_kg), 2) AS avg_cost_per_kg,
    MIN(launch_date) AS first_launch,
    MAX(launch_date) AS latest_launch
FROM launches l
LEFT JOIN performance_metrics p ON l.flight_number = p.flight_number
LEFT JOIN economics e ON l.flight_number = e.flight_number
GROUP BY launch_site
ORDER BY total_launches DESC;

-- View 5: The Learning Curve (Cumulative Metrics)
CREATE OR REPLACE VIEW v_learning_curve AS
SELECT 
    flight_number,
    launch_date,
    days_since_first_launch,
    cumulative_launches,
    rolling_success_rate,
    payload_mass_kg,
    reused,
    reused_count,
    block_version,
    e.cost_per_kg,
    e.cumulative_savings_million
FROM launches l
LEFT JOIN performance_metrics p ON l.flight_number = p.flight_number
LEFT JOIN economics e ON l.flight_number = e.flight_number
ORDER BY flight_number;
