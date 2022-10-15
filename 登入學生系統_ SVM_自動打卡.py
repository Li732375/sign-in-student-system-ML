##於指定時間自動登入學生系統打卡並登出關閉
##介面完成
##測試完成

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import system

from os import sep, path, system, mkdir, listdir
from PIL import Image, ImageEnhance, ImageFilter
from time import time, sleep, localtime, ctime

import joblib

import numpy as np

import traceback, stdiomask

# https://www.facebook.com/
site = 'https://webap.nptu.edu.tw/web/Secure/default.aspx?sIndex=2'
#帳號
account = input('帳號?')
#密碼至少首位要大寫
password = stdiomask.getpass(prompt = '密碼(至少首位要大寫)?', mask = '密')
#功能選擇
carded = input('上班(0) / 下班(1) / 上下班(2)?')
 

def login(driver, site, svc_model2, account, password):
#登入
    while True:
        #前往網站
        driver.get(site)

        #輸入email 
        context = driver.find_element_by_css_selector('#LoginStd_txtAccount')
        context.send_keys(account) 
        sleep(0.5)

        #輸入password
        context = driver.find_element_by_css_selector('#LoginStd_txtPassWord')
        context.send_keys(password)
        sleep(0.5)

        #輸入驗證碼
        #驗證碼網址
        targetUrl = 'https://webap.nptu.edu.tw/web/Modules/CaptchaCreator.aspx'

        ##裁切等分
        scale = 7
        ##亮度增強值
        l_fac = 14
        ##銳度增強值
        c_fac = 10
        ##中值濾波尺寸
        size = 3

        #擷取圖片
        context = driver.find_element_by_css_selector('#imgCaptcha')
        context.screenshot('quest.png')

        #開啟圖片
        pic = Image.open('quest.png')

        width, height = pic.size
            
        #求出分割比例單位
        part = int(height / scale)

        ##分割成上下半
        #crop((left, upper, right, lower))
        halfUp = pic.crop((0, 0, width, part))
        halfDown = pic.crop((0, part, width, height))
        print('分割完成')

        #重組並建立空白圖片
        newPic = Image.new('RGB', (width, height))

        newPic.paste(halfDown, (0, 0, width, height - part))
        newPic.paste(halfUp, (0, height - part , width, height))
        print('重組完成')

        ##影像處理
        #調亮
        newPic = ImageEnhance.Brightness(newPic).enhance(l_fac)

        #提升銳利度
        newPic = ImageEnhance.Contrast(newPic).enhance(c_fac)

        #中值濾波
        newPic = newPic.filter(ImageFilter.MedianFilter(size))

        print('- 影像處理第一部分完成\n')

        cut = int((width - 2) / 4 - 1)
        parts = list()
        answer = list()
            
        for i in range(4):
                
            part = newPic.crop((3 + cut * i, 0, 3 + cut + cut * i, height))
            part_arr = np.array(part)
            part_arr_One = list(part_arr.flatten())
            parts.extend([part_arr_One])
        
        ##SVM辨識並預測
        parts = np.array(parts)
        answer = svc_model2.predict(parts)    
        code = ''.join(str(x) for x in answer)
        print('辨識結果：', code) 
    
        #輸入答案
        context = driver.find_element_by_css_selector('#LoginStd_txtCheckCode')
        context.send_keys(code)
    
        #按下登入紐
        commit = driver.find_element_by_css_selector('#LoginStd_ibtLogin')
        commit.click()
        sleep(1.5)

        #獲取alert對話方塊
        #下列為舊寫法，已棄用
        #alert = driver.switch_to.alert()
        alert = driver.switch_to.alert
        alert_info = alert.text
        print('\n網頁訊息: ', alert_info)
        sleep(0.5)
        alert.accept()      

        #為驗證碼錯誤時而設，待補強
        #亦可以直接重啟程式就好
    
        if alert_info == '您目前已經登錄系統中，無法重複登入，如果您前一次是非正常狀態下登出，請等5分鐘後再登入!!':      
            t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
            print(t + ' 登入失敗\n')
            sleep(2)
            break
        
        elif alert_info == '驗證碼不符!!':
            t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
            print(t + ' 登入失敗\n')
            print('嘗試重新登入')
            sleep(2)
            continue
        
        elif alert_info == '因為你太久沒有操作網頁，網頁權限已過期，為了安全考量，系統將自動登出，敬請見諒!!':
            t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
            print(t + ' 登入失敗\n')
            print('嘗試重新登入')
            sleep(2)
            continue
        
        else:
            print('\n登入成功')
    
        break
    
def logout(driver):
#登出
    ##進去之後是站中站
    #左半站'https://webap.nptu.edu.tw/web/Message/MenuTree.aspx'
    #右半站'https://webap.nptu.edu.tw/web/Message/Main.aspx'
    #而登出僅在右半站才有
    driver.get('https://webap.nptu.edu.tw/web/Message/Main.aspx')
    sleep(1)

    #按下登出紐
    commit = driver.find_element_by_css_selector('#CommonHeader_ibtLogOut')
    commit.click()
    sleep(0.8)

    #登出確認
    alert = driver.switch_to.alert.accept()
    print('\n登出成功\n')

def do(driver):
#抵達目標頁面
    driver.get('https://webap.nptu.edu.tw/web/Message/Main.aspx')
    sleep(1)

    #找到打卡紐
    commit = driver.find_element_by_css_selector('#MenuDefault_dgData__ctl23_ibtMENU_ID')
    commit.click()
    sleep(0.2)

    #找到兼任助理打卡紀錄
    commit = driver.find_element_by_css_selector('#SubMenu_dgData .TRAlternatingItemStyle')
    commit.click()
    sleep(0.2)

    #獲取alert對話方塊
    alert = driver.switch_to.alert
    alert_info = alert.text
    print()
    print('網頁訊息: ', alert_info)
    sleep(0.5)
    alert.accept()    

    print('\n成功抵達打卡頁面')

def countdown(target_Time, delta = 1):
#倒數計時
#參數範例格式(ex:'2300')，24 制
#時間限制 24 小時內
# delta 為緩衝誤差值
    target_Time = [int(target_Time[0:2]), int(target_Time[2:4])]
    nowTime = [localtime(time()).tm_hour, localtime(time()).tm_min, localtime(time()).tm_sec]
    
    if localtime(time()).tm_hour > target_Time[0]:
        target_Time[0] += 24
 
    if localtime(time()).tm_min > target_Time[1]:
        target_Time[1] += 60
        target_Time[0] -= 1                                    
    
    t = (target_Time[0] - nowTime[0])*60*60 + (target_Time[1] - nowTime[1])*60 + nowTime[2]
    t -= delta

    print('現在時間', ctime(time()))
    print('倒數時間(秒)', t)
    print('開始計時啦 >o<')
    
    for i in range(t):
        sleep(1)

    print('時間到~~~ >w<')

        
###main
if carded == '1' or carded == '2':
    ##填寫欄位的內容
    #是否包含休息時間
    rest = input('有休息時間?(y(1)/n(0))')
    if not rest == 'y' and not rest == '1' and not rest == 'n' and not rest == '0':
        print('\n找到例外文字，改為預設值(n)')
        rest = 'n'
    
    if rest == 'y' or rest == '1':
        #休息時間左
        rest_start_time = int(input('\n休息開始時間?(ex:1200)'))        
    
        #休息時間右
        rest_end_time = input('\n休息結束時間?(ex:1300, 預設為開始時間加一小時，不考慮休息時間在凌晨)')
        if len(rest_end_time) == 0:
            rest_end_time = int(rest_start_time) + 100
    
        #異常說明
        rest_explanation = input('\n異常說明原因(預設為\'休息\')?')
        if len(rest_explanation) == 0:
            rest_explanation = '休息'

        #格式調整
        rest_start_time = str(rest_start_time)[0:2] + ':' + str(rest_start_time)[2:4]
        rest_end_time = str(rest_end_time)[0:2] + ':' + str(rest_end_time)[2:4]
        
    #工作內容
    workContent = input('\n異常工作內容(預設為\'文書處理\')?')
    if len(workContent) == 0:
            workContent = '文書處理'

#執行時間
if carded == '0' or carded == '1':
    set_Time = input('\n預定執行時間?(ex: 2300，24 制，預設馬上執行)')
    if len(set_Time) == 0:
        set_Time = '0000'
        
elif carded == '2':
    set_Time = input('\n預定執行時間(上班)?(ex: 2300，24 制，預設馬上執行)')
    if len(set_Time) == 0:
        set_Time = '0000'

    set_Time2 = input('\n預定執行時間(下班)?(ex: 2300，24 制，預設馬上執行)')
    if len(set_Time2) == 0:
        set_Time2 = '0000'
        
#讀取 Model
#務必確認 svc_model.pkl 檔案跟 python 檔案要在同個層資料夾中
svc_model2 = joblib.load('svc_model.pkl')

# 關閉通知
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
options.add_experimental_option('prefs', prefs)
options.add_argument('disable-infobars')
#背景執行
#option.add_argument('headless')

# 啟動selenium 務必確認 driver 檔案跟 python 檔案要在同層資料夾中
#這裡會先啟動一個空白頁籤 Chrome
driver = webdriver.Chrome(options = options)

#倒數計時
countdown(set_Time)

#登入
login(driver, site, svc_model2, account, password)

try:
    ##函式裡穿插動作
    do(driver)

    #依據需求打上下班卡
    if carded == '0':
    
        #找到上班打卡
        commit = driver.find_element_by_css_selector('#B4001A_btnIN')
        print('按下上班按鈕囉~~')
        commit.click()
        sleep(0.2)

    elif carded == '1':
    
        ##先填寫四欄的內容
        #包含休息時間
        if rest == 'y' or rest == '1':
            #休息時間左
            context = driver.find_element_by_css_selector('#B4001A_txtBREAK_STM')
            context.send_keys(rest_start_time)# 12:00
            sleep(0.2)
    
            #休息時間右
            context = driver.find_element_by_css_selector('#B4001A_txtBREAK_ETM')
            context.send_keys(rest_end_time)# 13:00
            sleep(0.2)
    
            #異常說明
            context = driver.find_element_by_css_selector('#B4001A_txtEXPLAIN_NOTES')
            context.send_keys(rest_explanation)
            sleep(0.2)
        
        #工作內容
        commit = driver.find_element_by_css_selector('#B4001A_txtJOB_NOTES')
        commit.send_keys(workContent)
        sleep(0.2)

        #找到下班打卡
        commit = driver.find_element_by_css_selector('#B4001A_btnOFF')
        print('按下下班按鈕囉~~')
        commit.click()
        sleep(0.2)
        
    elif carded == '2':

        #找到上班打卡
        commit = driver.find_element_by_css_selector('#B4001A_btnIN')
        print('按下上班按鈕囉~~')
        commit.click()
        sleep(0.2)

        #登出
        logout(driver)

        #關閉瀏覽器全部標籤頁
        driver.quit()

        print('上班打卡完成\n')
    
        #倒數計時
        countdown(set_Time2)

        #登入
        login(driver, site, svc_model2, account, password)

        ##函式裡穿插動作
        do(driver)

        ##先填寫四欄的內容
        #包含休息時間
        if rest == 'y' or rest == '1':
            #休息時間左
            context = driver.find_element_by_css_selector('#B4001A_txtBREAK_STM')
            context.send_keys(rest_start_time)# 12:00
            sleep(0.2)
    
            #休息時間右
            context = driver.find_element_by_css_selector('#B4001A_txtBREAK_ETM')
            context.send_keys(rest_end_time)# 13:00
            sleep(0.2)
    
            #異常說明
            context = driver.find_element_by_css_selector('#B4001A_txtEXPLAIN_NOTES')
            context.send_keys(rest_explanation)
            sleep(0.2)
        
        #工作內容
        context = driver.find_element_by_css_selector('#B4001A_txtJOB_NOTES')
        context.send_keys(workContent)
        sleep(0.2)

        #找到下班打卡
        commit = driver.find_element_by_css_selector('#B4001A_btnOFF')
        print('按下下班按鈕囉~~')
        commit.click()
        sleep(0.2)
    

    #登出
    logout(driver)
    
except:
    print('發生意外，緊急關閉程式')
    traceback.print_exc()
    
finally:
    #關閉瀏覽器全部標籤頁
    driver.quit()

    print('已結束作業\n')
    system('pause')
