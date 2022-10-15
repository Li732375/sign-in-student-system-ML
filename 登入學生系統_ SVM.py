##自動登入並登出關閉

##介面完成
##測試完成

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import system

from os import sep, path, system, mkdir, listdir
from PIL import Image, ImageEnhance, ImageFilter
from time import time, sleep, localtime

import joblib, stdiomask

import numpy as np

#https://www.facebook.com/
site = 'https://webap.nptu.edu.tw/web/Secure/default.aspx?sIndex=2'
#帳號
account = input('帳號?')
#密碼至少首位要大寫
password = stdiomask.getpass(prompt = '密碼(至少首位要大寫)?', mask = '密')

#讀取 Model
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

# 啟動selenium 務必確認driver 檔案跟python 檔案要在同個資料夾中
driver = webdriver.Chrome(options = options)


while True:
    driver.get(site)
    sleep(1.8)

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

    print('- 影像處理第一部分完成')

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
    print(parts.shape)
    print()
    
    answer = svc_model2.predict(parts)    
    print(answer)
    code = ''.join(str(x) for x in answer)
    print('辨識結果：', code)        
    print()
    
    #輸入答案
    context = driver.find_element_by_css_selector('#LoginStd_txtCheckCode')
    context.send_keys(code)
    
    #按下登入紐
    context = driver.find_element_by_css_selector('#LoginStd_ibtLogin')
    context.click()
    sleep(1.5)

    #獲取alert對話方塊
    #下列為舊寫法，已棄用
    #alert = driver.switch_to.alert()
    alert = driver.switch_to.alert
    alert_info = alert.text
    print()
    print(alert_info)
    alert.accept()
    sleep(0.5)

    #為驗證碼錯誤時而設，待補強
    #亦可以直接重啟程式就好
    
    if alert_info == '您目前已經登錄系統中，無法重複登入，如果您前一次是非正常狀態下登出，請等5分鐘後再登入!!':      
        t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
        print(t + ' 登入失敗\n')

        #關閉瀏覽器全部標籤頁
        driver.quit()
        system('pause')
        
    elif alert_info == '驗證碼不符!!':
        t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
        print(t + ' 登入失敗\n')
        print('嘗試重新登入')
        continue
    
    elif alert_info == '因為你太久沒有操作網頁，網頁權限已過期，為了安全考量，系統將自動登出，敬請見諒!!':
        t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
        print(t + ' 登入失敗\n')
        print('嘗試重新登入')
        continue
    
    else:
        print('\n登入成功\n')
    
    break   

#可以穿插任意動作
'''

'''

##進去之後是站中站
#左半站'https://webap.nptu.edu.tw/web/Message/MenuTree.aspx'
#右半站'https://webap.nptu.edu.tw/web/Message/Main.aspx'
#而登出僅在右半站才有
driver.get('https://webap.nptu.edu.tw/web/Message/Main.aspx')
sleep(1)

#按下登出紐
context = driver.find_element_by_css_selector('#CommonHeader_ibtLogOut')
context.click()
sleep(1)

#登出確認
alert = driver.switch_to.alert.accept()
sleep(1)

print('\n登出成功\n')
sleep(1)

#關閉瀏覽器全部標籤頁
driver.quit()

print('完成\n')
system('pause')
