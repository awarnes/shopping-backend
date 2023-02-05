CREATE TABLE IF NOT EXISTS patch_history (
    patch_name TEXT NOT NULL,
    date_applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    products TEXT NULL,
    roles TEXT NOT NULL,
    preferences TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lists (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NULL,
    products TEXT NULL,
    owners TEXT NULL,
    subscribers TEXT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    tags TEXT NULL,
    brand TEXT NOT NULL,
    sku TEXT NOT NULL,
    location TEXT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY NOT NULL,
    brand TEXT NOT NULL,
    name TEXT NOT NULL,
    store_id TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert base TJ values into DB
INSERT INTO stores (brand, name, store_id, address, phone)
VALUES
    ("TRADER_JOES", "Trader Joe's Portland - Hollywood", "144", "4121 NE Halsey St\nPortland, OR 97232", "503-284-4232"),
    ("TRADER_JOES", "Trader Joe's Portland SE", "143", "4715 SE Cesar Chavez Blvd\nPortland, OR 97202", "503-777-1601"),
    ("TRADER_JOES", "Trader Joe's Clackamas", "152", "9345 SE 82nd Ave\nClackamas, OR 97086", "503-771-6300"),
    ("TRADER_JOES", "Trader Joe's Portland NW", "146", "2122 NW Glisan St\nPortland, OR 97210", "971-544-0788");