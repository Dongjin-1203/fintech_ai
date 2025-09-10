"""
# 상장목록
1. 코스피 상장 목록 딕셔너리 관리 + 공시정보 코드까지??

# 주식데이터
1. yfinance로 증권데이터 가져오기
2. csv로 저장

# 뉴스데이터
1. rss_feeds정보 수집
2. 기사 제목, 링크, 게시일 수집
3. csv로 저정

# DART 공시정보
1. DART 공시정보에서 보고서 제목, 번호, 기타 필요 내용추출
2. csv, json형식으로 저장
"""
# 라이브러리
from dotenv import load_dotenv
import os
import pandas as pd
import dart_fss as dart
import requests
import json
import yfinance as yf
import re
import warnings
warnings.filterwarnings('ignore')

# 환경변수 설정
load_dotenv()   # .env 파일 로드

api_key = os.getenv("dart_api_key")
# API 키가 제대로 로드되었는지 확인
if api_key is None or api_key == "":
    print("❌ API 키가 로드되지 않았습니다!")
    print("1. .env 파일이 올바른 위치에 있는지 확인")
    print("2. .env 파일 내용: dart_api_key=YOUR_API_KEY")
else:
    print("✅ API 키 로드 완료")
    dart.set_api_key(api_key=api_key)
    print("✅ DART API 키 설정 완료")

def get_corp_code():
    '''DART API로 기업 코드, 기업명 저장'''
    corp_list = dart.api.filings.get_corp_code()
    corp_df = pd.DataFrame.from_dict(corp_list)
    corp_df = corp_df.dropna(subset = 'stock_code').sort_values('modify_date',ascending=False).reset_index(drop=True)
    corp_df['done_YN'] = "N"
    return corp_df
class Data_pipeline:
    def __init__(self):
        pass
    
    def get_corp_report_list(self, corp_code, corp_df, params):
        '''보고서 리스트를 출력하고 이 정보를 저장'''
        url_json = "https://opendart.fss.or.kr/api/list.json"
        response = requests.get(url_json, params)
        res = response.json()
        # 예외 처리: status 013(조회 데이터가 없음)
        if res ['status'] =='013' :
            print(f'{i},{corp_code}, {corp_df.loc[i,"corp_name"]}, 사업보고서개수 : 0')
        df_imsi = pd.DataFrame(res['list'])
        return df_imsi
    
    def collect_finance_data(self, corp_name):
        stock = yf.Ticker(corp_name)   # 주식 데이터 다운
        # info = stock.info
        stock_data = stock.history(period="1mo")   # 한달 간 주가 데이터
        stock_data = pd.DataFrame(stock_data)
        return stock_data
    
    def get_naver_news_api(self, company_name, naver_id, naver_api_key):
        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": naver_id,
            "X-Naver-Client-Secret": naver_api_key
        }
        params = {
            "query": f"{company_name} 주식",
            "display": 20,
            "sort": "date"
        }
        
        def clean_html_tags(text):
            """HTML 태그를 완전히 제거하는 함수"""
            if not text:
                return ""
            # 모든 HTML 태그 제거
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("요청 성공!")
                
                # 직접 JSON으로 파싱
                news_data = response.json()
                
                # 뉴스 데이터를 저장할 리스트 생성 (수정된 부분)
                news_list = []
                
                # 각 뉴스 아이템에서 필요한 정보를 추출
                for item in news_data['items']:
                    title = clean_html_tags(item['title'])
                    link = item['link']
                    description = clean_html_tags(item['description'])
                    pubDate = item['pubDate']

                    # 개별 뉴스를 딕셔너리로 생성
                    news_dict = {
                        "제목": title,
                        "링크": link,
                        "기사요약": description,
                        "작성일자": pubDate
                    }
                    
                    # 리스트에 추가
                    news_list.append(news_dict)
                    
                    # 출력 (선택사항)
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Description: {description}")
                    print(f"Published Date: {pubDate}")
                    print("\n")
                
                # 전체 리스트로 DataFrame 생성 (수정된 부분)
                news_df = pd.DataFrame(news_list)
                print(f"총 {len(news_df)}개의 뉴스를 DataFrame으로 생성했습니다.")
                
                # 성공 시 DataFrame 반환
                return news_df
                
            else:
                print(f"Error Code: {response.status_code}")
                print(f"Error Message: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"요청 중 오류 발생: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
        except Exception as e:
            print(f"예상치 못한 오류: {e}")
            return None
    
def main():
    pipeline = Data_pipeline()

    # 기업 정보 저장
    corp_df = get_corp_code()
    print("기업 정보 현황 다운로드 ")
    print("="*30)
    corp_df.to_csv('stock_rag_chatbot/notebooks/data/corp_code_list.csv', index=False)
    print("✅ corp_code_list.csv 파일 저장 완료. 한국 상장기업 저장완료")
    # 상세 검색
    # print(corp_df[corp_df['corp_name']=='삼성전자'])  # 찾고 싶은 기업의 이름을 넣으면 된다.

    # 공시 보고서 제목 리스트 저장
    print("최근 1분기 기업 공시 보고서 저장(제목 리스트)")
    print("="*30)
    corp_name = input("기업명을 입력하세요(예:삼성전자): ")
    corp_code = corp_df[corp_df['corp_name']==corp_name]['corp_code'].values[0]
    report_params = {
            'crtfc_key' : api_key,
            'corp_code' : corp_code ,
            'pblntf_ty' : 'A',
            'bgn_de' : '20250101' ## 사업보고서 시작일!
        }

    # 기업 공시 보고서
    df_imsi = pipeline.get_corp_report_list(corp_code, corp_df, report_params)
    # print(df_imsi) 
    file_path = f"stock_rag_chatbot/notebooks/data/csv/{corp_name}_report_list_test.csv"
    df_imsi.to_csv(file_path, index=False)
    print(f"✅ {corp_name} 공시정보 제목 리스트 저장 완료. {corp_name}_report_list_test.csv")

    # 뉴스 크롤링 관련 변수
    print("최근 1달 간 네이버 기업 뉴스 저장")
    print("="*30)
    naver_id = os.getenv("naver_id")
    naver_api_key = os.getenv("naver_api_key")

    # 뉴스데이터 수집(네이버)
    naver_news_path = f"stock_rag_chatbot/notebooks/data/csv/{corp_name}_naver_news_test.csv"
    naver_news_df = pipeline.get_naver_news_api(corp_name, naver_id, naver_api_key)
    naver_news_df.to_csv(naver_news_path, index=False)
    print(f"✅ {corp_name} 네이버 기업 뉴스 저장 완료. {corp_name}_naver_news_test.csv")

    # 주식 데이터 수집
    print("1달 기업 주가 저장")
    print("="*30)
    corp_list = []
    nums = int(input("몇개의 기업 주가 데이터를 수집할까요? (예:1): "))
    for _ in range(nums):
        stock_name = input("조회할 기업명을 입력하세요(예:삼성전자): ")
        stock_code = corp_df[corp_df['corp_name']==stock_name]['stock_code'].values[0]
        print(f"{stock_name}의 종목코드: {stock_code} / yfinance용 종목코드: {stock_code}.KS")
        corp_list.append(f"{stock_code}.KS")
        print("종목을 저장 완료 했습니다.")
        print("-"*30)
    print("수집할 기업 리스트:", corp_list)
    
    for corp_nm in corp_list:
        stock_data_path = f"stock_rag_chatbot/notebooks/data/csv/{corp_nm}_stock_data_test.csv"
        stock_data = pipeline.collect_finance_data(corp_name= corp_nm)
        stock_data.to_csv(stock_data_path, index=False)
        print(f"✅ {corp_nm} 기업 주가 정보 저장 완료. {corp_nm}_stock_data_test.csv")


    
# 실행     
main()