/* create.sql */
/* users tables */
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

/* covid-symptom table */
CREATE TABLE symptoms (
    subject_id SERIAL PRIMARY KEY,
    age INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    height INTEGER NOT NULL,
    temperature FLOAT NOT NULL,
    sp02 INTEGER NOT NULL,
    gender INTEGER NOT NULL,
    fever INTEGER NOT NULL,
    cough INTEGER NOT NULL,
    runny_nose INTEGER NOT NULL,
    headache INTEGER NOT NULL,
    muscle_aches INTEGER NOT NULL,
    fatigue INTEGER NOT NULL
);

/* predictions table */
CREATE TABLE predictions  (
    id SERIAL PRIMARY KEY,
    prediction INTEGER NOT NULL,
    subject_id INTEGER REFERENCES symptoms(subject_id)
);
