import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import joblib
from sklearn.model_selection import StratifiedKFold
from time import time, localtime
from sklearn.manifold import Isomap
import numpy as np

digits = pd.read_csv('imageDataset_8000.csv')
print('資料讀取完成')

print('\n原本樣子:')
print(digits.head())

#移調不要的欄
digits = digits.drop('name', axis = 1)
print('\n調整後:')
print(digits.head())

data_X = digits.loc[:, digits.columns !=  'answer' ]
print('\ndata_X\n:')
print(data_X)

data_Y = digits['answer']
print('\ndata_Y:\n')
print(data_Y)

#答案種類
print('\n答案種類')
answerClass = sorted(data_Y.unique())
print(answerClass)

#分析各項答案個數
print('\n分析各項答案個數(答案, 統計個數)\n')
print(data_Y.value_counts())

#開切
X_train, X_test, y_train, y_test = train_test_split(data_X,
                                                    data_Y,
                                                    test_size = 0.25,
                                                    random_state = 42 )
'''
# Y 資料最小出現數的樣本 / n_splits 最少須為 2
#超過的話亦可以嘗試忽略
#下方 GridSearchCV 參數亦須做對應的修正
#skf = StratifiedKFold(n_splits = 2)

# Set the parameter candidates
#使用網格搜索（Grid search）
parameter_candidates = [
  {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},]

# Create a classifier with the parameter candidates
GridSearchCV_clf = GridSearchCV(estimator = svm.SVC(),
                                param_grid = parameter_candidates,
                                n_jobs = -1)

## Train the classifier on training data
print('\nStart Training ~')

#計時
t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
print('開始時間: ', t)

# Train
GridSearchCV_clf.fit(X_train, y_train)

print('\nFinish Training ~')

t2 = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
print('結束時間: ', t2)

t = t.split(':')
t2 = t2.split(':')
t3 = str(int(t2[0]) - int(t[0])) + ' 時 ' + str(int(t2[1]) - int(t[1])) + ' 分 ' + str(int(t2[2]) - int(t[2])) + ' 秒 '
print('\n訓練時間: ', t3)

# Print out the results 
print('Best score for training data:', GridSearchCV_clf.best_score_)
print('Best `C`:',GridSearchCV_clf.best_estimator_.C)
print('Best kernel:',GridSearchCV_clf.best_estimator_.kernel)
print('Best `gamma`:',GridSearchCV_clf.best_estimator_.gamma)

'''
#建立模型
# Create the SVC model 
svc_model = svm.SVC(C = 1., kernel = 'linear')

print('\nStart Training ~')

#計時
t = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
print('開始時間: ', t)

# Fit the data to the SVC model
svc_model.fit(X_train, y_train)

t2 = str(localtime(time()).tm_hour) + ':' + str(localtime(time()).tm_min) + ':' + str(localtime(time()).tm_sec)
print('結束時間: ', t2)

t = t.split(':')
t2 = t2.split(':')
tDel = (int(t2[0]) - int(t[0]))*60*60 + (int(t2[1]) - int(t[1]))*60 + (int(t2[2]) - int(t[2]))
t3_h = int(tDel/3600)
t3_m = int(tDel/60) - t3_h*60
t3_s = int(tDel) - t3_m*60

t3 = str(t3_h) + ' 時 ' + str(t3_m) + ' 分 ' + str(t3_s) + ' 秒 '
print('\n訓練時間: ', t3)
print('訓練完成\n')

print('測試結果 >>')
predicted = svc_model.predict(X_test)

# Print the classification report of `y_test` and `predicted`
print(metrics.classification_report(y_test, predicted))

# Print the confusion matrix
print(metrics.confusion_matrix(y_test, predicted))


##視覺化
#下面因每次都要關圖片才能繼續，所以先 ban 起來
'''
# 將預測結果置入
plt.imshow(metrics.confusion_matrix(y_test, svc_model.predict(X_test)),
           interpolation = 'nearest',
           cmap = plt.cm.Blues)
plt.title('Confusion matrix')
plt.colorbar()
tick_marks = answerClass
plt.xticks(tick_marks, answerClass)
plt.yticks(tick_marks, answerClass)
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()
'''
#下面因每次都要關圖片才能繼續，所以先 ban 起來
'''
# 對 `digits` 資料降維，屬非線性降維
print('\n降維處理中 >>\n')
X_iso = Isomap(n_neighbors = 10).fit_transform(X_test)

# 在 2x3 的網格上繪製子圖形
fig, ax = plt.subplots(1, 2, figsize = (6, 4))

# 調整圖形的外觀
fig.suptitle('Predicted Versus Training Labels', fontsize = 12,
             fontweight = 'bold')
fig.subplots_adjust(wspace = 0.2, top = 0.85)

# 繪製 SVM 散佈圖
print('\n繪圖中 >>\n')
ax[0].scatter(X_iso[:, 0], X_iso[:, 1])
ax[0].set_title('SVM_Predicted labels')
ax[1].scatter(X_iso[:, 0], X_iso[:, 1])
ax[1].set_title('SVM_Actual Labels')

# 顯示圖形
print('\n顯示圖形 >>\n')
plt.show()
'''

#保存 Model (倘若路徑有資料夾要先建立，否則會出錯)
joblib.dump(svc_model, 'svc_model.pkl')
print('\nsaveed model!')

