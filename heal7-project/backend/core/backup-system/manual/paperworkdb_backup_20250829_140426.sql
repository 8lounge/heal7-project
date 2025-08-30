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

--
-- Name: jobstatus; Type: TYPE; Schema: public; Owner: liveuser
--

CREATE TYPE public.jobstatus AS ENUM (
    'PENDING',
    'PROCESSING',
    'COMPLETED',
    'FAILED'
);


ALTER TYPE public.jobstatus OWNER TO liveuser;

--
-- Name: jobtype; Type: TYPE; Schema: public; Owner: liveuser
--

CREATE TYPE public.jobtype AS ENUM (
    'TEMPLATE',
    'FROM_SCRATCH'
);


ALTER TYPE public.jobtype OWNER TO liveuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: liveuser
--

CREATE TABLE public.jobs (
    id integer NOT NULL,
    status public.jobstatus,
    job_type public.jobtype,
    output_format character varying,
    result_file_path character varying,
    user_id integer
);


ALTER TABLE public.jobs OWNER TO liveuser;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: liveuser
--

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jobs_id_seq OWNER TO liveuser;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: liveuser
--

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;


--
-- Name: raw_scraped_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_scraped_data (
    id integer NOT NULL,
    portal_id character varying(100) NOT NULL,
    title text,
    quality_score integer,
    created_at timestamp without time zone DEFAULT now(),
    raw_data jsonb,
    scraped_content text,
    source_url text,
    processing_status character varying(50) DEFAULT 'raw'::character varying
);


ALTER TABLE public.raw_scraped_data OWNER TO postgres;

--
-- Name: raw_scraped_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.raw_scraped_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.raw_scraped_data_id_seq OWNER TO postgres;

--
-- Name: raw_scraped_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.raw_scraped_data_id_seq OWNED BY public.raw_scraped_data.id;


--
-- Name: scraping_config; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scraping_config (
    id integer NOT NULL,
    portal_id character varying(100) NOT NULL,
    enabled boolean DEFAULT true,
    interval_minutes integer DEFAULT 60,
    max_pages integer DEFAULT 10,
    timeout_seconds integer DEFAULT 30,
    last_updated timestamp without time zone DEFAULT now(),
    daily_limit integer DEFAULT 50,
    interval_hours integer DEFAULT 3,
    random_delay_min integer DEFAULT 5,
    random_delay_max integer DEFAULT 15,
    start_time time without time zone DEFAULT '09:00:00'::time without time zone,
    end_time time without time zone DEFAULT '18:00:00'::time without time zone,
    quality_threshold integer DEFAULT 7,
    is_enabled boolean DEFAULT true,
    weekdays_only boolean DEFAULT false,
    auto_retry boolean DEFAULT true,
    max_retries integer DEFAULT 3,
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.scraping_config OWNER TO postgres;

--
-- Name: scraping_config_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.scraping_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scraping_config_id_seq OWNER TO postgres;

--
-- Name: scraping_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.scraping_config_id_seq OWNED BY public.scraping_config.id;


--
-- Name: source_files; Type: TABLE; Schema: public; Owner: liveuser
--

CREATE TABLE public.source_files (
    id integer NOT NULL,
    file_name character varying,
    file_path character varying,
    file_size bigint,
    file_type character varying,
    category character varying,
    tags character varying,
    user_id integer
);


ALTER TABLE public.source_files OWNER TO liveuser;

--
-- Name: source_files_id_seq; Type: SEQUENCE; Schema: public; Owner: liveuser
--

CREATE SEQUENCE public.source_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.source_files_id_seq OWNER TO liveuser;

--
-- Name: source_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: liveuser
--

ALTER SEQUENCE public.source_files_id_seq OWNED BY public.source_files.id;


--
-- Name: support_programs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.support_programs (
    id integer NOT NULL,
    program_id character varying(255),
    portal_id character varying(100) NOT NULL,
    title text NOT NULL,
    implementing_agency text,
    support_field character varying(255),
    application_status character varying(50) DEFAULT 'active'::character varying,
    application_period text,
    data_quality_score integer,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    original_raw_id integer,
    evaluation_criteria text,
    attachments text,
    support_amount text,
    detail_url text
);


ALTER TABLE public.support_programs OWNER TO postgres;

--
-- Name: support_programs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.support_programs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.support_programs_id_seq OWNER TO postgres;

--
-- Name: support_programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.support_programs_id_seq OWNED BY public.support_programs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: liveuser
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying,
    password_hash character varying,
    storage_used bigint,
    google_auth_token character varying
);


ALTER TABLE public.users OWNER TO liveuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: liveuser
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO liveuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: liveuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


--
-- Name: raw_scraped_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_scraped_data ALTER COLUMN id SET DEFAULT nextval('public.raw_scraped_data_id_seq'::regclass);


--
-- Name: scraping_config id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scraping_config ALTER COLUMN id SET DEFAULT nextval('public.scraping_config_id_seq'::regclass);


--
-- Name: source_files id; Type: DEFAULT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.source_files ALTER COLUMN id SET DEFAULT nextval('public.source_files_id_seq'::regclass);


--
-- Name: support_programs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_programs ALTER COLUMN id SET DEFAULT nextval('public.support_programs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: liveuser
--

COPY public.jobs (id, status, job_type, output_format, result_file_path, user_id) FROM stdin;
1	PENDING	FROM_SCRATCH	docx	\N	3
2	PENDING	FROM_SCRATCH	docx	\N	7
3	PENDING	FROM_SCRATCH	docx	\N	8
\.


--
-- Data for Name: raw_scraped_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.raw_scraped_data (id, portal_id, title, quality_score, created_at, raw_data, scraped_content, source_url, processing_status) FROM stdin;
1	k-startup	중소벤처기업부	92	2025-08-25 14:09:21.062025	\N	\N	\N	raw
2	k-startup	창업진흥원	82	2025-08-25 14:09:21.070297	\N	\N	\N	raw
3	k-startup	2025 창업지원사업통합공고	84	2025-08-25 14:09:21.073893	\N	\N	\N	raw
4	k-startup	사업신청관리	82	2025-08-25 14:09:21.077223	\N	\N	\N	raw
5	k-startup	K-스타트업 지원사업 5	91	2025-08-25 14:09:21.084634	\N	\N	\N	raw
6	k-startup	중소벤처기업부	88	2025-08-25 14:14:54.566806	{"title": "중소벤처기업부", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251414_001", "scraped_at": "2025-08-25T14:14:54.566379", "source_url": "https://www.mss.go.kr/site/smba/main.do", "support_field": "창업지원", "support_amount": "최대 47억원", "scraped_content": "제목: 중소벤처기업부\\n기관: 중소벤처기업부\\n분야: 창업지원\\n링크: https://www.mss.go.kr/site/smba/main.do\\n원본: 중소벤처기업부...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.88}, "application_period": "2025년 모집", "data_quality_score": 88, "implementing_agency": "중소벤처기업부"}	제목: 중소벤처기업부\n기관: 중소벤처기업부\n분야: 창업지원\n링크: https://www.mss.go.kr/site/smba/main.do\n원본: 중소벤처기업부...	https://www.mss.go.kr/site/smba/main.do	processed
7	k-startup	창업진흥원	80	2025-08-25 14:14:54.575411	{"title": "창업진흥원", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251414_002", "scraped_at": "2025-08-25T14:14:54.575350", "source_url": "https://www.kised.or.kr/", "support_field": "창업지원", "support_amount": "최대 15억원", "scraped_content": "제목: 창업진흥원\\n기관: 창업진흥원\\n분야: 창업지원\\n링크: https://www.kised.or.kr/\\n원본: 창업진흥원...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.8}, "application_period": "2025년 모집", "data_quality_score": 80, "implementing_agency": "창업진흥원"}	제목: 창업진흥원\n기관: 창업진흥원\n분야: 창업지원\n링크: https://www.kised.or.kr/\n원본: 창업진흥원...	https://www.kised.or.kr/	processed
8	k-startup	2025 창업지원사업통합공고	86	2025-08-25 14:14:54.580174	{"title": "2025 창업지원사업통합공고", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251414_003", "scraped_at": "2025-08-25T14:14:54.580123", "source_url": "https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do", "support_field": "창업지원", "support_amount": "최대 23억원", "scraped_content": "제목: 2025 창업지원사업통합공고\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do\\n원본: 2025 창업지원사업통합공고...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.86}, "application_period": "2025년 모집", "data_quality_score": 86, "implementing_agency": "K-스타트업"}	제목: 2025 창업지원사업통합공고\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do\n원본: 2025 창업지원사업통합공고...	https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do	processed
9	k-startup	사업신청관리	86	2025-08-25 14:14:54.584881	{"title": "사업신청관리", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251414_004", "scraped_at": "2025-08-25T14:14:54.584838", "source_url": "https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz", "support_field": "창업지원", "support_amount": "최대 35억원", "scraped_content": "제목: 사업신청관리\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz\\n원본: 사업신청관리...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.86}, "application_period": "2025년 모집", "data_quality_score": 86, "implementing_agency": "K-스타트업"}	제목: 사업신청관리\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz\n원본: 사업신청관리...	https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz	processed
10	k-startup	K-스타트업 지원사업 5	85	2025-08-25 14:14:54.589773	{"title": "K-스타트업 지원사업 5", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251414_005", "scraped_at": "2025-08-25T14:14:54.589711", "source_url": "https://www.k-startup.go.kr/web/contents/webLGIN.do", "support_field": "창업지원", "support_amount": "최대 40억원", "scraped_content": "제목: K-스타트업 지원사업 5\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/web/contents/webLGIN.do\\n원본: \\n로그인\\n...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.85}, "application_period": "2025년 모집", "data_quality_score": 85, "implementing_agency": "K-스타트업"}	제목: K-스타트업 지원사업 5\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/web/contents/webLGIN.do\n원본: \n로그인\n...	https://www.k-startup.go.kr/web/contents/webLGIN.do	processed
11	k-startup	중소벤처기업부	88	2025-08-25 14:20:03.449204	{"title": "중소벤처기업부", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251419_001", "scraped_at": "2025-08-25T14:20:03.449135", "source_url": "https://www.mss.go.kr/site/smba/main.do", "support_field": "창업지원", "support_amount": "최대 25억원", "scraped_content": "제목: 중소벤처기업부\\n기관: 중소벤처기업부\\n분야: 창업지원\\n링크: https://www.mss.go.kr/site/smba/main.do\\n원본: 중소벤처기업부...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.88}, "application_period": "2025년 모집", "data_quality_score": 88, "implementing_agency": "중소벤처기업부"}	제목: 중소벤처기업부\n기관: 중소벤처기업부\n분야: 창업지원\n링크: https://www.mss.go.kr/site/smba/main.do\n원본: 중소벤처기업부...	https://www.mss.go.kr/site/smba/main.do	processed
12	k-startup	창업진흥원	83	2025-08-25 14:20:03.806241	{"title": "창업진흥원", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251420_002", "scraped_at": "2025-08-25T14:20:03.806178", "source_url": "https://www.kised.or.kr/", "support_field": "창업지원", "support_amount": "최대 14억원", "scraped_content": "제목: 창업진흥원\\n기관: 창업진흥원\\n분야: 창업지원\\n링크: https://www.kised.or.kr/\\n원본: 창업진흥원...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.83}, "application_period": "2025년 모집", "data_quality_score": 83, "implementing_agency": "창업진흥원"}	제목: 창업진흥원\n기관: 창업진흥원\n분야: 창업지원\n링크: https://www.kised.or.kr/\n원본: 창업진흥원...	https://www.kised.or.kr/	processed
13	k-startup	2025 창업지원사업통합공고	93	2025-08-25 14:20:03.837969	{"title": "2025 창업지원사업통합공고", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251420_003", "scraped_at": "2025-08-25T14:20:03.837911", "source_url": "https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do", "support_field": "창업지원", "support_amount": "최대 7억원", "scraped_content": "제목: 2025 창업지원사업통합공고\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do\\n원본: 2025 창업지원사업통합공고...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.93}, "application_period": "2025년 모집", "data_quality_score": 93, "implementing_agency": "K-스타트업"}	제목: 2025 창업지원사업통합공고\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do\n원본: 2025 창업지원사업통합공고...	https://www.k-startup.go.kr/web/contents/webFSBIPBANC.do	processed
14	k-startup	사업신청관리	80	2025-08-25 14:20:03.869831	{"title": "사업신청관리", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251420_004", "scraped_at": "2025-08-25T14:20:03.869680", "source_url": "https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz", "support_field": "창업지원", "support_amount": "최대 38억원", "scraped_content": "제목: 사업신청관리\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz\\n원본: 사업신청관리...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.8}, "application_period": "2025년 모집", "data_quality_score": 80, "implementing_agency": "K-스타트업"}	제목: 사업신청관리\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz\n원본: 사업신청관리...	https://www.k-startup.go.kr/passni/kstartup/tokenInfoRelay.jsp?flag=biz	processed
15	k-startup	K-스타트업 지원사업 5	83	2025-08-25 14:20:03.887794	{"title": "K-스타트업 지원사업 5", "portal_id": "k-startup", "program_id": "KSTARTUP_202508251420_005", "scraped_at": "2025-08-25T14:20:03.887729", "source_url": "https://www.k-startup.go.kr/web/contents/webLGIN.do", "support_field": "창업지원", "support_amount": "최대 22억원", "scraped_content": "제목: K-스타트업 지원사업 5\\n기관: K-스타트업\\n분야: 창업지원\\n링크: https://www.k-startup.go.kr/web/contents/webLGIN.do\\n원본: \\n로그인\\n...", "scraping_metadata": {"user_agent": "Mozilla/5.0 (Scraper Bot)", "portal_type": "k-startup", "scraping_method": "BeautifulSoup", "extraction_confidence": 0.83}, "application_period": "2025년 모집", "data_quality_score": 83, "implementing_agency": "K-스타트업"}	제목: K-스타트업 지원사업 5\n기관: K-스타트업\n분야: 창업지원\n링크: https://www.k-startup.go.kr/web/contents/webLGIN.do\n원본: \n로그인\n...	https://www.k-startup.go.kr/web/contents/webLGIN.do	processed
\.


--
-- Data for Name: scraping_config; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scraping_config (id, portal_id, enabled, interval_minutes, max_pages, timeout_seconds, last_updated, daily_limit, interval_hours, random_delay_min, random_delay_max, start_time, end_time, quality_threshold, is_enabled, weekdays_only, auto_retry, max_retries, updated_at) FROM stdin;
1	bizinfo	t	60	20	30	2025-08-25 13:33:20.930304	2	1	3	12	09:00:00	18:00:00	8	t	f	t	3	2025-08-25 16:20:27.57426
2	k-startup	t	60	15	30	2025-08-25 13:33:20.930304	2	1	5	18	09:00:00	18:00:00	7	t	f	t	2	2025-08-25 16:20:27.72152
\.


--
-- Data for Name: source_files; Type: TABLE DATA; Schema: public; Owner: liveuser
--

COPY public.source_files (id, file_name, file_path, file_size, file_type, category, tags, user_id) FROM stdin;
1	test-document.txt	uploads/3_test-document.txt	467	txt	기타		3
2	[별첨 1] 예비창업패키지 사업계획서 양식(hwp파일).pdf	uploads/5_[별첨 1] 예비창업패키지 사업계획서 양식(hwp파일).pdf	603245	pdf	\N	\N	5
3	test-template.txt	uploads/7_test-template.txt	318	txt	\N	\N	7
4	test-document.txt	uploads/8_test-document.txt	49	txt	\N	\N	8
\.


--
-- Data for Name: support_programs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.support_programs (id, program_id, portal_id, title, implementing_agency, support_field, application_status, application_period, data_quality_score, created_at, updated_at, original_raw_id, evaluation_criteria, attachments, support_amount, detail_url) FROM stdin;
1	BIZINFO_001	bizinfo	중소기업 기술개발 지원사업	중소벤처기업부	기술개발	active	\N	85	2025-08-25 13:11:26.867496	2025-08-25 13:11:26.867496	\N	\N	\N	최대 3억원	\N
2	BIZINFO_002	bizinfo	창업 인큐베이팅 프로그램	창업진흥원	창업지원	active	\N	92	2025-08-25 13:11:26.867496	2025-08-25 13:11:26.867496	\N	\N	\N	최대 5천만원	\N
3	KSTARTUP_001	k-startup	예비창업패키지	K-스타트업	창업지원	active	\N	88	2025-08-25 13:11:26.867496	2025-08-25 13:11:26.867496	\N	\N	\N	최대 1억원	\N
4	KSTARTUP_002	k-startup	BI 육성사업	TIPS	창업지원	active	\N	90	2025-08-25 13:11:26.867496	2025-08-25 13:11:26.867496	\N	\N	\N	최대 2억원	\N
5	KSTARTUP_202508251409_001	k-startup	중소벤처기업부	중소벤처기업부	창업지원	active	2025년 모집	92	2025-08-25 14:09:21.068137	2025-08-25 14:09:21.068442	\N	\N	\N	최대 38억원	\N
6	KSTARTUP_202508251409_002	k-startup	창업진흥원	창업진흥원	창업지원	active	2025년 모집	82	2025-08-25 14:09:21.072266	2025-08-25 14:09:21.072541	\N	\N	\N	최대 9억원	\N
7	KSTARTUP_202508251409_003	k-startup	2025 창업지원사업통합공고	K-스타트업	창업지원	active	2025년 모집	84	2025-08-25 14:09:21.07591	2025-08-25 14:09:21.076022	\N	\N	\N	최대 49억원	\N
8	KSTARTUP_202508251409_004	k-startup	사업신청관리	K-스타트업	창업지원	active	2025년 모집	82	2025-08-25 14:09:21.079212	2025-08-25 14:09:21.079529	\N	\N	\N	최대 35억원	\N
9	KSTARTUP_202508251409_005	k-startup	K-스타트업 지원사업 5	K-스타트업	창업지원	active	2025년 모집	91	2025-08-25 14:09:21.086613	2025-08-25 14:09:21.086755	\N	\N	\N	최대 37억원	\N
10	KSTARTUP_202508251414_001	k-startup	중소벤처기업부	중소벤처기업부	창업지원	active	2025년 모집	88	2025-08-25 14:14:54.571102	2025-08-25 14:14:54.571658	6	\N	\N	최대 47억원	\N
11	KSTARTUP_202508251414_002	k-startup	창업진흥원	창업진흥원	창업지원	active	2025년 모집	80	2025-08-25 14:14:54.577384	2025-08-25 14:14:54.57753	7	\N	\N	최대 15억원	\N
12	KSTARTUP_202508251414_003	k-startup	2025 창업지원사업통합공고	K-스타트업	창업지원	active	2025년 모집	86	2025-08-25 14:14:54.581918	2025-08-25 14:14:54.582025	8	\N	\N	최대 23억원	\N
13	KSTARTUP_202508251414_004	k-startup	사업신청관리	K-스타트업	창업지원	active	2025년 모집	86	2025-08-25 14:14:54.586811	2025-08-25 14:14:54.586931	9	\N	\N	최대 35억원	\N
14	KSTARTUP_202508251414_005	k-startup	K-스타트업 지원사업 5	K-스타트업	창업지원	active	2025년 모집	85	2025-08-25 14:14:54.591608	2025-08-25 14:14:54.591727	10	\N	\N	최대 40억원	\N
15	KSTARTUP_202508251419_001	k-startup	중소벤처기업부	중소벤처기업부	창업지원	active	2025년 모집	88	2025-08-25 14:20:03.790896	2025-08-25 14:20:03.797508	11	\N	\N	최대 25억원	\N
16	KSTARTUP_202508251420_002	k-startup	창업진흥원	창업진흥원	창업지원	active	2025년 모집	83	2025-08-25 14:20:03.828522	2025-08-25 14:20:03.829322	12	\N	\N	최대 14억원	\N
17	KSTARTUP_202508251420_003	k-startup	2025 창업지원사업통합공고	K-스타트업	창업지원	active	2025년 모집	93	2025-08-25 14:20:03.846675	2025-08-25 14:20:03.846886	13	\N	\N	최대 7억원	\N
18	KSTARTUP_202508251420_004	k-startup	사업신청관리	K-스타트업	창업지원	active	2025년 모집	80	2025-08-25 14:20:03.877033	2025-08-25 14:20:03.877132	14	\N	\N	최대 38억원	\N
19	KSTARTUP_202508251420_005	k-startup	K-스타트업 지원사업 5	K-스타트업	창업지원	active	2025년 모집	83	2025-08-25 14:20:03.892997	2025-08-25 14:20:03.893186	15	\N	\N	최대 22억원	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: liveuser
--

COPY public.users (id, email, password_hash, storage_used, google_auth_token) FROM stdin;
1	test@paperwork.com	$2b$12$gOxhHduZZ.xka8bkDTPVPeGaqIv1PPtzno6F.2A/nQ8yqCPn7Lm6S	0	\N
2	test3@example.com	$2b$12$rhT7wQ9xJkFUYolAQZRmgeUzsUNps1pmzhTUP6leBKVrxMg7upWue	0	\N
3	demo@paperwork.ai	$2b$12$.YoerapzcFY8wUpr5/T0ref7iY0WiZMamlIIEpSkNkAyViuZKCY6a	0	\N
4	test.user@paperwork.ai	$2b$12$1Zz8rbeueJl9LYykMCpKs.2omWMElGMOWZKQX2veNsdWLD7lAz/Ce	0	\N
5	jihwan20@naver.com	$2b$12$B2/EkGUbLHHKvYkeoXNnBOB6uFksJdANFChzSeW.krdGmccRG9ajq	0	\N
6	demo.user@example.com	$2b$12$QSsWgW9tb/lDq1uWPKGK2O0WcEJsi0ibLGNYOYrD86bmCr5H1UptW	0	\N
7	visual-editor-test@heal7.com	$2b$12$/RASmFngWLX4rH/aROZTe.Ka7WAQnzxyNOgqKGDCtg4ahcWN83fte	0	\N
8	test@example.com	$2b$12$SK7qZlIdj4jiEH6KsL/7PumLb7h1pWaEvmm00SvAzl1ZbrMjvOxwO	0	\N
\.


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: liveuser
--

SELECT pg_catalog.setval('public.jobs_id_seq', 3, true);


--
-- Name: raw_scraped_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.raw_scraped_data_id_seq', 15, true);


--
-- Name: scraping_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.scraping_config_id_seq', 4, true);


--
-- Name: source_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: liveuser
--

SELECT pg_catalog.setval('public.source_files_id_seq', 4, true);


--
-- Name: support_programs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.support_programs_id_seq', 19, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: liveuser
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: raw_scraped_data raw_scraped_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_scraped_data
    ADD CONSTRAINT raw_scraped_data_pkey PRIMARY KEY (id);


--
-- Name: scraping_config scraping_config_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scraping_config
    ADD CONSTRAINT scraping_config_pkey PRIMARY KEY (id);


--
-- Name: scraping_config scraping_config_portal_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scraping_config
    ADD CONSTRAINT scraping_config_portal_id_key UNIQUE (portal_id);


--
-- Name: source_files source_files_pkey; Type: CONSTRAINT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.source_files
    ADD CONSTRAINT source_files_pkey PRIMARY KEY (id);


--
-- Name: support_programs support_programs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_programs
    ADD CONSTRAINT support_programs_pkey PRIMARY KEY (id);


--
-- Name: support_programs support_programs_program_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_programs
    ADD CONSTRAINT support_programs_program_id_key UNIQUE (program_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_jobs_id; Type: INDEX; Schema: public; Owner: liveuser
--

CREATE INDEX ix_jobs_id ON public.jobs USING btree (id);


--
-- Name: ix_source_files_id; Type: INDEX; Schema: public; Owner: liveuser
--

CREATE INDEX ix_source_files_id ON public.source_files USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: liveuser
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: liveuser
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: jobs jobs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: source_files source_files_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: liveuser
--

ALTER TABLE ONLY public.source_files
    ADD CONSTRAINT source_files_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

