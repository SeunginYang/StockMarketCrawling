import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()      # 창 최대화

#1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

#2. 조회 항목 초기화 (체크되어 있는 항목 체크해주기 "거래량, 외국인비율, 상장주식수, 시가총액 등")
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): #체크된 상태라면
        checkbox.click() #클릭 (체크해제)

#3. 조회 항목 설정 (원하는 항목)
items_to_select = ['영업이익', '자산총계', '매출액증가율']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')    # 부모 element를 찾게 된다
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text)    #선택할 수 있는 항목들 확인완료
    if label.text in items_to_select:
        checkbox.click() # 체크 클릭

#4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()


for idx in range(1,40):                              #네이버 주식에서 조회 가능한 페이지가 약 37페이지 인데 늘어날 가능성이 있어 범위를 더 넓힘
    # 사전 작업 : 페이지 이동
    browser.get(url + str(idx))    # http://naver.com ..... &page=1~39 까지 반복문으로 돌림
        
    #5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]         #df = data frame의 약자
    df.head(10)                                       #가독성을 위해 종목을 10개로 추림 -> 원하는 수로 변경 가능
    df.dropna(axis='index', how='all', inplace=True)  #가로줄(index) 기준으로 전체가 비어있다고(Nan data) 하면 내용을 지워라
    df.dropna(axis='columns', how='all', inplace=True)  #세로줄(column) 기준으로 전체가 비어있다고(Nan data) 하면 내용을 지워라
    if len(df) == 0:     # 네이버 주식 조회 가능한 페이지가 38이상 넘어서 아무런 내용이 없는 경우는 작업을 종료하겠다는 내용을 포함
        break

    #6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): #파일이 있다면? 헤더는 제외시키자
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)       #mode='a' append의 의미로 다음페이지의 자료도 뒤에 붙일 수 있게 하는 명령어,    header=False 로 헤더 부분 제외 시킴
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit()      #브라우저 종료



