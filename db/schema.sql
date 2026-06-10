--
-- PostgreSQL database dump
--

\restrict 2keIXHLrbzl3WEodNIom7fO2qy0I56Du2LTcSPVo0vJmtL35cgaXJEyO865H1Yo

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-05-29 01:37:28

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4914 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: noticias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.noticias (
    id integer NOT NULL,
    url text NOT NULL,
    title text,
    rawcontent text,
    extractdate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    processdate timestamp without time zone,
    processed boolean,
    tags json
);


ALTER TABLE public.noticias OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: noticias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.noticias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.noticias_id_seq OWNER TO postgres;

--
-- TOC entry 4916 (class 0 OID 0)
-- Dependencies: 219
-- Name: noticias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.noticias_id_seq OWNED BY public.noticias.id;


--
-- TOC entry 4756 (class 2604 OID 16393)
-- Name: noticias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticias ALTER COLUMN id SET DEFAULT nextval('public.noticias_id_seq'::regclass);


--
-- TOC entry 4759 (class 2606 OID 16399)
-- Name: noticias noticias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticias
    ADD CONSTRAINT noticias_pkey PRIMARY KEY (id);


--
-- TOC entry 4761 (class 2606 OID 16401)
-- Name: noticias noticias_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticias
    ADD CONSTRAINT noticias_url_key UNIQUE (url);


--
-- TOC entry 4915 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE noticias; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.noticias TO cyberscout;


--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE noticias_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.noticias_id_seq TO cyberscout;


--
-- TOC entry 2052 (class 826 OID 16403)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO cyberscout;


-- Completed on 2026-05-29 01:37:28

--
-- PostgreSQL database dump complete
--

\unrestrict 2keIXHLrbzl3WEodNIom7fO2qy0I56Du2LTcSPVo0vJmtL35cgaXJEyO865H1Yo

