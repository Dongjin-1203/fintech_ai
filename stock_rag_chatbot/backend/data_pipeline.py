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

class Data_pipeline:
    def __init__(self, json_params):
        self.url_json = "https://opendart.fss.or.kr/api/list.json"
        self.json_params = json_params

    def get_corp_code(self):
        '''DART API로 기업 코드, 기업명 저장'''
        corp_list = dart.api.filings.get_corp_code()
        corp_df = pd.DataFrame.from_dict(corp_list)
        corp_df = corp_df.dropna(subset = 'stock_code').sort_values('modify_date',ascending=False).reset_index(drop=True)
        corp_df['done_YN'] = "N"
        return corp_df
    
    def get_corp_report_list(self, corp_code, corp_df):
        '''보고서 리스트를 출력하고 이 정보를 저장'''
        response = requests.get(self.url_json, json_params=self.json_params)
        res = response.json()
        # 예외 처리: status 013(조회 데이터가 없음)
        if res ['status'] =='013' :
            print(f'{i},{corp_code}, {corp_df.loc[i,"corp_name"]}, 사업보고서개수 : 0')
        df_imsi = pd.DataFrame(res['list'])
        return df_imsi
    
def main():
    # 필요 변수 설장
    corp_code = '00126380'
    json_params = {
            'crtfc_key' : api_key,
            'corp_code' : corp_code ,
            'pblntf_ty' : 'A',
            'bgn_de' : '20250101' ## 사업보고서 시작일!
        }
    
    pipeline = Data_pipeline(json_params)

    # 기업 정보 저장 결과
    corp_df = pipeline.get_corp_code()
    print("기업 정보 현황 ")
    print("="*14)
    # print(corp_df) 
    # 상세 검색
    # print(corp_df[corp_df['corp_name']=='삼성전자'])  # 찾고 싶은 기업의 이름을 넣으면 된다.

    # 기업 공시 보고서
    df_imsi = pipeline.get_corp_report_list(corp_code, corp_df)
    print("기업 공시 보고서 ")
    print("="*14)
    # print(df_imsi) 
    file_path = f"stock_rag_chatbot/notebooks/data/csv/{corp_code}_report_list_test.csv"

    df_imsi.to_csv(file_path, index=False)
# 실행     
main()