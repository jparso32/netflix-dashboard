import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pycountry

df = pd.read_csv("data/netflix_titles.csv")

#print(df.shape)
#print(df.dtypes)
#print(df.isnull().sum())
#print(df.head())

# Fill missing values for these 3 with unknown, some are almost 10-30% missing values so it'll be better to fill them with unknown rather than dropping them
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

df = df.dropna(subset=["date_added", "rating", "duration"])

df['date_added'] = pd.to_datetime(df['date_added'].str.strip())

# We do this to extract the numeric part of the duration and also to categorize the duration type (Season(s) or min)
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(int)
df['duration_type'] = df['duration'].apply(lambda x: "Season(s)" if "Season" in x else 'min')

#print(df.isnull().sum())
#print(df.dtypes)

# ---------------------------------------------------------
# CHART 1: Titles by Rating (bar chart)
# Simple categorical count — no reshaping needed since each
# row only has one rating value
# ---------------------------------------------------------

rating_counts = df['rating'].value_counts().reset_index()
rating_counts.columns = ['rating', 'count']

fig_rating = px.bar(rating_counts, x='rating', y='count', title='Titles by Rating')
st.plotly_chart(fig_rating)

fig_rating.write_image('imgs/rating_counts.png')

# ---------------------------------------------------------
# CHART 2: Top Genres (bar chart)
# listed_in holds multiple genres per row,
# so we split + explode into one genre per row before counting 
# otherwise combo-strings would be counted as their own separate categories
# ---------------------------------------------------------

genre_df = df.copy()
genre_df['genres'] = genre_df['listed_in'].str.split(', ')
genre_df = genre_df.explode('genres')

genre_counts = genre_df['genres'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_genre = px.bar(genre_counts, x='genre', y='count', title='Titles by Genre')
st.plotly_chart(fig_genre)
fig_genre.write_image('imgs/genre_counts.png')

# ---------------------------------------------------------
# CHART 3: Movie Runtime Distribution (histogram)
# Only movies have a runtime in minutes, TV show "durations" are
# season counts, a completely different unit, so we filter to movies only
# ---------------------------------------------------------

movies_df = df[df['duration_type'] == 'min']
fig_duration = px.histogram(movies_df, x='duration_num', nbins=20, title='Movie Runtime Distribution')
st.plotly_chart(fig_duration)
fig_duration.write_image('imgs/duration_distribution.png')

# ---------------------------------------------------------
# CHART 4: Titles Added to Netflix Per Year (line chart)
# Trend-over-time question, so it needs chronological order 
# value_counts() sorts by count by default, so sort_index() re-sorts by year
# ---------------------------------------------------------

df['year_added'] = df['date_added'].dt.year
year_counts = df['year_added'].value_counts().sort_index().reset_index()
year_counts.columns = ['year_added', 'count']

fig_trend = px.line(year_counts, x='year_added', y='count', title='Titles Added to Netflix Per Year')
st.plotly_chart(fig_trend)
fig_trend.write_image('imgs/titles_added_per_year.png')

# ---------------------------------------------------------
# CHART 5: Titles by Country (choropleth map)
# country has multi-country strings too, so split + explode again.
# Choropleths need standardized ISO codes to draw shapes correctly,
# so we convert country names to codes and drop the small number that fail to match
# ---------------------------------------------------------
country_df = df.copy()
country_df['countries'] = country_df['country'].str.split(', ')
country_df = country_df.explode('countries')

country_counts = country_df['countries'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

def get_iso_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None

country_counts['iso_code'] = country_counts['country'].apply(get_iso_code)
country_counts = country_counts.dropna(subset=['iso_code'])

fig_country = px.choropleth(
    country_counts,
    locations='iso_code',
    color='count',
    hover_name='country',
    color_continuous_scale='Reds',
    title='Netflix Titles by Country'
)
st.plotly_chart(fig_country)
fig_country.write_image('imgs/titles_by_country.png')

# ---------------------------------------------------------
# CHART 6: Movies vs. TV Shows Added Per Year (multi-line chart)
# groupby() groups by TWO columns at once (year + type), unlike
# value_counts() which only handles one column
# ---------------------------------------------------------

type_year_counts = df.groupby(['year_added', 'type']).size().reset_index()
type_year_counts.columns = ['year_added', 'type', 'count']

fig_type_trend = px.line(
    type_year_counts,
    x='year_added',
    y='count',
    color='type',
    title='Movies vs. TV Shows Added Per Year'
)
st.plotly_chart(fig_type_trend)
fig_type_trend.write_image('imgs/movies_vs_tv_shows_per_year.png')

# ---------------------------------------------------------
# INTERACTIVE FILTER: Top Genres by Country
# ---------------------------------------------------------
st.header("Top Genres by Country")

genre_country_df = genre_df.copy()
genre_country_df['country'] = genre_country_df['country'].str.split(', ')
genre_country_df = genre_country_df.explode('country')

selected_country = st.selectbox("Choose a country", sorted(genre_country_df["country"].unique()))

filtered_genre_df = genre_country_df[genre_country_df['country'] == selected_country]
genre_counts_filtered = filtered_genre_df['genres'].value_counts().reset_index()
genre_counts_filtered.columns = ['genre', 'count']

fig_genre_filtered = px.bar(genre_counts_filtered, x='genre', y='count', title=f'Top Genres in {selected_country}')
st.plotly_chart(fig_genre_filtered)