CREATE TABLE IF NOT EXISTS "^dji-1m" (
    datetime TIMESTAMP PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
);

CREATE TABLE IF NOT EXISTS "^dji-3m" (
    datetime TIMESTAMP PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
);

CREATE TABLE IF NOT EXISTS "^dji-15m" (
    datetime TIMESTAMP PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
);

CREATE TABLE IF NOT EXISTS "^dji-1h" (
    datetime TIMESTAMP PRIMARY KEY,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
);