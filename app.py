import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a connection to the PostgreSQL database

engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5432/{os.getenv('DB_NAME')}")
print("Database connection established successfully.")

# Page configuration
st.set_page_config(page_title="Movie Recommendation System", layout="wide", page_icon="🎬",)


# Function to get the list of movie titles for the dropdown
@st.cache_data
def get_movie_list():
    query = "SELECT title FROM movies ORDER BY title"
    return pd.read_sql(query, engine)['title'].tolist()

# Function to get hybrid recommendations based on shared genres and ratings
@st.cache_data
def get_hybrid_recommendations(movie_title, min_votes=500, limit=5):
    query = f"""
    with target_genres as (
        select mg.genres
        from movies_genres mg
        join movies m on m."movieId" = mg."movieId"
        where m.title = %(movie_title)s
    ),
    similar_movies as (
        select 
            m."movieId",
            m.title,
            count(mg.genres) as shared_genres_count
        from movies m
        join movies_genres mg 
            on m."movieId" = mg."movieId"
        where mg.genres in (select genres from target_genres)
          and m.title <> %(movie_title)s
        group by m."movieId", m.title
        having count(mg.genres) >= 3
    )
    select 
        sm.title,
        sm.shared_genres_count,
        mrs.avg_rating,
        mrs.vote_count
    from similar_movies sm
    join movie_rating_stats mrs  
        on sm."movieId" = mrs."movieId"
    where mrs.vote_count >= %(min_votes)s
    order by sm.shared_genres_count desc, mrs.avg_rating desc
    limit %(limit)s;
    """
    return pd.read_sql(query,engine, params={'movie_title': movie_title, 'min_votes': min_votes, 'limit': limit})

@st.cache_data
def get_genres_distribution():
    query = """
    select genres, count(*) as movie_count
    from movies_genres
    group by genres
    order by movie_count desc
    limit 10;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_yearly_movie_trends():
    query = """
    select year, count(*) as movie_count
    from movies
    where year is not null 
    group by year
    order by year;
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_top_rated_movies(limit=10):
    query = f"""
    select m.title as "Movie Title", mrs.avg_rating as "Average Rating", mrs.vote_count as "Number of Votes"
    from movies m
    join movie_rating_stats mrs on m."movieId" = mrs."movieId"
    where mrs.vote_count >= 1000
    order by mrs.avg_rating desc
    limit {limit};
    """
    return pd.read_sql(query, engine)

# Streamlit user interface
st.title("🎬 Movie Recommendation System & Reccommendation Portal")
#st.markdown("Choose a movie to get hybrid recommendations that blend shared genres with strong ratings.")

# Sidebar for movie selection - get fields for analysis
with st.sidebar:
    st.header("⚙️ Recommendation Settings")
    min_votes = st.slider("Minimum Number of Votes", min_value=100, max_value=10000, value=500, step=100)
    limit = st.number_input("Number of Recommendations", min_value=1, max_value=20, value=5)

# Home page content
# Tabs

tab1, tab2, tab3 = st.tabs(["🎥 Get Recommendations", "📊 Movie Data Analysis", "🏆 Top Rated Movies"])
with tab1:
    st.subheader("Get Movie Recommendations")
    movie_list = get_movie_list()
    selected_movie = st.selectbox("Select a Movie", options=movie_list, label_visibility="collapsed")

    if st.button("Get Recommendations"):
        with st.spinner("Fetching recommendations..."):
            recommendations = get_hybrid_recommendations(selected_movie, min_votes, limit)
            if not recommendations.empty:
                st.subheader(f"Recommendations for '{selected_movie}'")
                st.dataframe(recommendations, use_container_width=True)  # Display the recommendations in a table format

                # Display the top recommendation with a metric
                col1, col2 = st.columns(2)
                top_movie = recommendations.iloc[0]['title']
                top_rating = recommendations.iloc[0]['avg_rating']
                col1.metric("Top Recommendation", top_movie)
                col2.metric("Average Rating", f"⭐ {top_rating:.1f}")
                
            else:
                st.warning("No recommendations found. Try adjusting the settings.")

with tab2:
    st.header("Movie Data Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Genres Distribution")
        genres_distribution = get_genres_distribution()
        st.bar_chart(genres_distribution.set_index('genres')['movie_count'], color="#ff4b4b")
        st.caption("Distribution of top genres in the dataset.(Top 10)")
    with col2:
        st.subheader("Yearly Movie Trends")
        yearly_trends = get_yearly_movie_trends()
        st.line_chart(yearly_trends.set_index('year')['movie_count'], color="#4b7bec")
        st.caption("Number of movies released each year.")

with tab3:
    st.subheader("Top 10 Rated Movies")
    top_movies = get_top_rated_movies(limit=10)
    top_movies["Average Rating"] = pd.to_numeric(top_movies["Average Rating"], errors="coerce").round(1)
    top_movies.index += 1  # Start index from 1 for better readability
    st.table(top_movies.style.format({"Average Rating": "{:.1f}"}))

    m1,m2,m3 = st.columns([2,1,1])
    title = top_movies.iloc[0]['Movie Title']
    rating = top_movies.iloc[0]['Average Rating']
    votes = top_movies.iloc[0]['Number of Votes']
    with m1:
        st.metric("🏆 Top Rated Movie", title)
       
    with m2:
        st.metric("⭐ Average Rating", f"{rating:.1f}")
    with m3:
        st.metric("👥 Total Votes", f"{votes:,}")


# extra info
st.divider()
st.info("This application uses a hybrid recommendation approach that combines shared genres with strong ratings to provide personalized movie suggestions. Adjust the settings in the sidebar to find the best recommendations for you!")

# project info
st.info("**Project Note:** This dashboard provides optimized summaries (Materialized Views) of over 20 million 'rating' data points running on PostgreSQL, enabling analysis in seconds.")