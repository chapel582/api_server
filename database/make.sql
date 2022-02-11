CREATE DATABASE illu_db;

\c illu_db;

CREATE SCHEMA my_schema;

CREATE TABLE my_schema.organization(
    id serial PRIMARY KEY,
    org_name character varying(100) NOT NULL UNIQUE
);

CREATE TABLE my_schema.illu_user(
    id serial PRIMARY KEY,
    phone_prefix character varying(8) NOT NULL,
    phone character varying(100) NOT NULL,
    UNIQUE(phone_prefix, phone),
    user_name character varying(100) NOT NULL,
    pw_hash character varying(256) NOT NULL,
    jwt character varying(512),
    org_id bigint,
    CONSTRAINT fk_org 
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id)
);