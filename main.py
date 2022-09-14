import streamlit as st
import pandas as pd
import plotly.express as px

from functions import plot_histograms, plot_relations, create_user_test
from training import y_test, y_pred, lr

tips = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')

st.write('''
# Прогноз размера чаевых

Для этого приложения используется датасет [*tips.csv*](https://github.com/mwaskom/seaborn-data/blob/master/tips.csv).

Описание датасета доступно по ссылке: https://vincentarelbundock.github.io/Rdatasets/doc/reshape2/tips.html

### Описание данных

Для начала посмотрим, как распределены наши данные.
''')
columns = ['Размер счета', 'Пол', 'Наличие курильщиков', 'День недели', 'Время дня', 'Размер компании']
y_type = st.selectbox("Выбери параметр:", columns)

st.plotly_chart(plot_histograms(y_type, tips), use_container_width=True)

st.write('''
Теперь посмотрим, как различные параметры влияют на размер чаевых.
''')

y_type2 = st.selectbox("Еще раз выбери параметр:", columns)

st.plotly_chart(plot_relations(y_type2, tips), use_container_width=True)

st.write('''
### Обучение модели

Для обучения модели данные были случайно разделены в соотношении 70 % - данные для обучения, 30 % - данные для предсказания.

Обучение осуществлялось с помощью модели [Линейной Регрессии](https://en.wikipedia.org/wiki/Linear_regression)

Успешность модели оцениваем с помощью коэффициента детерминации. В данной модели коэффициент равен:

$$ R\^2 $$ = 0.422797

такой показатель означает, что наша модель хорошо (но не отлично) предсказала реальный размер чаевых.
''')

fig = px.scatter(x=y_test, y=y_pred, trendline="ols")
fig.update_layout(title="Успешность модели",
                  xaxis_title="Реальный размер чаевых",
                  yaxis_title="Предсказанный размер чаевых")

st.plotly_chart(fig, use_container_width=True)

st.write('''
### Прогноз

Теперь с помощью полученной модели можно предсказать, сколько вы оставили чаевых.
''')

total_bill = st.slider("Выберите размер вашего счета:", min_value=3, max_value=50)
sex = st.radio("Выберите ваш пол:", ['Женский', 'Мужской'])
time = st.radio("В какое время дня вы посетили заведение?", ['Обед', 'Ужин'])
day = st.selectbox("В какой день недели вы посетили заведение?", ['четверг', 'пятница', 'суббота', 'воскресенье'])
smoker = st.radio("В вашей компании есть курящие?", ['Да', 'Нет'])
size = st.slider("Выберите размер вашей компании", min_value=1, max_value=6)

user_test = create_user_test(total_bill, sex, time, smoker, size, day)

user_pred = lr.predict(user_test)

st.write('''
##### Размер ваших чаевых:
''')

st.metric(label="", value=user_pred[0])
