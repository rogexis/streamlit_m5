import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def read_file(name_file):
    return pd.read_csv(name_file, nrows=500)

@st.cache_data
def unique_elements(data):
    return data.unique()[::-1]

@st.cache_data
def chart_hist(data):
    fig, ax = plt.subplots()
    sns.histplot(data, ax=ax)
    return fig

@st.cache_data
def chart_freq(data):
    fig, ax = plt.subplots()
    sns.countplot(x=data, ax=ax)
    plt.xticks(rotation=90)
    return fig

@st.cache_data
def chart_bar(data, x, y):
    fig, ax = plt.subplots()
    sns.barplot(data.reset_index(), x=x, y=y, ax= ax)
    plt.xticks(rotation=90)
    return fig

@st.cache_data
def chart_scatter(x, y):
    fig, ax = plt.subplots()
    sns.scatterplot(x=x, y=y, ax= ax)
    plt.xticks(rotation=90)
    return fig

data = read_file('./content/Employees.csv')
data_plots = data 
st.title('Employees')

sidebar = st.sidebar

with sidebar:
    show_df = st.checkbox('Mostrar DataFrame')
    if show_df:
        text_Eid = st.text_input('Browser', placeholder='Employee_ID, Hometown o Unit')
        selected_E_L = st.selectbox('Filter By Education level', unique_elements(data.Education_Level.append(pd.Series(['All']))))
        selected_cities = st.selectbox('Filter By City', unique_elements(data.Hometown.append(pd.Series(['All']))))
        selected_Unit = st.selectbox('Filter By Unit', unique_elements(data.Unit.append(pd.Series(['All']))))

        
if show_df:

    if text_Eid != '':
        data = data[(data.Employee_ID == text_Eid) | (data.Hometown  == text_Eid) | (data.Unit == text_Eid)]
    
    if selected_E_L != 'All':
        data = data[data.Education_Level == selected_E_L] 

    if selected_cities != 'All':
        data = data[data.Hometown == selected_cities] 

    if selected_Unit != 'All':
        data = data[data.Unit == selected_Unit] 

    st.dataframe(data)
    
    st.header('Employees By Age')
    st.pyplot(chart_hist(data_plots.Age))

    data_by_hometown=data_plots.groupby(by=['Hometown']).mean()

    col1, col2 = st.columns(2)
    with col1:
        st.header('Employees By Unit')
        st.pyplot(chart_freq(data_plots.Unit))
    with col2:
        st.header('Hometown Attrition Rate')
        st.pyplot(chart_bar(data_by_hometown.Attrition_rate, 'Hometown', 'Attrition_rate'))
    
    col3, col4 = st.columns(2)
    with col3:
        st.header('Attrition rate & Age')
        st.pyplot(chart_scatter(data_plots.Attrition_rate, data_plots.Age))
    with col4:
        st.header('Attrition rate & Time of Service')
        st.pyplot(chart_scatter(data_plots.Attrition_rate, data_plots.Time_of_service))