import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

repo_url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
mx_regions_geo = requests.get(repo_url).json()

def get_data():
    path = "data/indicadores_turisticos.xlsx"
    df = pd.read_excel(path, sheet_name = "Datatur (2)")
    df = df.rename(columns = {"Llegada_de_Turistas_Nacionales": "Nacionales",
                              "Llegada_de_Turistas_Extranjeros": "Extranjeros",
                              "Cuartos_Disponibles_": "Cuartos",
                              "Porcentaje_de_Ocupación_Total": "Ocupacion"
                            })
    df.Estado = df.Estado.apply(lambda x: "México" if x == "Estado de México" else x)

    return df

def get_state_info(x):
    df = get_data()
    
    if x == "Nacional":
         df = df.query("Estado == 'Nacional'")
         return df
    if x == "Estatal":
         df = df.query("Centro_Turístico == 'Total' & Estado != 'Nacional'")
         
         return df

def get_list():
    df = get_data()
    estados = df["Estado"].unique()
    estados = list(estados)

    return estados

def get_centers(state):
    df = get_data()
    c_turisticos = df[df["Estado"] == state]["Centro_Turístico"].unique()

    return c_turisticos


def arrive():
    fig = px.bar(get_state_info("Nacional"), x="Año", y=["Nacionales","Extranjeros"], 
                title="Llegada de Turistas",
                template="simple_white",
                text_auto= ".2s",
                color_discrete_sequence=["#B38E5D", "#D4C19C"])
    fig.update_layout(hovermode="x unified")
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_xaxes(
                tickangle = 270,
                title_font = {"size": 14},
                color = "black"
                )
    fig.update_yaxes(
                title_font = {"size": 14},
                color = "black",
                visible = False
                )
    fig.update_layout(
                legend=dict(orientation='h', title = "", yanchor='bottom',xanchor='center',y=-0.5,x=0.5)
                )
    fig.update_layout(title_text="Llegada de turistas<br><sup>(Millones de turistas)</sup>", title_x=0.5, title_xanchor = "center")
    fig.update_traces(hovertemplate = '%{y:,.0f} ')
        
    return fig

def availability():
    df = get_state_info("Nacional")
    df["Cuartos"] = df["Cuartos"]/1000000

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x = df["Año"], y = df["Cuartos"],
            marker=dict(color = "#D4C19C"), 
            name="Cuartos disponibles (millones)",
            text = df["Cuartos"],
            texttemplate = "%{y:,.0f}",
            textposition='inside'),
            secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x = df["Año"], y = df["Ocupacion"],
                mode='markers+text',
                marker=dict(color="#9D2449"),
                name="Porcentaje de ocupación",
                text= df["Ocupacion"],
                texttemplate = "%{y:,.2f}",
                textposition='top center',),
        secondary_y = True,
    )
    fig.update_layout(template="simple_white")

    fig.update_xaxes(title_text="Año")

    # Set y-axes titles
    fig.update_yaxes(title_text="Número de Cuartos", secondary_y=False, range=[0,300])
    fig.update_yaxes(title_text="Porcentaje", secondary_y=True, range=[0,0.6])

    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        hoverlabel=dict(
            font_size=10,
            font_family="Montserrat"
        )
    )
    fig.update_layout(
                legend=dict(orientation='h', title = "", yanchor='bottom',xanchor='center',y=-0.5,x=0.5)
                )
    fig.update_layout(title_text="Cuartos disponibles y porcentaje de ocupación<br><sup>(Millones de cuartos y porcentaje)</sup>", title_x=0.5, title_xanchor = "center")
    fig.update_traces(hovertemplate = '%{y:,.2f}')

    return fig

def gen_table_state(x):
    df = get_state_info("Nacional")
    if x == "llegadas":
        df = df[["Año", "Nacionales", "Extranjeros"]]
        df["Año"] = df["Año"].apply(str)
        return df
    if x == "disponibilidad":
        df = df[["Año", "Cuartos", "Ocupacion"]]
        df["Año"] = df["Año"].apply(str)
        return df

def table_style_state(x):
    df = gen_table_state(x)
    # style
    th_props = [
    ('font-size', '16px'),
    ('text-align', 'center'),
    ('font-weight', 'bold'),
    ('color', '#ffffff'),
    ('background-color', '#B38E5D')
    ]

    td_props = [
    ('font-size', '14px')
    ]

    styles = [
    dict(selector="th", props=th_props),
    dict(selector="td", props=td_props)
    ]

    # table
    df = (df.style
        .format(precision=2, thousands=",")
        .set_properties(**{'text-align': 'left'})
        .set_table_styles(styles))
    
    return df

def gen_map(var):
    df = get_state_info("Estatal")
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

