CREATE DATABASE illu_db;

\c illu_db;

CREATE SCHEMA my_schema;

CREATE TABLE my_schema.organization(
    id bigint NOT NULL,
    org_name character varying(100) NOT NULL,
    PRIMARY KEY(id)
);
CREATE SEQUENCE my_schema.organization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE my_schema.organization_id_seq OWNED BY my_schema.organization.id;

CREATE TABLE my_schema.illu_user(
    id bigint NOT NULL,
    phone_prefix character varying(8) NOT NULL,
    phone character varying(100) NOT NULL,
    user_name character varying(100) NOT NULL,
    pwhash character varying(256) NOT NULL,
    jwt character varying(512),
    user_role bigint,
    org_id bigint,
    PRIMARY KEY(id),
    CONSTRAINT fk_org 
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id)
);
CREATE SEQUENCE my_schema.illu_user_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE my_schema.illu_user_seq OWNED BY my_schema.illu_user.id;