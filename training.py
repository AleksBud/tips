import pandas as pd

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from functions import categories_encoder

tips = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')

# preprocessing
tips = categories_encoder(tips)

X = tips.drop('tip', axis=1)
Y = tips['tip']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.70, random_state=20)

lr = LinearRegression()
lr.fit(x_train, y_train)

y_pred = lr.predict(x_test)

metrics.r2_score(y_test, y_pred)
