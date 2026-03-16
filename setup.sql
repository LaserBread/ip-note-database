DROP TABLE Entries;

CREATE TABLE IF NOT EXISTS Entries(
    id int NOT NULL UNIQUE AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    hostname varchar(63),
    ipv4 INT UNSIGNED,
    cidrmask INT UNSIGNED,
    mac varchar(17),
    notes text,
    CONSTRAINT chk_at_least_one_identifier
    CHECK (ipv4 IS NOT NULL OR hostname IS NOT NULL),
    CONSTRAINT chk_mac
    CHECK (mac IS NULL OR mac REGEXP '^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'),
    CONSTRAINT chk_cidr
    CHECK (cidrmask <=32)
);

INSERT INTO Entries (name, hostname, ipv4, cidrmask, mac, notes)
    VALUES('Router','MyGateway',INET_ATON('192.168.0.1'),24,"5F:50:DE:AD:BE:EF",'Example router setup for this thing');