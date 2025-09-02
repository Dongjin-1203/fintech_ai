# fintect_ai
---
RAG 실습 및 챗봇 개발을 연습겸 실제 투자정보를 수집하고 종목을 추천해주는 AI 에이전트를 만들면 좋겠다는 생각과 함께 프로젝트를 시작했다.

## 기술 스택

__Backend__
- FastAPI + PostgreSQL + Redis
- LangChain + OpenAI GPT-4
- Pinecone (Vector DB)

__Data Pipeline__
- Apache Airflow (스케줄링)
- yfinance, beautifulsoup4
- pandas, numpy

__Frontend__
- Next.js 14 + TypeScript + Tailwind CSS
- Streamlit (프로토타입/어드민)
- Chart.js / Recharts (차트)

__DevOps__
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- AWS/Vercel (배포)

## 📋 Phase 1: 기초 인프라 구축
### 1.1 환경 설정      
- [ ] Python 가상환경 구성    
- [ ] FastAPI 백엔드 프로젝트 초기화      
- [ ] Streamlit 프로토타입 환경 구성      
- [ ] Next.js 프로젝트 초기화      

### 1.2 데이터 수집 파이프라인
```
# 주요 데이터 소스
- yfinance (주가 데이터)
- Alpha Vantage API (재무제표)
- 네이버 증권 뉴스 크롤링
- DART API (공시정보)
```

### 1.3 기본 RAG 시스템
- [ ] Vector DB 선택 및 설정 (Pinecone/Qdrant)
- [ ] 문서 임베딩 파이프라인 구축
- [ ] 기본 검색 및 생성 로직 구현

### 1.4 Streamlit 프로토타입
- [ ] 기본 채팅 인터페이스
- [ ] 주가 차트 시각화
- [ ] 간단한 주식 정보 조회

__📊 Milestone 1__: 삼성전자, SK하이닉스 등 5개 종목 기본 정보 조회 가능

---

## 25.09.02

### 시행 과제

#### 1. 개발 환경 구축
__🎯 Task 1.1: 프로젝트 구조 생성__
```
bashstock_rag_chatbot/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── streamlit_app/
│   └── nextjs_app/
├── notebooks/
├── data/
└── docker-compose.yml
```

__체크리스트__:      
- [x] GitHub 레포지토리 생성      
- [x] 폴더 구조 생성      
- [x] requirements.txt 작성      
- [x] .gitignore 설정      
- [x] README.md 초안 작성      

__🎯 Task 1.2: 가상환경 & 패키지 설치__
```
# requirements.txt 기본 패키지
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.1
yfinance==0.2.28
python-dotenv==1.0.0
requests==2.31.0
pandas==2.1.1
numpy==1.24.3
```
__체크리스트__:      
- [x] Python 가상환경 생성 (venv)        
- [x] 기본 패키지 설치      
- [x] VSCode에서 인터프리터 설정      
- [x] Colab에서 패키지 설치 테스트

#### 주식 데이터 수집 테스트
__🎯 Task 1.3: yfinance 데이터 수집 테스트(Colab)__
__체크리스트__:
- [ ] yfinance로 한국 주식 데이터 수집 테스트
- [ ] 주가, 거래량, 기본 정보 추출 확인
- [ ] 데이터 형태 파악 및 전처리 로직 작성
- [ ] 에러 핸들링 (네트워크, 심볼 오류 등)

__🎯 Task 1.4: 뉴스 크롤링 테스트(Colab)__
__체크리스트__:
- [ ] 네이버 증권 뉴스 크롤링 테스트
- [ ] 뉴스 제목, 내용, 날짜 추출
- [ ] robots.txt 확인 및 윤리적 크롤링
- [ ] 크롤링 결과를 CSV로 저장
