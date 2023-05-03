import pandas as pd
import plotly.express as px
import requests
from pathlib import Path

repo_url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
mx_regions_geo = requests.get(repo_url).json()

def get_state_info(var):
    path = "data/indicadores_turisticos.xlsx"
    df = pd.read_excel(path, sheet_name = "Datatur (2)")
    df = (df[(df["Centro_Turístico"] == "Total") & (df["Estado"] != "Nacional")]
          .rename(columns={"Llegada_de_Turistas_Nacionales": "Nacionales",
                           "Llegada_de_Turistas_Extranjeros": "Extranjeros"}))
    df.Estado = df.Estado.apply(lambda x: "México" if x == "Estado de México" else x)
    return df

def gen_map(var):
    df = get_state_info(var)
    min = df[var].min()
    max = df[var].max()

    fig = px.choropleth(df, 
                            geojson= mx_regions_geo, 
                            locations = 'Estado', # nombre de la columna del Dataframe
                            featureidkey= 'properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                            color = var, #El color depende de las cantidades
                            color_continuous_scale = ["#d2eee7","#1f5247", "#040b0a"],
                            range_color = (min, max),
                            hover_name = "Estado",
                            hover_data = {"Estado": False, var:':.2f'},
                            custom_data=['Estado', var],
                            center = {'lat': 25, 'lon': -99}
                    )
    hovertemp = '<b>%{customdata[0]}<b><br>'
    hovertemp += '<b>%{customdata[1]} Millones<b><br>'
    fig.update_geos(showcoastlines = False, showland=False, visible = False, fitbounds="locations")
    fig.update_traces(hovertemplate=hovertemp)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    ))

    return fig

