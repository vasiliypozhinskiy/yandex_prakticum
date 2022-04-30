--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Debian 13.5-1.pgdg110+1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg20.04+1+b1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: auth_app
--

CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO auth_app;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: login_history; Type: TABLE; Schema: auth; Owner: auth_app
--

CREATE TABLE auth.login_history (
    id uuid NOT NULL,
    user_agent character varying(150) NOT NULL,
    refresh_token text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE auth.login_history OWNER TO auth_app;

--
-- Name: role; Type: TABLE; Schema: auth; Owner: auth_app
--

CREATE TABLE auth.role (
    title character varying(50) NOT NULL
);


ALTER TABLE auth.role OWNER TO auth_app;

--
-- Name: user; Type: TABLE; Schema: auth; Owner: auth_app
--

CREATE TABLE auth.user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    id uuid NOT NULL,
    login character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    is_superuser boolean NOT NULL
);


ALTER TABLE auth.user OWNER TO auth_app;

--
-- Name: user_data; Type: TABLE; Schema: auth; Owner: auth_app
--

CREATE TABLE auth.user_data (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    birthdate DATE
);

ALTER TABLE auth.user_data OWNER TO auth_app;


--
-- Name: user_role; Type: TABLE; Schema: auth; Owner: auth_app
--

CREATE TABLE auth.user_role (
    role_id character varying(50) NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE auth.user_role OWNER TO auth_app;

--
-- Name: login_history login_history_pkey; Type: CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.login_history
    ADD CONSTRAINT login_history_pkey PRIMARY KEY (id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (title);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.user
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_login_key; Type: CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.user
    ADD CONSTRAINT user_login_key UNIQUE (login);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.user
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: login_history_user_id_0eeaebb8; Type: INDEX; Schema: auth; Owner: auth_app
--

CREATE INDEX login_history_user_id_0eeaebb8 ON auth.login_history USING btree (user_id);


--
-- Name: role_title_c2f44585_like; Type: INDEX; Schema: auth; Owner: auth_app
--

CREATE INDEX role_title_c2f44585_like ON auth.role USING btree (title varchar_pattern_ops);


--
-- Name: user_login_3b007138_like; Type: INDEX; Schema: auth; Owner: auth_app
--

CREATE INDEX user_login_3b007138_like ON auth.user USING btree (login varchar_pattern_ops);


--
-- Name: login_history login_history_user_id_0eeaebb8_fk_user_id; Type: FK CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.login_history
    ADD CONSTRAINT login_history_user_id_0eeaebb8_fk_user_id FOREIGN KEY (user_id) REFERENCES auth.user(id) DEFERRABLE INITIALLY DEFERRED;

--
-- Name: user_data login_history_user_id_0eeaebb8_fk_user_id; Type: FK CONSTRAINT; Schema: auth; Owner: auth_app
--

ALTER TABLE ONLY auth.user_data
    ADD CONSTRAINT user_data_user_id_fk_user_id FOREIGN KEY (user_id) REFERENCES auth.user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

