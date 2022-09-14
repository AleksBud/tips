import streamlit as st
import pandas as pd
import plotly.express as px

from functions import plot_histograms, plot_relations, create_user_test
from training import y_test, y_pred, y_pred2, lr, rf

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

Обучение осуществлялось с помощью:
- [Случайных лесов](https://en.wikipedia.org/wiki/Random_forest)
- [Линейной Регрессии](https://en.wikipedia.org/wiki/Linear_regression)


Успешность модели оцениваем на данных для предсказания с помощью коэффициента детерминации ($$ R\^2 $$):
- Если показатель равен 0, то модель никогда не предсказывает точно.
- Если показатель равен 1, то модель всегда предсказывает точно.
Давайте, определим, если показатель варьируется между 0,4 и 0,6, то такая модель хорошая. Соответственно, чем выше показатель, тем лучше модель.
''')

model = st.radio("Выберите модель:", ['Случайные леса', 'Линейная регрессия'])
if model == 'Случайные леса':
    fig = px.scatter(x=y_test, y=y_pred2, trendline="ols")
    fig.update_layout(title="Успешность модели",
                      xaxis_title="Реальный размер чаевых",
                      yaxis_title="Предсказанный размер чаевых")
    st.plotly_chart(fig, use_container_width=True)
    st.write('''Коэффициент ($$ R\^2 $$) в данной модели равен: 0.36''')

if model == 'Линейная регрессия':
    fig = px.scatter(x=y_test, y=y_pred, trendline="ols")
    fig.update_layout(title="Успешность модели",
                      xaxis_title="Реальный размер чаевых",
                      yaxis_title="Предсказанный размер чаевых")
    st.plotly_chart(fig, use_container_width=True)
    st.write('''Коэффициент ($$ R\^2 $$) в данной модели равен: 0.42''')

st.write('''
### Прогноз

Теперь с помощью построенных моделей можно предсказать, сколько вы оставили чаевых.
''')

col1, col2 = st.columns(2)

total_bill = col2.slider("Выберите размер вашего счета:", min_value=3, max_value=50)
sex = col1.radio("Выберите ваш пол:", ['Женский', 'Мужской'])
time = col1.radio("В какое время дня вы посетили заведение?", ['Обед', 'Ужин'])
day = col2.selectbox("В какой день недели вы посетили заведение?", ['четверг', 'пятница', 'суббота', 'воскресенье'])
smoker = col1.radio("В вашей компании есть курящие?", ['Да', 'Нет'])
size = col2.slider("Выберите размер вашей компании", min_value=1, max_value=6)

user_test = create_user_test(total_bill, sex, time, smoker, size, day)

fit = st.selectbox("Выберите модель для предсказания", ['Случайные леса', 'Линейная регрессия'])

st.write('''
##### Размер ваших чаевых:
''')
if fit == 'Случайные леса':
    user_pred = rf.predict(user_test)
    st.metric(label="", value=f'{round(user_pred[0], 2)} $')

if fit == 'Линейная регрессия':
    user_pred = lr.predict(user_test)
    st.metric(label="", value=f'{round(user_pred[0], 2)} $')
