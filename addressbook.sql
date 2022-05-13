DROP TABLE IF EXISTS contacts;

CREATE TABLE contacts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    phone TEXT NOT NULL
);

INSERT INTO contacts (first, last, phone)
VALUES 
    ('Paul','Deitel','(856) 555-2022'), 
    ('Harvey','Deitel','(856) 555-2020'),
    ('Abbey','Deitel','(609) 555-5981'), 
    ('Dan','Quirk','(609) 555-1092'),
    ('Alexander', 'Wald','(856) 555-0188');
