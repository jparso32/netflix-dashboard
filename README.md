# Netflix Titles Dashboard

An interactive Streamlit dashboard exploring Netflix's title catalog — ratings,
genres, runtime, content growth over time, and country-based genre filtering.

# Link to Dashboard
https://netflix-dashboard-vgjvr7ayztrvbmxwsypmyc.streamlit.app/ 

# Image Examples
<img width="540" height="256" alt="image" src="https://github.com/user-attachments/assets/2ffb2cf9-c868-4ea5-a3a4-30dc1f8f8d56" />
C:\Users\jayde\netflix-dashboard\imgs\movies_vs_tv_shows_per_year.png 


## What it does

This dashboard answers a handful of questions about Netflix's content library
using the public [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows):

- How is content distributed across maturity ratings?
- What are the most common genres, and how does that change by country?
- How long are movies, typically?
- How has the volume of titles added to Netflix changed year over year, and
  how does that growth compare between movies and TV shows?
- Which countries produce the most Netflix content?

## Features

- 6 interactive visualizations built with Plotly (bar charts, a histogram, line
  charts, and a choropleth map)
- A country filter that dynamically updates the "Top Genres" chart based on the
  selection
- All charts render inline and respond live to user input — no page reloads

## Tech Stack

- **Python** — data processing
- **Pandas** — cleaning and reshaping the dataset
- **Plotly Express** — chart generation
- **Streamlit** — interactive web app framework
- **pycountry** — standardizing country names into ISO codes for the map

## Data Cleaning Notes

A few real-world data issues had to be handled deliberately rather than with
generic cleaning:

- `director`, `cast`, and `country` were missing in roughly 10–30% of rows —
  too much to drop without losing a meaningful chunk of the dataset, so these
  were filled with `"Unknown"` instead.
- `date_added`, `rating`, and `duration` were only missing a handful of rows,
  so those rows were safely dropped.
- `duration` mixed two incompatible units in one column — `"90 min"` for
  movies and `"3 Seasons"` for TV shows. These were split into a numeric
  value and a separate unit column so they're never accidentally averaged
  or charted together.
- Both `listed_in` (genre) and `country` can hold multiple comma-separated
  values per row (e.g. `"Dramas, International Movies"`). These were split
  and exploded into one value per row before counting, so a title with
  multiple genres/countries contributes to each of them individually rather
  than being counted as one unique combined category.
- For the choropleth map, country names were converted to ISO alpha-3 codes
  via `pycountry`; the small number of names that failed to match were
  dropped rather than guessed at.

## Running it locally

```bash
git clone https://github.com/YOUR_USERNAME/netflix-titles-dashboard.git
cd netflix-titles-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) (Kaggle)
