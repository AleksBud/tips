import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

def plot_histograms(y_type, tips):
    if y_type == "Размер счета":
        fig = px.histogram(x=tips['total_bill'])
        fig.update_layout(title="График распределения по размеру счета",
                          xaxis_title="Размер счета",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type == "Пол":
        fig = px.histogram(x=tips['sex'])
        fig.update_layout(title="График распределения по полу",
                          xaxis_title="Пол",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type == "Наличие курильщиков":
        fig = px.histogram(x=tips['smoker'])
        fig.update_layout(title="График распределения по наличию\nкурильщиков в компании",
                          xaxis_title="Есть курильщики?",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type == "День недели":
        fig = px.histogram(x=tips['day'])
        fig.update_layout(title="График распределения по дням недели",
                          xaxis_title="День недели",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type == "Время дня":
        fig = px.histogram(x=tips['time'])
        fig.update_layout(title="График распределения по времени дня",
                          xaxis_title="Время дня",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type == "Размер компании":
        fig = px.histogram(x=tips['size'])
        fig.update_layout(title="График распределения по размеру компании",
                          xaxis_title="Размер компании",
                          yaxis_title="Количество")
        # st.plotly_chart(fig, use_container_width=True)
    return fig

def plot_relations(y_type2, tips):
    if y_type2 == "Размер счета":
        y = tips['tip']
        x = tips['total_bill']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y,mode='markers', marker_size=3))
        fig.update_layout(title="График зависимости от размера счета",
                          xaxis_title="Размер счета",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type2 == "Пол":
        y = tips['tip']
        x = tips['sex']
        fig = go.Figure()
        fig.add_trace(go.Box(x=x, y=y, boxpoints='all', marker_size=2))
        fig.update_layout(title="График зависимости от пола",
                          xaxis_title="Пол",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type2 == "Наличие курильщиков":
        y = tips['tip']
        x = tips['smoker']
        fig = go.Figure()
        fig.add_trace(go.Box(x=x, y=y, boxpoints='all', marker_size=2))
        fig.update_layout(title="График зависимости от наличия\nкурильщиков в компании",
                          xaxis_title="Есть курильщики?",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type2 == "День недели":
        y = tips['tip']
        x = tips['day']
        fig = go.Figure()
        fig.add_trace(go.Box(x=x, y=y, boxpoints='all', marker_size=2))
        fig.update_layout(title="График зависимости от дня недели",
                          xaxis_title="День недели",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type2 == "Время дня":
        y = tips['tip']
        x = tips['time']
        fig = go.Figure()
        fig.add_trace(go.Box(x=x, y=y, boxpoints='all', marker_size=2))
        fig.update_layout(title="График зависимости от времени дня",
                          xaxis_title="Время дня",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)

    if y_type2 == "Размер компании":
        y = tips['tip']
        x = tips['size']
        fig = go.Figure()
        fig.add_trace(go.Box(x=x, y=y, boxpoints='all', marker_size=2))
        fig.update_layout(title="График зависимости от размера компании",
                          xaxis_title="Размер компании",
                          yaxis_title="Размер чаевых")
        # st.plotly_chart(fig, use_container_width=True)
    return fig

def categories_encoder(data):
    data['sex'] = data['sex'].apply(lambda x: 1 if x == 'Female' else 0)
    data['smoker'] = data['smoker'].apply(lambda x: 1 if x == 'Yes' else 0)
    data['time'] = data['time'].apply(lambda x: 1 if x == 'Dinner' else 0)
    data['Thur'] = data['day'].apply(lambda x: 1 if x == 'Thur' else 0)
    data['Fri'] = data['day'].apply(lambda x: 1 if x == 'Fri' else 0)
    data['Sat'] = data['day'].apply(lambda x: 1 if x == 'Sat' else 0)
    data['Sun'] = data['day'].apply(lambda x: 1 if x == 'Sun' else 0)
    data = data.drop('day', axis=1)
    return data

def create_user_test(total_bill, sex, time, smoker, size, day):
    sex = pd.Series(sex).replace(['Женский', 'Мужской'], ['Female', 'Male'])
    smoker = pd.Series(smoker).replace(['Да', 'Нет'], ['Yes', 'No'])
    time = pd.Series(time).replace(['Обед', 'Ужин'], ['Lunch', 'Dinner'])
    day = pd.Series(day).replace(['четверг', 'пятница', 'суббота', 'воскресенье'], ['Thur', 'Fri', 'Sat', 'Sun'])

    user_test = pd.concat([pd.Series(total_bill), sex, smoker, time, pd.Series(size), day], axis=1)
    user_test.columns = ['total_bill', 'sex', 'smoker', 'time', 'size', 'day']

    user_test = categories_encoder(user_test)
    return user_test