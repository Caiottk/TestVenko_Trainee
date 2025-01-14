CREATE TABLE system_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpu_usage FLOAT NOT NULL,
    mem_usage FLOAT NOT NULL,
    ip_address VARCHAR(255) NOT NULL,
    ping_latency FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
