CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO auth_app;

CREATE TABLE auth.test (
    id SERIAL PRIMARY KEY,
    testfield text
);

ALTER TABLE auth.test OWNER TO auth_app;

INSERT INTO auth.test (testfield) VALUES ('HELLO from postgres'), ('and from FLASK');