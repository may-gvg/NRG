import warnings
import cufflinks
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

# loading & transforming data

df2 = pd.read_csv("World Energy Consumption.csv")

df2 = df2[(df2.country == "Poland") | (df2.country == "Italy") | (df2.country == "Netherlands")
          | (df2.country == "Spain") | (df2.country == "Germany") | (df2.country == "France")]

df2 = df2[df2.year == 2020]

df = df2[['country', 'biofuel_electricity', 'hydro_electricity', 'nuclear_electricity', 'solar_electricity',
          'wind_electricity', 'other_renewable_electricity', 'coal_electricity', 'gas_electricity',
          'oil_electricity']]

production_df = df.rename(columns={'biofuel_electricity': 'biofuel', 'hydro_electricity': 'hydro',
                                   'nuclear_electricity': 'nuclear', 'solar_electricity': 'solar',
                                   'wind_electricity': 'wind', 'other_renewable_electricity': 'other_renewable',
                                   'coal_electricity': 'coal', 'gas_electricity': 'gas', 'oil_electricity': 'oil',
                                   'country': 'Country'})

# production_df = production_df.rename(columns={'country': 'Country'})

# app setup

st.set_page_config(layout="wide")

st.markdown("## Energy Production in 2020")

# scatter 1

st.sidebar.markdown("### Scatter Chart: Relationship Between Energy Types per Country :")

ingredients = production_df.drop(labels=["Country"], axis=1).columns.tolist()

x_axis = st.sidebar.selectbox("X-Axis", ingredients)
y_axis = st.sidebar.selectbox("Y-Axis", ingredients, index=1)

if x_axis and y_axis:
    scatter_fig = production_df.iplot(kind="scatter", x=x_axis, y=y_axis, mode="markers", categories="Country",
                                      asFigure=True, opacity=1.0,
                                      xTitle=x_axis.replace("_", " ").capitalize(),
                                      yTitle=y_axis.replace("_", " ").capitalize(),
                                      title="{} vs {}".format(x_axis.replace("_", " ").capitalize(),
                                                              y_axis.replace("_", " ").capitalize()))

# bar 2

st.sidebar.markdown("### Bar Chart: Production of Energy Types per Country : ")

avg_production_df = production_df.groupby(by=["Country"]).sum()

bar_axis = st.sidebar.multiselect(label="Bar Chart Ingredient", options=avg_production_df.columns.tolist(),
                                  default=["solar", "gas", "coal"])

if bar_axis:
    bar_fig = avg_production_df[bar_axis].iplot(kind="bar", barmode="stack", xTitle="Country",
                                                title="Distribution of Energy Types Per Country",
                                                asFigure=True, opacity=1.0);
else:
    bar_fig = avg_production_df[["coal"]].iplot(kind="bar", barmode="stack",xTitle="Country",
                                                title="Distribution of Coal Per Country",
                                                asFigure=True, opacity=1.0);

# hist 3

st.sidebar.markdown("### 3.Histogram: Distribution of Energy Types : ")

hist_axis = st.sidebar.multiselect(label="Histogram Ingredient", options=ingredients, default=["coal", "solar"])
bins = st.sidebar.radio(label="Bins :", options=[10, 20, 30, 40, 50], index=1)

if hist_axis:
    hist_fig = production_df.iplot(kind="hist", keys=hist_axis, xTitle="Energy Types", bins=bins,
                                   title="Distribution of Energy Types", asFigure=True, opacity=1.0);
else:
    hist_fig = production_df.iplot(kind="hist", keys=["coal"], xTitle="Coal", bins=bins, title="Distribution of Coal",
                                   asFigure=True, opacity=1.0);

# pie 4
production_df["production"] = production_df.biofuel + production_df.hydro + production_df.nuclear \
                              + production_df.solar + production_df.wind + production_df.other_renewable \
                              + production_df.coal + production_df.gas + production_df.oil

production_cnt = production_df.groupby(by=["Country"]).sum()[['production']].rename(columns={"production": "Count"}) \
    .reset_index()

pie_fig = production_cnt.iplot(kind="pie", labels="Country", values="Count", title="Total Production Per Country",
                               hole=0.4, asFigure=True)

# layout

container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        scatter_fig
    with col2:
        bar_fig

container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        hist_fig
    with col4:
        pie_fig

