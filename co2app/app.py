import streamlit as st

# import folium
# from streamlit_folium import st_folium
from utils import load_data, make_total_by_year, make_top_installations, get_countries

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("ArcelorMittal CO2 Emissions")

    st.write(
        "This app allows you to explore data from the EU ETS register on ArcelorMittal's CO2 emissions."
    )

df = load_data()


# Inputs
with st.sidebar:
    countries = get_countries(df)

    country = st.selectbox("Country", ["All"] + countries)

    years = st.select_slider("Years", list(range(2006, 2022)), value=(2006, 2021))

# Dataset filtering


if country != "All":
    df = df[df["NationalAdministrator"] == country]

# Results

st.subheader("Total by year")


cols = st.columns([15, 5])
with cols[0]:
    total_by_year = make_total_by_year(df, start_year=years[0], end_year=years[1])
    st.bar_chart(total_by_year)

with cols[1]:
    total_all_years = total_by_year["Total by Year"].sum()
    st.metric("Total (all years, tons)", f"{total_all_years:,.0f}")

with st.expander("Show the data"):
    st.dataframe(total_by_year, use_container_width=True)


st.subheader("Top Installations")
top_installations = make_top_installations(df, start_year=years[0], end_year=years[1])
st.dataframe(
    top_installations[["ID", "InstallationNameOrAircraftOperatorCode", "Total"]],
    use_container_width=True,
)


# st.subheader("Emissions Map")
# m = folium.Map(
#     location=[48, 14],
#     zoom_start=5,
#     tiles="cartodbpositron",
#     min_zoom=5,
#     max_zoom=5,
#     # prefer_canvas=True,
#     max_bounds=True,
#     zoomDelta=0.5,
#     min_lat=35,
#     max_lat=58,
#     min_lon=-13,
#     max_lon=35,
# )
#
#
# for index, row in top_installations.sort_values(
#     "Total", axis=0, ascending=False
# ).iterrows():
#     lat = row["Latitude"]
#     lon = row["Longitude"]
#     tooltip = f"""<b>{row["ID"]} - {row["InstallationNameOrAircraftOperatorCode"]}</b><br>
#         Total: {row["Total"]:,.0f} tons"""
#     radius = float(row["Total"]) / 1500000
#
#     folium.CircleMarker(
#         [row["Latitude"], row["Longitude"]],
#         tooltip=tooltip,
#         radius=radius,
#         color="crimson",
#         fill=True,
#         fill_color="crimson",
#         fill_opacity=0.3,
#         opacity=0.3,
#         weight=2,
#     ).add_to(m)
#
# folium.plugins.Fullscreen().add_to(m)
#
# st_folium(m, width=1200, height=800)
#
# st.map(
#     top_installations.rename({"Longitude": "longitude", "Latitude": "latitude"}, axis=1)
# )
