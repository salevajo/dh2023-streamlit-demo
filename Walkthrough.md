# Create a simple data web app in Python with Streamlit
DataHarvest 2023


## What is Streamlit? Why is it useful?

Streamlit is a Python library or framework dedicated to the creation of data web applications. With it you can:
- Share data with non-technical people in your team.
- Let them analyze and visualize it, without having to sollicit you.
- Stop running jupyter notebooks again & again & again
- Keep the work on analysis & backend code.

#### Alternatives...

- [Dash](https://plotly.com/) by Plotly: Not as simple. Way more verbose. Not fully open-source.
- [Voila](https://voila.readthedocs.io/en/stable/): Turns Jupyter notebooks into interactive web pages.
- [Gradio](https://www.gradio.app/): ML-oriented
- [Streamsync](https://www.streamsync.cloud/introduction.html): Single-dev project. Build the UI visually.
- [Anvil](https://anvil.works/): Drag & drop UI designer. Fast deployment. Some important features are reserved for paid users.

#### Advantages of Streamlit

- Pythonic, easy to use library = quick to develop, easy to maintain
- No need to use web languages (html, css, js). But if you know them, you can use them.
- Well documented, well supported. Bought by Snowflake in March 2022.
- Active community & third-party modules
- Compatible with many useful python mapping & visualization libraries: Altair, Folium, Plotly, PyDeck, VegaLite
- Easy to deploy

#### Drawbacks of Streamlit

- No route handling = may not fit difficult datasets or specific use cases.
- Still evolving fast, hasn't reached maturity. Breaking changes are still frequent.
- Not very flexible. Customization is often hacky.
- Custom components are rather hard to develop, they require a good knowledge of HTML, CSS, Javascript & its frameworks.


## Today's dataset & objectives

#### `ArcelorMittal_CO2_Emissions.csv`
- Scrapped data from the [European Union Transaction Log](https://ec.europa.eu/clima/ets/napMgt.do)
- All ArcelorMittal present and past installations, their years of activity, and their CO2 emissions.
- This is a simplified version of our full dataset.

#### Questions from the newsroom:
- How much CO2 has ArcelorMittal emitted over the years?
- Which installations emit the most CO2?
- Can we see the results by country?
- Can we see the results for the last 5 or 10 years?

## Let's code !

#### Prepare the virtual environment

```bash
# Create a new virtual environment
virtualenv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the libraries we will need
pip install streamlit pandas

# Create requirements file
mkdir co2app
cd co2app
pip freeze > requirements.txt
```

Creating the requirements file is not just good Python practice, it's necessary if you want to put your app online. Streamlit Share (or any other provider) will need it to know which libraries are needed to run your app.

### Prepare the file structure

Let's have a very simple structure:

```
├── .venv
└── co2app
    ├── app.py
    ├── requirements.txt
    ├── utils.py
    └── ArcelorMittal_CO2_Emissions.csv
```

- `app.py`: where the main logic for our app will be.
- `utils.py`: where our data-processing & other functions will be.

#### Streamlit Basics

```python
# app.py

import streamlit as st

st.write('Hello world!')
```

To run the app, fire up a terminal and type:
```bash
streamlit run app.py
```

A browser window should pop up and show the app.

Now let's change the text:
```python
st.write('Hello DataHarvest!')
```

In the browser, we hit the `Rerun` button which just appeared to see the changes.

Let's give our app a title and some explanations.

```python
# app.py
# ...
st.header('ArcelorMittal CO2 Emissions')

st.write("This app allows you to explore data from the EU ETS register on ArcelorMittal's CO2 emissions.")
```

We could also do it in Markdown:

```python
st.markdown("""
## ArcelorMittal CO2 Emissions

This app lets you visualize..
""")
```

You can see other ways of displaying text in Streamlit's documentation: [Text elements](https://docs.streamlit.io/library/api-reference/text)

#### Load & display the data

```python
# app.py
import pandas as pd
# ...
df = pd.read_csv('ArcelorMittal_CO2_Emissions.csv')
```

To display our data, we have a number of choices, let's just use the simplest for now, `st.table`:

```python
# app.py
# ...
st.table(df)
```

The data is ready! Let's process it so we visualize significant data.

#### Data Processing

To process the data, we create functions in the `utils.py` file. Our objective is to answer the first two questions from the newsroom:
- How much CO2 has ArcelorMittal emitted over the years?
- Which installations emit the most CO2?

I won't detail the code here as this is a presentation about streamlit, not pandas. Feel free to just copy and paste.

###### How much CO2 has ArcelorMittal emitted over the years?

```python
def make_total_by_year(df, start_year=2006, end_year=2022):
    """Returns a dataframe with emissions for each year."""

    total_by_year = df[[str(y) for y in list(range(start_year, end_year + 1))]].sum()
    total_by_year = pd.DataFrame(total_by_year)

    total_by_year = df_totals.rename({0: "Total by Year"}, axis=1)

    return total_by_year
```

###### Which installations emit the most CO2?

```python
def make_top_installations(df, start_year=2006, end_year=2022):
    """Returns a dataframe with all installations, from top emitting to less emitting."""
    top_installations = df.copy()

    years = [str(y) for y in list(range(start_year, end_year + 1))]

    top_installations["Total"] = top_installations[years].sum(axis=1)

    return top_installations.sort_values("Total", ascending=False)

```

One thing to note: Don't worry too much about efficiency in your pandas code. If it works and you can understand it, that's enough! We'll learn to use caching later in the session so the app won't run these over and over.

###### Displaying results

Now let's import, use these functions and display their results in our main app file:

```python
# app.py
# ...
from utils import load_data, make_total_by_year, make_top_installations

st.subheader("Total by year")

total_by_year = make_total_by_year(df)
st.table(total_by_year)

# To calculate the total for all years :
st.write(f"Total: {total_by_year['Total by Year'].sum()}")


st.subheader("Top Installations")

top_installations = make_top_installations(df)
st.table(top_installations[:10])

```

#### Display the data nicely

###### Chart

Let's display our emissions over the years in a nice graph:

```python
# app.py
# ...
total_by_year = make_total_by_year(df)
st.line_chart(total_by_year)
# st.bar_chart(total_by_year)
```

That was easy! But it's not always that straightforward. Streamlit provides functions for very simple charts & maps ([see the docs](https://docs.streamlit.io/library/api-reference/charts)), but for more complex situations, you will have to use a plotting or mapping library such as:
- Matplotlib
- Altair
- VegaLite
- Bokeh
- Plotly
- Pydeck
- and many more through third party components

Some of these are complex to master (looking at you, matplotlib), some are easier. When you have a complex visualization to make, I'll recommend trying to find examples with code in the documentation of these libraries or in forums. Sometimes all it takes is to change a few lines here and there. Experiment!


### Metric

Let's better present our grand total for all years, using Streamlit's [metric component](https://docs.streamlit.io/library/api-reference/data/st.metric). We'll pass the arguments for the label, then the number, as seen in the docs.

```python
st.metric("Total (all years, tons)", f"{int(total_all_years):,d}")
```
In the code above, I've converted the number to `int` & formatted it using an f-string, indicating `,` as the thousands separator. Better practice would be to define the data types when loading our csv, so we're sure to be working with `int`s all along.


###### DataFrame

Finally, we'll show our table of top installations in a nicer way too. Instead of using `st.table`, which renders a simple html table, we'll use [`st.dataframe`](https://docs.streamlit.io/library/api-reference/data/st.dataframe), which renders an interactive table.

```python
st.dataframe(
    top_installations[["ID", "InstallationNameOrAircraftOperatorCode", "Total"]],
    use_container_width=True,
)
```

In the code above, I'm passing our data to `st.dataframe` and specifying the columns I want to show on the way. Note that I now choose to show all the installations instead of the top 10 ones: the table now takes a limited height of the screen, and users can scroll to display more data.

I also use `use_container_width=True` to tell Streamlit that this component should take all the width available to it.

#### Inputs

Now, let's focus on the last two questions:
- Can we see the results by country?
- Can we see the results for the last 5 or 10 years?

This is a good opportunity to add some interactivity to our app. Let's give the user the possibility to select a country and a year range.

Here are our steps:
1. Get the user's input
2. Filter our data accordingly
3. Diplay the data (this we did already)

Note that Streamlit executes the code of our app from top to bottom, so these steps need to be in order in our code. When the app detects a change in the user's input, it will re-run its code.

###### Country input

Having a look at the [list of available input widgets](https://docs.streamlit.io/library/api-reference/widgets), [`st.selectbox`](https://docs.streamlit.io/library/api-reference/widgets/st.selectbox) would fit our needs: our user could choose "All", or a specific country from a list to filter the dataset.

To do this, we need a list of countries present in our dataset. The list isn't long, and we could make it manually. But what if our dataset changes and other countries are added?

Let's make it with code instead, so whenever the dataset changes, the app updates accordingly. Create a new function in `utils.py`:

```python
# ...

def get_countries(df):
    """Returns the list of countries in the dataset."""
    countries = df["NationalAdministrator"].unique()
    return sorted(countries)
```

Pandas' `.unique()` method gets the list of all different values in a column, in our case `NationalAdministrator`. Finally, we return the countries sorted alphabetically.

Now that we have our list of countries, we can create our selectbox widget in `app.py`, just after importing the data.

```python
# app.py
# ...
from utils import make_total_by_year, make_top_installations, get_countries
# ...
country_options = ["All"] + get_countries(df)
country = st.selectbox("Country", ["All"] + countries)
# ...
```

Two things to note:
- Let's not forget to add the option to see the data for all countries!
- You register user input in your code by simply assigning the widget to a variable


Now that we have our input widget ready, filtering the data is very easy. We'll add a bit of code before our display of the results:

```python
#app.py
# ...
if country != "All":
    df = df[df["NationalAdministrator"] == country]
```

If anything else than "All" is selected by the user, `df` will be replaced by a conditionally filtered version of itself, where only the installations from the selected countries will be taken in consideration.

Since the rest of the code uses `df` to do calculations & display data, we don't need to change it one bit!

###### Year range input

Using the same principle, we can create an input to select a range of years to consider.

```python
# app.py
years = st.select_slider("Years", list(range(2006, 2022)), value=(2006, 2021))
```

As the [documentation for `st.select_slider`](https://docs.streamlit.io/library/api-reference/widgets/st.select_slider) explains, the `value` keywords set the default state of the widget. I.e: by default, the period 2006-2021 is considered.

This time, instead of filtering the dataset, we will pass the start and end years to our calculation functions `make_total_by_year` and `make_top_installations`:

```python
# app.py
# ...
total_by_year = make_total_by_year(df, start_year=years[0], end_year=years[1])
# ...
top_installations = make_top_installations(df, start_year=years[0], end_year=years[1])
```

#### Better layout

Our app is almost complete! Let's use some of the layout possibilities offered by Streamlit to make things look a bit better still.

- [`st.sidebar`](https://docs.streamlit.io/library/api-reference/layout/st.sidebar) - to put input widgets, title, info..
- [`st.set_page_config(layout="wide")`](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config) - Wide layout
- [`st.expander`](https://docs.streamlit.io/library/api-reference/layout/st.expander) - Show/hide extra info, such as a table.
- [`st.columns`](https://docs.streamlit.io/library/api-reference/layout/st.columns) - Show elements side by side


#### Optimization

Now that our app is ready, let's think about how we can optimize it before deploying it online. Streamlit Share servers have 1GB of RAM!

One way we can easioptimize our app is by leveraging Streamlit's caching capabilities. Streamlit runs our code from top to bottom, and re-runs it whenever an input has changed. Caching allows your Streamlit app to "remember" the results of some calculation given certain input, without having to calculate it again.

The way it works is that we use a function decorator over functions we would like to cache.

For example, all three 3 functions we have in `utils.py` could benefit from caching:

```python
# ...
@st.cache_data
def make_total_by_year(df, start_year=2006, end_year=2022):
#...

@st.cache_data
def make_top_installations(df, start_year=2006, end_year=2022):
# ...

@st.cache_data
def get_countries(df):
# ...
```

Easy! But there are still other parts of our application that we can refactor into functions so we can cache them.

For example, we could load data like this:

```python
# app.py
from utils import load_data #...
# ...
df = load_data()
```

```python
# utils.py
DATA_FILEPATH = "ArcelorMittal_CO2_Emissions.csv"

@st.cache_data
def load_data(data_filepath=DATA_FILEPATH):
    df = pd.read_csv(data_filepath)
    return df
```
Note that we specify the data filepath as a function parameter instead of using it directly: it is through parameter that Streamlit keeps track of whether the result in already in the cache.

## Deployment on Streamlit Share

This may not suit all uses cases, as Streamlit Share machines are limited to 1GB of RAM. But for our simple app and 95 rows of data, it will work just fine.

Think also about security, your threat model and the data sensitivity as well, as you would before using any "cloud" service.

### Github repository

The first thing we need to do is to upload the code of our app to GitHub.

In GitHub's web interface, create a new repository (private or public, doesn't matter). Let's call it "co2app".

Use your code editor functionalities to create a repository, stage, commit and push changes to GitHub, or do it from the command-line:

```bash
git init -b main # create
git add . # stage
git commit -m "First commit" # commit
git remote add origin <REMOTE_URL> # adding remote
git push origin main # pushing to remote
```

If you are unconfortable or unfamiliar with git, there's also a simple "upload" button on your GitHub repo's file.

#### Streamlit Share

Now that our code is on GitHub, we can visit https://share.streamlit.io.

We'll login using GitHub, so the connection between our Streamlit Share and GitHub accounts is done straigh away.

To deploy an app, click "New app" from the upper right corner, then choose your repository, its main branch, and the file path of our streamlit app (`app.py`).

Make a tour of the other available options, and click "Deploy" when you are satisfied.

You will now see your app launch, you can show logs by clicking "Manage" in the bottom-right corner of the page.

Wait a bit, and hopefully your app is now live! Everytime the code in your GitHub repository changes, the app will update automatically.


## Demo of the full featured app

The original app I based this presentation on is a bit more complex, but not by much.

You can have a look at it here:

https://amets-p46xvx.streamlit.app/ | password: DataHarvest2023

Third party components:
- [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) for the navigation menu in the sidebar. Not the standard way of making [multi-page apps](https://docs.streamlit.io/library/get-started/multipage-apps), but it works with [authentication without SSO](https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso).
- [streamlit-aggrid](https://github.com/PablocFonseca/streamlit-aggrid) for the interactive table where you can select a row.
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) for the maps.


## Q & A
