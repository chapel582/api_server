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

CREATE TABLE my_schema.site(
    id serial PRIMARY KEY,
    name character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    org_id integer NOT NULL,
    UNIQUE(org_id, name),
    CONSTRAINT fk_org
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id) 
);

CREATE TABLE my_schema.job_type_tag(
    id serial PRIMARY KEY,
    name character varying(32),
    org_id integer,
    UNIQUE(org_id, name),
    CONSTRAINT fk_org
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id)
);

CREATE TABLE my_schema.job_status(
    id serial PRIMARY KEY,
    name character varying(32),
    org_id integer,
    UNIQUE(org_id, name),
    CONSTRAINT fk_org
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id)
);

CREATE TABLE my_schema.user_job(
    id serial PRIMARY KEY,
    job_name character varying(100) NOT NULL,
    status smallint DEFAULT 0,
    type_tag integer NOT NULL,
    org_id integer NOT NULL,
    site_id integer NOT NULL,
    due_date date NOT NULL,
    assigned_user_id integer NOT NULL,
    manager_user_id integer NOT NULL,
    notes character varying(512),
    repeat_interval_type smallint,
    repeat_interval_num smallint,

    CONSTRAINT fk_assigned_user
        FOREIGN KEY(assigned_user_id)
        REFERENCES my_schema.illu_user(id),
    CONSTRAINT fk_manager_user_id
        FOREIGN KEY(manager_user_id)
        REFERENCES my_schema.illu_user(id),
    CONSTRAINT fk_org
        FOREIGN KEY(org_id)
        REFERENCES my_schema.organization(id),
    CONSTRAINT fk_site
        FOREIGN KEY(site_id)
        REFERENCES my_schema.site(id),
    CONSTRAINT fk_status
        FOREIGN KEY(status)
        REFERENCES my_schema.job_status(id),
    CONSTRAINT fk_type_tag
        FOREIGN KEY(type_tag)
        REFERENCES my_schema.job_type_tag
);