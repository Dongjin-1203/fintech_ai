from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')

import dart_fss as dart
import pandas as pd
# 환경변수 설정
load_dotenv()   # .env 파일 로드

# print(f"현재 작업 디렉토리: {os.getcwd()}")
# # .env 파일 존재 여부 확인
# env_path = ".env"
# print(f".env 파일 존재: {os.path.exists(env_path)}")
api_key = os.getenv("dart_api_key")
print(f"DART API: {api_key}")

dart.set_api_key(api_key=api_key)  # API 등록
corp_list = dart.api.filings.get_corp_code()
print(corp_list)
# corp_df = pd.DataFrame.from_dict(corp_list)
# corp_df = corp_df.dropna(subset = 'stock_code').sort_values('modify_date',ascending=False).reset_index(drop=True)
# corp_df['done_YN'] = "N"