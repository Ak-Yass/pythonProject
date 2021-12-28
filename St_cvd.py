import streamlit as st
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import locale
from locale import atof, setlocale, LC_NUMERIC
import pymongo
import altair as alt
from streamlit_folium import folium_static
import folium

URI = "mongodb+srv://admin:admin@cluster0.zb4wy.mongodb.net/covid-database?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'

db = client["covid-database"]
df = db.Iris
df = pd.DataFrame(list(df.find()))

df.drop('_id', inplace=True, axis=1)
df2 = df.set_index('Countries')
df2.index.names = [None]

ddff = df

ddff.replace('USA', "United States of America", inplace=True)
ddff.replace('Tanzania', "United Republic of Tanzania", inplace=True)
ddff.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace=True)
ddff.replace('Congo', "Republic of the Congo", inplace=True)
ddff.replace('Lao', "Laos", inplace=True)
ddff.replace('Syrian Arab Republic', "Syria", inplace=True)
ddff.replace('Serbia', "Republic of Serbia", inplace=True)
ddff.replace('Czechia', "Czech Republic", inplace=True)
ddff.replace('UAE', "United Arab Emirates", inplace=True)
ddff.replace('North Macedonia', "Macedonia", inplace=True)
ddff.replace('UK', "United Kingdom", inplace=True)
ddff.replace('CAR', "Central African Republic", inplace=True)
ddff.replace('DRC', "Democratic Republic of the Congo", inplace=True)

n = folium.Map(location=[20, 0], tiles="OpenStreetMap", zoom_start=2)

# add marker one by one on the map
for i in range(0, len(ddff)):
    folium.Marker(
        location=[ddff.iloc[i]['lat'], ddff.iloc[i]['long']],
        popup=ddff.iloc[i]['Total Cases'],
        icon=folium.DivIcon(
            html=f"""<div style="font-family: courier new; color: blue">{ddff.iloc[i]['Total Cases']}</div>""")
    ).add_to(n)

m = folium.Map()

folium.Choropleth(
    geo_data=country_shapes,
    name='choropleth',
    data=ddff,
    columns=['Countries', 'Total Cases'],
    key_on='feature.properties.name',
    fill_color='PuRd',
    nan_fill_color='green',
    legend_name='Total Covid Cases',

).add_to(m)

for i in range(0, len(ddff)):
    html = f"""
        <p>{ddff.iloc[i]['Countries']} contains: </p>
        <h1> {ddff.iloc[i]['Total Cases']}</h1>
        """

    folium.Marker(
        location=[ddff.iloc[i]['lat'], ddff.iloc[i]['long']],
        popup=html,
    ).add_to(m)

st.markdown("""
    <style>
    .reportview-container {
        background: url("https://www.desktopbackground.org/download/2560x1600/2010/12/16/127022_light-grey-backgrounds-hd_2560x1600_h.jpg")
    }
   .sidebar .sidebar-content {
        background: url("")
    }
    </style>
    """,
            unsafe_allow_html=True
            )

add_selectbox = st.sidebar.selectbox(
    'Select what to view',
    ('Welcome', 'Raw data', 'Plots', 'Maps')
)

if add_selectbox == 'Welcome':
    st.title("WELCOME TO Covid bot tracker")

if add_selectbox == 'Raw data':
    st.title("Raw DataFrame")
    st.text("dataframe head")
    st.dataframe(df2.head())
    user_input = st.text_input("Search a specific Country", "")
    if st.button("Search"):
        st.dataframe(df.loc[df['Countries'] == user_input])

    if st.button("Show All countries"):
        st.dataframe(df2)

if add_selectbox == 'Plots':
    st.title("Plots")
    st.bar_chart(df2.head())
    c = alt.Chart(df.head()).mark_bar().encode(
        x='Countries',
        y='Total Cases',

    )
    st.altair_chart(c, use_container_width=True)

    st.markdown("""
    <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=15800df9-8c31-40b7-85c4-be096152776f&maxDataAge=3600&theme=dark&autoRefresh=true">
    </iframe>
    """, unsafe_allow_html=True)

    st.markdown("""
    <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=26af633d-2d92-42f2-899f-66979962693d&maxDataAge=3600&theme=dark&autoRefresh=true">
    </iframe>
    """, unsafe_allow_html=True)

if add_selectbox == 'Maps':
    st.title("Maps")
    st.text("mongo")
    st.markdown("""
        <iframe style="background: #21313C;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=fe31b2f8-39cf-4886-8761-6768dd1dc0e2&maxDataAge=3600&theme=dark&autoRefresh=true">
        </iframe>
        """, unsafe_allow_html=True)
    st.text("Map + numbers")
    folium_static(n)
    st.text("Chloro map")
    folium_static(m)
    st.text("Death map mongo")
    st.markdown("""
        <iframe style="background: #FFFFFF;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" width="640" height="480" src="https://charts.mongodb.com/charts-e-shop-mhnfu/embed/charts?id=f19def7f-76c2-48c7-a29c-7658e91bfd72&maxDataAge=3600&theme=light&autoRefresh=true">
        </iframe>"""
                , unsafe_allow_html=True)