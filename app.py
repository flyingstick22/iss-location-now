import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests
import json

def app():

    #colleting data from API's and place them in variables
    iss_location = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
    astronauts_in_iss = requests.get("http://api.open-notify.org/astros.json")
    location  = iss_location.json()
    data1 = astronauts_in_iss.json()
    latitude = float(location["latitude"])
    longitude = float(location["longitude"])
    speed = int(location["velocity"])
    altitude = int(location["altitude"])

    #map & metrics visualization
    st.title("Where is ISS ?")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Speed km/h", speed)
    col2.metric("Altitude in km", altitude)
    col3.metric("Latitude", round(latitude,3))
    col4.metric("Longitude", round(longitude,3))
    location_for_map = pd.DataFrame({
        'lat' : [latitude],
        'lon' : [longitude]
    })
    st.map(location_for_map, zoom=1)

    #creating table only with ISS astronauts
    df = pd.json_normalize(data1, record_path =['people'])
    df2 = df.loc[df["craft"] == "ISS"]
    df3 = df2.name
    hide_table_row_index = """          
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    st.subheader("Astronauts on board")
    col1, col2 = st.columns([3,2])

    #Lottie animation
    with col1:
        lottie_filepath = ("Lottiefiles/astronaut.json")
        with open(lottie_filepath, "r") as f:
            file = json.load(f)
        st_lottie(file, speed=1, height=300, width=300)

    #Table visialization
    with col2:
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df3)

if __name__ == "__main__":
    app()
