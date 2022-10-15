##批量圖片辨識
##批量圖片重組>>影像處理>>OCR辨識並重新命名檔名
##測試完成

from os import path, system, listdir, rename
from time import sleep


##指定副檔名
pictureFileExtension = 'jpg'
##要增加的值
'''要輸入喔~'''
value = ''

###main
##讀取目錄路徑
#'F:\\python作品\\登入學生系統\\test2'
pictrueInputDir = #str(input('輸入圖片目錄，可以直接拖曳至此：'))

if not path.isdir(pictrueInputDir):
    print('路徑驗證異常，請確認路徑')

count = 0
   
# 逐一查詢檔案清單
for item in listdir(pictrueInputDir):
    #緩衝一下
    sleep(0.2)
    
    target = path.join(pictrueInputDir, item)
    
    if path.isdir(target):
    #使用 isdir 檢查是否為目錄
    #使用 join 的方式把路徑與檔案名稱串起來
        print('\n目錄: ', item)    
    
    elif path.isfile(target):
    #使用isfile判斷是否為檔案
        print('\n發現檔案: ', item)

        rename(path.join(pictrueInputDir, item),
                  path.join(pictrueInputDir, value + item))

        print('\n- 更名為: ', value + item)

        count += 1
        
print('\n共計完成' + str(count) + '筆')
print('\n作業完成\n')
system('pause')

