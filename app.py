# 
import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv('country_wise_latest.csv')
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# -------------------- TITLE --------------------
st.title("🌍 COVID-19 PRO Dashboard")

# -------------------- SIDEBAR --------------------
st.sidebar.header("🔎 Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country/Region'].dropna().unique()),
    default=["India"] if "India" in df['Country/Region'].values else []
)

# -------------------- METRICS --------------------
st.header("📊 Selected Country Stats")

for country in countries:
    row = df[df['Country/Region'] == country].iloc[0]

    st.subheader(country)
    col1, col2, col3 = st.columns(3)

    col1.metric("New Cases", f"{int(row['New cases']):,}")
    col2.metric("New Deaths", f"{int(row['New deaths']):,}")
    col3.metric("New Recovered", f"{int(row['New recovered']):,}")

# -------------------- COMPARISON --------------------
st.header("📊 Multi-Country Comparison")

if countries:
    compare_df = df[df['Country/Region'].isin(countries)]

    fig = px.bar(
        compare_df,
        x='Country/Region',
        y=['New cases', 'New deaths', 'New recovered'],
        barmode='group',
        title="Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------- TOP 10 --------------------
st.header("🌍 Top 10 Countries (New Cases)")

top10 = df.sort_values(by='New cases', ascending=False).head(10)

fig_top = px.bar(
    top10,
    x='Country/Region',
    y='New cases',
    text='New cases'
)

fig_top.update_traces(texttemplate='%{text:,}', textposition='outside')

st.plotly_chart(fig_top, use_container_width=True)

# -------------------- MAP --------------------
st.header("🌍 World Map")

fig_map = px.choropleth(
    df,
    locations='Country/Region',
    locationmode='country names',
    color='New cases',
    hover_name='Country/Region',
    color_continuous_scale='Reds'
)

st.plotly_chart(fig_map, use_container_width=True)

# -------------------- TABLE --------------------
st.header("🔎 Data Table")
st.dataframe(df)

# -------------------- FOOTER --------------------
st.markdown("---")
st.write("Built with Streamlit 🚀")
