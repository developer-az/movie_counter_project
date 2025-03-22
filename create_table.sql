CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    tickets_available INTEGER
);
