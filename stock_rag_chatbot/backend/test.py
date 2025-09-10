import pandas as pd
import dart_fss as dart
import os
from dotenv import load_dotenv
import requests

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

corp_df = get_corp_code()
corp_df.to_csv('stock_rag_chatbot/notebooks/data/corp_code_list.csv', index=False)
print("✅ corp_code_list.csv 파일 저장 완료")

print(corp_df[corp_df['corp_name']=='삼성전자']['corp_code'].values[0])  # 삼성전자 기업코드 출력

def get_corp_report_list(corp_code, corp_df, params):
    '''보고서 리스트를 출력하고 이 정보를 저장'''
    url_json = "https://opendart.fss.or.kr/api/list.json"
    response = requests.get(url_json, params)
    res = response.json()
    # 예외 처리: status 013(조회 데이터가 없음)
    if res ['status'] =='013' :
        print(f'{i},{corp_code}, {corp_df.loc[i,"corp_name"]}, 사업보고서개수 : 0')
    df_imsi = pd.DataFrame(res['list'])
    return df_imsi

# 필요 변수 설장
print("기업 공시 보고서 저장(제목 리스트)")
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
df_imsi = get_corp_report_list(corp_code, corp_df, report_params)
# print(df_imsi) 
file_path = f"stock_rag_chatbot/notebooks/data/csv/{corp_name}_report_list_test.csv"
df_imsi.to_csv(file_path, index=False)
print(f"✅ {corp_name} 공시정보 제목 리스트 저장 완료. {file_path}")