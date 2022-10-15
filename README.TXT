附註條件

1.需安裝 Tesseract-OCR 程式(tesseract-ocr-w64-setup-v5.0.0-alpha.20200328)

2.修改後的數據檔(digits_onlyNum)也需至於指定目錄
(C:\Program Files\Tesseract-OCR\tessdata\configs\)

3.輔助程式大部分都....沒介面，須配合閱讀程式碼操作

4.20191202更新
### 錯誤解決 pytesseract.pytesseract.TesseractNotFoundError: 
tesseract is not installed or it's not in your path ###

找到 pytesseract 模組裡的 pytesseract.py 文件進行修改
(?:\python\python38\lib\site-packages\pytesseract\pytesseract.py , ? = python 安裝槽)
找到：tesseract_cmd = 'tesseract'

改成：tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tesseract_cmd所賦予的值其實就是tesseract的安裝路徑

5. chromedriver.exe 要跟程式同一層，不然會烙賽