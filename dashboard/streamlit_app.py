"""
Movie Analytics Dashboard

An interactive dashboard for exploring movie industry data, trends, and insights.
Built with Streamlit for professional data visualization and analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #ff6b6b;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all datasets with caching for performance"""
    try:
        movies = pd.read_csv('../data/processed/movies_processed.csv')
        sales = pd.read_csv('../data/processed/sales_processed.csv')
        genre_stats = pd.read_csv('../data/processed/genre_stats.csv')
        studio_stats = pd.read_csv('../data/processed/studio_stats.csv')
        monthly_sales = pd.read_csv('../data/processed/monthly_sales.csv')
        
        # Convert date columns
        movies['release_date'] = pd.to_datetime(movies['release_date'])
        sales['date'] = pd.to_datetime(sales['date'])
        
        return movies, sales, genre_stats, studio_stats, monthly_sales
    except FileNotFoundError:
        st.error("Data files not found. Please run the data generation scripts first.")
        return None, None, None, None, None

def main():
    """Main dashboard application"""
    
    # Load data
    movies, sales, genre_stats, studio_stats, monthly_sales = load_data()
    
    if movies is None:
        st.stop()
    
    # Header
    st.title("🎬 Movie Industry Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(movies['release_date'].min(), movies['release_date'].max()),
        min_value=movies['release_date'].min(),
        max_value=movies['release_date'].max()
    )
    
    # Genre filter
    genres = st.sidebar.multiselect(
        "Select Genres",
        options=movies['genre'].unique(),
        default=movies['genre'].unique()
    )
    
    # Budget range filter
    budget_range = st.sidebar.slider(
        "Budget Range (Millions)",
        min_value=0,
        max_value=int(movies['budget'].max() / 1_000_000),
        value=(0, int(movies['budget'].max() / 1_000_000)),
        step=10
    )
    
    # Apply filters
    filtered_movies = movies[
        (movies['release_date'] >= pd.Timestamp(date_range[0])) &
        (movies['release_date'] <= pd.Timestamp(date_range[1])) &
        (movies['genre'].isin(genres)) &
        (movies['budget'] >= budget_range[0] * 1_000_000) &
        (movies['budget'] <= budget_range[1] * 1_000_000)
    ]
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Movies",
            value=f"{len(filtered_movies):,}"
        )
    
    with col2:
        total_gross = filtered_movies['total_gross'].sum()
        st.metric(
            label="Total Box Office",
            value=f"${total_gross/1_000_000_000:.1f}B"
        )
    
    with col3:
        avg_rating = filtered_movies['imdb_rating'].mean()
        st.metric(
            label="Avg IMDb Rating",
            value=f"{avg_rating:.1f}/10"
        )
    
    with col4:
        profitable_pct = (len(filtered_movies[filtered_movies['profit'] > 0]) / len(filtered_movies)) * 100
        st.metric(
            label="Profitable Movies",
            value=f"{profitable_pct:.1f}%"
        )
    
    with col5:
        avg_roi = filtered_movies['roi'].mean()
        st.metric(
            label="Average ROI",
            value=f"{avg_roi:.1f}%"
        )
    
    st.markdown("---")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🎭 Genre Analysis", "🏢 Studio Performance", "📈 Trends", "🎫 Sales Data"])
    
    with tab1:
        show_overview_tab(filtered_movies)
    
    with tab2:
        show_genre_analysis(filtered_movies, genre_stats)
    
    with tab3:
        show_studio_analysis(filtered_movies, studio_stats)
    
    with tab4:
        show_trends_analysis(filtered_movies, sales)
    
    with tab5:
        show_sales_analysis(sales)

def show_overview_tab(movies):
    """Overview tab with key visualizations"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget vs Gross scatter plot
        fig = px.scatter(
            movies,
            x='budget',
            y='total_gross',
            color='genre',
            size='imdb_rating',
            hover_data=['title', 'release_year'],
            title='Budget vs Total Gross Revenue'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ROI distribution
        fig = px.histogram(
            movies,
            x='roi',
            nbins=30,
            title='Return on Investment Distribution'
        )
        fig.add_vline(x=movies['roi'].median(), line_dash="dash", 
                     annotation_text=f"Median: {movies['roi'].median():.1f}%")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top performers table
    st.subheader("🏆 Top Performing Movies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 10 by Total Gross**")
        top_gross = movies.nlargest(10, 'total_gross')[['title', 'genre', 'total_gross', 'imdb_rating']]
        top_gross['total_gross'] = top_gross['total_gross'].apply(lambda x: f"${x/1_000_000:.1f}M")
        st.dataframe(top_gross, hide_index=True)
    
    with col2:
        st.write("**Top 10 by ROI**")
        top_roi = movies.nlargest(10, 'roi')[['title', 'genre', 'roi', 'budget']]
        top_roi['roi'] = top_roi['roi'].apply(lambda x: f"{x:.1f}%")
        top_roi['budget'] = top_roi['budget'].apply(lambda x: f"${x/1_000_000:.1f}M")
        st.dataframe(top_roi, hide_index=True)

def show_genre_analysis(movies, genre_stats):
    """Genre analysis tab"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Genre distribution
        genre_counts = movies['genre'].value_counts()
        fig = px.pie(
            values=genre_counts.values,
            names=genre_counts.index,
            title='Movie Distribution by Genre'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average revenue by genre
        genre_performance = movies.groupby('genre').agg({
            'total_gross': 'mean',
            'imdb_rating': 'mean'
        }).reset_index()
        
        fig = px.bar(
            genre_performance,
            x='genre',
            y='total_gross',
            title='Average Revenue by Genre'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed genre statistics
    st.subheader("📊 Detailed Genre Statistics")
    st.dataframe(genre_stats, hide_index=True)

def show_studio_analysis(movies, studio_stats):
    """Studio analysis tab"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top studios by total revenue
        studio_revenue = movies.groupby('studio')['total_gross'].sum().nlargest(15)
        fig = px.bar(
            x=studio_revenue.values,
            y=studio_revenue.index,
            orientation='h',
            title='Top 15 Studios by Total Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Studio performance scatter
        studio_performance = movies.groupby('studio').agg({
            'movie_id': 'count',
            'total_gross': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            studio_performance,
            x='movie_id',
            y='total_gross',
            size='total_gross',
            hover_data=['studio'],
            title='Studio Performance: Movies Count vs Average Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Studio statistics table
    st.subheader("🏢 Studio Performance Statistics")
    st.dataframe(studio_stats, hide_index=True)

def show_trends_analysis(movies, sales):
    """Trends analysis tab"""
    
    # Extract year from release date
    movies['release_year'] = movies['release_date'].dt.year
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Movies released per year
        release_trends = movies.groupby('release_year').agg({
            'movie_id': 'count',
            'total_gross': 'mean'
        }).reset_index()
        
        fig = px.line(
            release_trends,
            x='release_year',
            y='movie_id',
            title='Number of Movies Released per Year',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average gross per year
        fig = px.line(
            release_trends,
            x='release_year',
            y='total_gross',
            title='Average Gross Revenue per Year',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Budget vs ratings over time
    fig = px.scatter(
        movies,
        x='release_year',
        y='imdb_rating',
        size='budget',
        color='genre',
        title='Movie Ratings vs Release Year (Size = Budget)'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_sales_analysis(sales):
    """Sales analysis tab"""
    
    # Daily sales trends
    daily_sales = sales.groupby('date').agg({
        'tickets_sold': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            daily_sales,
            x='date',
            y='tickets_sold',
            title='Daily Ticket Sales Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            daily_sales,
            x='date',
            y='revenue',
            title='Daily Revenue Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekend vs weekday analysis
    weekend_analysis = sales.groupby('is_weekend').agg({
        'tickets_sold': 'mean',
        'revenue': 'mean'
    }).reset_index()
    weekend_analysis['day_type'] = weekend_analysis['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            weekend_analysis,
            x='day_type',
            y='tickets_sold',
            title='Average Tickets Sold: Weekend vs Weekday'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            weekend_analysis,
            x='day_type',
            y='revenue',
            title='Average Revenue: Weekend vs Weekday'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top movies by sales
    st.subheader("🎬 Top Movies by Ticket Sales")
    top_sales = sales.groupby('movie_title')['tickets_sold'].sum().nlargest(15).reset_index()
    
    fig = px.bar(
        top_sales,
        x='tickets_sold',
        y='movie_title',
        orientation='h',
        title='Top 15 Movies by Total Ticket Sales'
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()