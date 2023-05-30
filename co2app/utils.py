import pandas as pd
import streamlit as st

DATA_FILEPATH = "ArcelorMittal_CO2_Emissions.csv"


@st.cache_data
def load_data(data_filepath=DATA_FILEPATH):
    df = pd.read_csv(data_filepath)
    return df


@st.cache_data
def make_total_by_year(df, start_year=2006, end_year=2022):
    """Returns a dataframe with emissions for each year."""
    total_by_year = df[[str(y) for y in list(range(start_year, end_year + 1))]].sum()
    total_by_year = pd.DataFrame(total_by_year)
    total_by_year = total_by_year.rename({0: "Total by Year"}, axis=1)

    return total_by_year


@st.cache_data
def make_top_installations(df, start_year=2006, end_year=2022):
    """Returns a dataframe with all installations, from top emitting to less emitting."""
    top_installations = df.copy()
    years = [str(y) for y in list(range(start_year, end_year + 1))]

    top_installations["Total"] = top_installations[years].sum(axis=1)

    return top_installations.sort_values("Total", ascending=False)


@st.cache_data
def get_countries(df):
    """Returns the list of countries in the dataset."""
    countries = df["NationalAdministrator"].unique()

    return sorted(countries)
