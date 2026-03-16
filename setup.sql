CREATE TABLE IF NOT EXISTS Entries(
    id int NOT NULL UNIQUE AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    hostname varchar(63),
    ipv4 int,
    cidr int,
    ipv6 binary(16),
    mac bigint,
    notes text,
    CONSTRAINT chk_at_least_one_identifier
    CHECK (ipv4 IS NOT NULL OR hostname IS NOT NULL OR ipv6 IS NOT NULL)
);
