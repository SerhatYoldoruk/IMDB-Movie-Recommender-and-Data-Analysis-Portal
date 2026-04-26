# 🎬 IMDB Movie Recommender & Data Analysis Portal

An end-to-end Data Science project featuring a **Hybrid Recommendation Engine** and an interactive **Exploratory Data Analysis (EDA)** dashboard. This application leverages real-world IMDB data to provide personalized movie suggestions and deep industry insights.

## 🚀 Core Features
* **Hybrid Recommender System:** Seamlessly combines *Content-Based Filtering* (using metadata like genres and keywords) and *Popularity-Based* metrics.
* **Interactive Analytics Dashboard:** A dynamic Streamlit interface offering visual insights into movie trends, ratings, and genre distributions.
* **Robust Database Management:** Powered by **PostgreSQL**, utilizing optimized schemas and Materialized Views for high-speed query performance.
* **Advanced Data Processing:** Extensive data cleaning and feature engineering on a dataset of 40,000+ movies using Pandas and NumPy.

## 🛠️ Technology Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy, Seaborn, Matplotlib
* **Web Framework:** Streamlit
* **Database:** PostgreSQL (SQLAlchemy & Psycopg2), Dbeaver(for psql queries)


## 📋 Installation & Local Setup
To run this project on your local machine, follow these steps:

1.  **Clone the Repository:**
    
    git clone [https://github.com/SerhatYoldoruk/IMDB-Movie-Recommender-and-Data-Analysis-Portal.git](https://github.com/SerhatYoldoruk/IMDB-Movie-Recommender-and-Data-Analysis-Portal.git)
    
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables:**
    Create a `.env` file in the root directory and add your PostgreSQL credentials:
    ```text
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_NAME=your_database_name
    ```
4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 📊 Visual Insights
The portal includes detailed visualizations such as:
* Distribution of movie ratings across different decades.
* Trend analysis of movie releases from the 1900s to the present.
* Correlation between budget, revenue, and weighted scores.

* ## 📊 Dataset Information
The project utilizes two main datasets sourced from **Kaggle (IMDB Movies Dataset)** (https://www.kaggle.com/datasets/ayberkural/movielens-movie-csv-and-rating-csv?resource=download) thanks to Ayberk Ural:
* `movie.csv`: Contains metadata for 40,000+ movies (titles, genres, years, etc.).
* `rating.csv`: Contains user-provided ratings that power the recommendation engine.
