--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: kasi_cache; Type: TABLE; Schema: public; Owner: heal7_user
--

CREATE TABLE public.kasi_cache (
    id integer NOT NULL,
    year integer NOT NULL,
    month integer NOT NULL,
    solar_terms jsonb NOT NULL,
    lunar_calendar jsonb,
    data_source text DEFAULT 'kasi_api'::text NOT NULL,
    cache_expires_at timestamp(3) without time zone NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.kasi_cache OWNER TO heal7_user;

--
-- Name: kasi_cache_id_seq; Type: SEQUENCE; Schema: public; Owner: heal7_user
--

CREATE SEQUENCE public.kasi_cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kasi_cache_id_seq OWNER TO heal7_user;

--
-- Name: kasi_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: heal7_user
--

ALTER SEQUENCE public.kasi_cache_id_seq OWNED BY public.kasi_cache.id;


--
-- Name: saju_interpretations; Type: TABLE; Schema: public; Owner: heal7_user
--

CREATE TABLE public.saju_interpretations (
    id integer NOT NULL,
    saju_result_id integer NOT NULL,
    personality_analysis text,
    wealth_analysis text,
    health_analysis text,
    relationship_analysis text,
    lifecycle_analysis jsonb,
    compatibility_notes text,
    recommendation text,
    ai_generated boolean DEFAULT false NOT NULL,
    analysis_source text DEFAULT 'frontend'::text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL
);


ALTER TABLE public.saju_interpretations OWNER TO heal7_user;

--
-- Name: saju_interpretations_id_seq; Type: SEQUENCE; Schema: public; Owner: heal7_user
--

CREATE SEQUENCE public.saju_interpretations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saju_interpretations_id_seq OWNER TO heal7_user;

--
-- Name: saju_interpretations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: heal7_user
--

ALTER SEQUENCE public.saju_interpretations_id_seq OWNED BY public.saju_interpretations.id;


--
-- Name: saju_results; Type: TABLE; Schema: public; Owner: heal7_user
--

CREATE TABLE public.saju_results (
    id integer NOT NULL,
    user_id integer,
    name text NOT NULL,
    birth_year integer NOT NULL,
    birth_month integer NOT NULL,
    birth_day integer NOT NULL,
    birth_hour integer NOT NULL,
    birth_minute integer DEFAULT 0 NOT NULL,
    gender text DEFAULT 'unknown'::text NOT NULL,
    year_pillar jsonb NOT NULL,
    month_pillar jsonb NOT NULL,
    day_pillar jsonb NOT NULL,
    hour_pillar jsonb NOT NULL,
    wuxing_analysis jsonb NOT NULL,
    sipsin_analysis jsonb NOT NULL,
    calculation_engine text DEFAULT 'frontend'::text NOT NULL,
    accuracy_score integer DEFAULT 95 NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL
);


ALTER TABLE public.saju_results OWNER TO heal7_user;

--
-- Name: saju_results_id_seq; Type: SEQUENCE; Schema: public; Owner: heal7_user
--

CREATE SEQUENCE public.saju_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saju_results_id_seq OWNER TO heal7_user;

--
-- Name: saju_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: heal7_user
--

ALTER SEQUENCE public.saju_results_id_seq OWNED BY public.saju_results.id;


--
-- Name: system_settings; Type: TABLE; Schema: public; Owner: heal7_user
--

CREATE TABLE public.system_settings (
    id integer NOT NULL,
    setting_key text NOT NULL,
    setting_value jsonb NOT NULL,
    setting_type text NOT NULL,
    description text,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL
);


ALTER TABLE public.system_settings OWNER TO heal7_user;

--
-- Name: system_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: heal7_user
--

CREATE SEQUENCE public.system_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_settings_id_seq OWNER TO heal7_user;

--
-- Name: system_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: heal7_user
--

ALTER SEQUENCE public.system_settings_id_seq OWNED BY public.system_settings.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: heal7_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email text,
    name text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    preferences jsonb DEFAULT '{}'::jsonb NOT NULL,
    user_mode text DEFAULT 'simple'::text NOT NULL
);


ALTER TABLE public.users OWNER TO heal7_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: heal7_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO heal7_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: heal7_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: kasi_cache id; Type: DEFAULT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.kasi_cache ALTER COLUMN id SET DEFAULT nextval('public.kasi_cache_id_seq'::regclass);


--
-- Name: saju_interpretations id; Type: DEFAULT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_interpretations ALTER COLUMN id SET DEFAULT nextval('public.saju_interpretations_id_seq'::regclass);


--
-- Name: saju_results id; Type: DEFAULT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_results ALTER COLUMN id SET DEFAULT nextval('public.saju_results_id_seq'::regclass);


--
-- Name: system_settings id; Type: DEFAULT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.system_settings ALTER COLUMN id SET DEFAULT nextval('public.system_settings_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: kasi_cache; Type: TABLE DATA; Schema: public; Owner: heal7_user
--

COPY public.kasi_cache (id, year, month, solar_terms, lunar_calendar, data_source, cache_expires_at, created_at) FROM stdin;
\.


--
-- Data for Name: saju_interpretations; Type: TABLE DATA; Schema: public; Owner: heal7_user
--

COPY public.saju_interpretations (id, saju_result_id, personality_analysis, wealth_analysis, health_analysis, relationship_analysis, lifecycle_analysis, compatibility_notes, recommendation, ai_generated, analysis_source, created_at, updated_at) FROM stdin;
1	1	프론트엔드에서 생성된 성격 분석입니다.	프론트엔드에서 생성된 재물운 분석입니다.	프론트엔드에서 생성된 건강운 분석입니다.	프론트엔드에서 생성된 인간관계 분석입니다.	\N	\N	\N	f	frontend	2025-08-12 02:26:21.105	2025-08-12 02:26:21.105
\.


--
-- Data for Name: saju_results; Type: TABLE DATA; Schema: public; Owner: heal7_user
--

COPY public.saju_results (id, user_id, name, birth_year, birth_month, birth_day, birth_hour, birth_minute, gender, year_pillar, month_pillar, day_pillar, hour_pillar, wuxing_analysis, sipsin_analysis, calculation_engine, accuracy_score, created_at, updated_at) FROM stdin;
1	\N	테스트	1990	1	1	12	0	male	{"지지": "오", "천간": "경", "한자지지": "午", "한자천간": "庚"}	{"지지": "해", "천간": "무", "한자지지": "亥", "한자천간": "戊"}	{"지지": "사", "천간": "신", "한자지지": "巳", "한자천간": "辛"}	{"지지": "사", "천간": "무", "한자지지": "巳", "한자천간": "戊"}	{"금": 2, "목": 0, "수": 1, "토": 2, "화": 3}	{"관살": 0, "비겁": 1, "식상": 0, "인성": 2, "재성": 0}	frontend	95	2025-08-12 02:26:21.082	2025-08-12 02:26:21.082
\.


--
-- Data for Name: system_settings; Type: TABLE DATA; Schema: public; Owner: heal7_user
--

COPY public.system_settings (id, setting_key, setting_value, setting_type, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: heal7_user
--

COPY public.users (id, email, name, created_at, updated_at, preferences, user_mode) FROM stdin;
\.


--
-- Name: kasi_cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: heal7_user
--

SELECT pg_catalog.setval('public.kasi_cache_id_seq', 1, false);


--
-- Name: saju_interpretations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: heal7_user
--

SELECT pg_catalog.setval('public.saju_interpretations_id_seq', 1, true);


--
-- Name: saju_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: heal7_user
--

SELECT pg_catalog.setval('public.saju_results_id_seq', 1, true);


--
-- Name: system_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: heal7_user
--

SELECT pg_catalog.setval('public.system_settings_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: heal7_user
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: kasi_cache kasi_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.kasi_cache
    ADD CONSTRAINT kasi_cache_pkey PRIMARY KEY (id);


--
-- Name: saju_interpretations saju_interpretations_pkey; Type: CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_interpretations
    ADD CONSTRAINT saju_interpretations_pkey PRIMARY KEY (id);


--
-- Name: saju_results saju_results_pkey; Type: CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_results
    ADD CONSTRAINT saju_results_pkey PRIMARY KEY (id);


--
-- Name: system_settings system_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT system_settings_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: kasi_cache_cache_expires_at_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX kasi_cache_cache_expires_at_idx ON public.kasi_cache USING btree (cache_expires_at);


--
-- Name: kasi_cache_year_month_key; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE UNIQUE INDEX kasi_cache_year_month_key ON public.kasi_cache USING btree (year, month);


--
-- Name: saju_interpretations_saju_result_id_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX saju_interpretations_saju_result_id_idx ON public.saju_interpretations USING btree (saju_result_id);


--
-- Name: saju_results_birth_year_birth_month_birth_day_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX saju_results_birth_year_birth_month_birth_day_idx ON public.saju_results USING btree (birth_year, birth_month, birth_day);


--
-- Name: saju_results_created_at_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX saju_results_created_at_idx ON public.saju_results USING btree (created_at);


--
-- Name: saju_results_user_id_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX saju_results_user_id_idx ON public.saju_results USING btree (user_id);


--
-- Name: system_settings_setting_key_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX system_settings_setting_key_idx ON public.system_settings USING btree (setting_key);


--
-- Name: system_settings_setting_key_key; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE UNIQUE INDEX system_settings_setting_key_key ON public.system_settings USING btree (setting_key);


--
-- Name: system_settings_setting_type_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX system_settings_setting_type_idx ON public.system_settings USING btree (setting_type);


--
-- Name: users_created_at_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX users_created_at_idx ON public.users USING btree (created_at);


--
-- Name: users_email_idx; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE INDEX users_email_idx ON public.users USING btree (email);


--
-- Name: users_email_key; Type: INDEX; Schema: public; Owner: heal7_user
--

CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email);


--
-- Name: saju_interpretations saju_interpretations_saju_result_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_interpretations
    ADD CONSTRAINT saju_interpretations_saju_result_id_fkey FOREIGN KEY (saju_result_id) REFERENCES public.saju_results(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: saju_results saju_results_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: heal7_user
--

ALTER TABLE ONLY public.saju_results
    ADD CONSTRAINT saju_results_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

