import pandas as pd
import plotly.express as px

def get_pib():
    path = "data/indicadores_turisticos.xlsx"
    df = pd.read_excel(path, sheet_name = "PIB")
    df = pd.melt(df, id_vars = "Concepto").rename(columns={'variable': 'Año', 'value':'PIB'})
    df["Concepto"] = df.Concepto.apply(lambda x: x.strip())

    df = df[(df["Concepto"] == "Total turístico") | (df["Concepto"] == "Bienes") | (df["Concepto"] == "Servicios")]
    return df

def gen_graph():
    df = get_pib()
    fig = px.line(df, x="Año", y="PIB", 
              title='Total del país',
              template="simple_white",
              color='Concepto',
              color_discrete_sequence=["#9D2449", "#13322B", "#B38E5D"])
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(
        tickangle = 270,
        title_font = {"size": 18},
        color = "black"
        )
    fig.update_xaxes(
        title_font = {"size": 14},
        color = "black"
        )
    fig.update_layout(title_text="Pib Turístico<br><sup>(Mil mdp a precios del 2013)</sup>", 
                      title_x=0.5, 
                      title_xanchor = "center")
    fig.update_traces(hovertemplate = '%{y:,.0f} ')
    fig.update_layout(
        legend=dict(orientation='h', title = "", yanchor='bottom',xanchor='center',y=-0.5,x=0.5)
        )
    
    return fig

def gen_table():
    path = "data/indicadores_turisticos.xlsx"
    df = pd.read_excel(path, sheet_name = "PIB")
    df = (df.set_index("Concepto")).T
    df = (df/1000)
    df.columns = df.columns.str.strip()
    df = df[['Total del país', 'Total turístico', 'Bienes', "Servicios"]]
    df = df.reset_index()
    df = df.rename(columns={"index": "Año",
                            'Total del país': "PIB Total",
                            "Total turístico": "PIB Turiístico"})
    df = df.query("Año >= '2010'")

    return df

def table_style():
    df = gen_table()
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
        .format(precision=0, thousands=",")
        .set_properties(**{'text-align': 'left'})
        .set_table_styles(styles))
    
    return df