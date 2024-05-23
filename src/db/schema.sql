DROP TABLE IF EXISTS FoodItem;
DROP TABLE IF EXISTS EstimatedExpiry;


CREATE TABLE IF NOT EXISTS FoodItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    purchase_date DATE NOT NULL DEFAULT (DATE('now')),
    current_count INTEGER NOT NULL,
    actual_expiry DATE NOT NULL,
    estimated_expiry_id INTEGER,
    FOREIGN KEY (estimated_expiry_id) REFERENCES EstimatedExpiry(id)
);

CREATE TABLE IF NOT EXISTS EstimatedExpiry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL UNIQUE,
    estimated_days INTEGER NOT NULL
);
