import pandas as pd
from common.database import Database
from models.coronadata import CoronaData
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from math import pi
from bokeh.transform import cumsum

def read_mongo():
    data = Database.find("coronadata", {})
    df = pd.DataFrame(list(data))
    return df

def first_graph():
    df = read_mongo()
    
    df_corona = df[df.corona == 'Ja']

    df_new = df_corona['province'].value_counts()

    data = pd.Series(df_new).reset_index(name='corona').rename(columns={'index':'province'})
    data['angle'] = data['corona']/data['corona'].sum() * 2*pi

    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
        tools="hover", tooltips="@province : @corona")

    p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='red', legend='province', source=data)

    return p
    #Stored the figure in components
    # return P and do the bottom part in app.py