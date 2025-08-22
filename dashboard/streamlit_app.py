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
        movies = pd.read_csv('data/processed/movies_processed.csv')
        sales = pd.read_csv('data/processed/sales_processed.csv')
        genre_stats = pd.read_csv('data/processed/genre_stats.csv')
        studio_stats = pd.read_csv('data/processed/studio_stats.csv')
        monthly_sales = pd.read_csv('data/processed/monthly_sales.csv')
        
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
    filtered_movies = movies[\n",
    "        (movies['release_date'] >= pd.Timestamp(date_range[0])) &\n",
    "        (movies['release_date'] <= pd.Timestamp(date_range[1])) &\n",
    "        (movies['genre'].isin(genres)) &\n",
    "        (movies['budget'] >= budget_range[0] * 1_000_000) &\n",
    "        (movies['budget'] <= budget_range[1] * 1_000_000)\n",
    "    ]\n",
    "    \n",
    "    # Key Metrics Row\n",
    "    col1, col2, col3, col4, col5 = st.columns(5)\n",
    "    \n",
    "    with col1:\n",
    "        st.metric(\n",
    "            label=\"Total Movies\",\n",
    "            value=f\"{len(filtered_movies):,}\"\n",
    "        )\n",
    "    \n",
    "    with col2:\n",
    "        total_gross = filtered_movies['total_gross'].sum()\n",
    "        st.metric(\n",
    "            label=\"Total Box Office\",\n",
    "            value=f\"${total_gross/1_000_000_000:.1f}B\"\n",
    "        )\n",
    "    \n",
    "    with col3:\n",
    "        avg_rating = filtered_movies['imdb_rating'].mean()\n",
    "        st.metric(\n",
    "            label=\"Avg IMDb Rating\",\n",
    "            value=f\"{avg_rating:.1f}/10\"\n",
    "        )\n",
    "    \n",
    "    with col4:\n",
    "        profitable_pct = (len(filtered_movies[filtered_movies['profit'] > 0]) / len(filtered_movies)) * 100\n",
    "        st.metric(\n",
    "            label=\"Profitable Movies\",\n",
    "            value=f\"{profitable_pct:.1f}%\"\n",
    "        )\n",
    "    \n",
    "    with col5:\n",
    "        avg_roi = filtered_movies['roi'].mean()\n",
    "        st.metric(\n",
    "            label=\"Average ROI\",\n",
    "            value=f\"{avg_roi:.1f}%\"\n",
    "        )\n",
    "    \n",
    "    st.markdown(\"---\")\n",
    "    \n",
    "    # Create tabs for different analyses\n",
    "    tab1, tab2, tab3, tab4, tab5 = st.tabs([\"📊 Overview\", \"🎭 Genre Analysis\", \"🏢 Studio Performance\", \"📈 Trends\", \"🎫 Sales Data\"])\n",
    "    \n",
    "    with tab1:\n",
    "        show_overview_tab(filtered_movies)\n",
    "    \n",
    "    with tab2:\n",
    "        show_genre_analysis(filtered_movies, genre_stats)\n",
    "    \n",
    "    with tab3:\n",
    "        show_studio_analysis(filtered_movies, studio_stats)\n",
    "    \n",
    "    with tab4:\n",
    "        show_trends_analysis(filtered_movies, sales)\n",
    "    \n",
    "    with tab5:\n",
    "        show_sales_analysis(sales)\n",
    "\ndef show_overview_tab(movies):\n",
    "    \"\"\"Overview tab with key visualizations\"\"\"\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        # Budget vs Gross scatter plot\n",
    "        fig = px.scatter(\n",
    "            movies,\n",
    "            x='budget',\n",
    "            y='total_gross',\n",
    "            color='genre',\n",
    "            size='imdb_rating',\n",
    "            hover_data=['title', 'release_year'],\n",
    "            title='Budget vs Total Gross Revenue'\n",
    "        )\n",
    "        fig.update_layout(height=500)\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        # ROI distribution\n",
    "        fig = px.histogram(\n",
    "            movies,\n",
    "            x='roi',\n",
    "            nbins=30,\n",
    "            title='Return on Investment Distribution'\n",
    "        )\n",
    "        fig.add_vline(x=movies['roi'].median(), line_dash=\"dash\", \n",
    "                     annotation_text=f\"Median: {movies['roi'].median():.1f}%\")\n",
    "        fig.update_layout(height=500)\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Top performers table\n",
    "    st.subheader(\"🏆 Top Performing Movies\")\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        st.write(\"**Top 10 by Total Gross**\")\n",
    "        top_gross = movies.nlargest(10, 'total_gross')[['title', 'genre', 'total_gross', 'imdb_rating']]\n",
    "        top_gross['total_gross'] = top_gross['total_gross'].apply(lambda x: f\"${x/1_000_000:.1f}M\")\n",
    "        st.dataframe(top_gross, hide_index=True)\n",
    "    \n",
    "    with col2:\n",
    "        st.write(\"**Top 10 by ROI**\")\n",
    "        top_roi = movies.nlargest(10, 'roi')[['title', 'genre', 'roi', 'imdb_rating']]\n",
    "        top_roi['roi'] = top_roi['roi'].apply(lambda x: f\"{x:.1f}%\")\n",
    "        st.dataframe(top_roi, hide_index=True)\n",
    "\ndef show_genre_analysis(movies, genre_stats):\n",
    "    \"\"\"Genre analysis tab\"\"\"\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        # Genre distribution pie chart\n",
    "        genre_counts = movies['genre'].value_counts()\n",
    "        fig = px.pie(\n",
    "            values=genre_counts.values,\n",
    "            names=genre_counts.index,\n",
    "            title='Movie Distribution by Genre'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        # Average gross by genre\n",
    "        genre_gross = movies.groupby('genre')['total_gross'].mean().sort_values(ascending=True)\n",
    "        fig = px.bar(\n",
    "            x=genre_gross.values,\n",
    "            y=genre_gross.index,\n",
    "            orientation='h',\n",
    "            title='Average Gross Revenue by Genre'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Genre performance metrics\n",
    "    st.subheader(\"📊 Genre Performance Metrics\")\n",
    "    \n",
    "    # Create genre performance summary\n",
    "    genre_summary = movies.groupby('genre').agg({\n",
    "        'movie_id': 'count',\n",
    "        'total_gross': ['mean', 'sum'],\n",
    "        'budget': 'mean',\n",
    "        'imdb_rating': 'mean',\n",
    "        'roi': 'mean',\n",
    "        'profit': 'mean'\n",
    "    }).round(2)\n",
    "    \n",
    "    genre_summary.columns = ['Count', 'Avg Gross', 'Total Gross', 'Avg Budget', 'Avg Rating', 'Avg ROI', 'Avg Profit']\n",
    "    genre_summary = genre_summary.reset_index()\n",
    "    \n",
    "    # Format currency columns\n",
    "    for col in ['Avg Gross', 'Total Gross', 'Avg Budget', 'Avg Profit']:\n",
    "        genre_summary[col] = genre_summary[col].apply(lambda x: f\"${x/1_000_000:.1f}M\")\n",
    "    \n",
    "    genre_summary['Avg ROI'] = genre_summary['Avg ROI'].apply(lambda x: f\"{x:.1f}%\")\n",
    "    genre_summary['Avg Rating'] = genre_summary['Avg Rating'].apply(lambda x: f\"{x:.1f}/10\")\n",
    "    \n",
    "    st.dataframe(genre_summary, hide_index=True)\n",
    "\ndef show_studio_analysis(movies, studio_stats):\n",
    "    \"\"\"Studio analysis tab\"\"\"\n",
    "    \n",
    "    # Top studios by total gross\n",
    "    top_studios = movies.groupby('studio')['total_gross'].sum().nlargest(10)\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        fig = px.bar(\n",
    "            x=top_studios.index,\n",
    "            y=top_studios.values,\n",
    "            title='Top 10 Studios by Total Gross Revenue'\n",
    "        )\n",
    "        fig.update_xaxes(tickangle=45)\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        # Studio performance scatter\n",
    "        studio_perf = movies.groupby('studio').agg({\n",
    "            'movie_id': 'count',\n",
    "            'total_gross': 'mean',\n",
    "            'imdb_rating': 'mean'\n",
    "        }).reset_index()\n",
    "        \n",
    "        fig = px.scatter(\n",
    "            studio_perf,\n",
    "            x='movie_id',\n",
    "            y='total_gross',\n",
    "            color='imdb_rating',\n",
    "            size='total_gross',\n",
    "            hover_data=['studio'],\n",
    "            title='Studio Performance: Movies vs Average Gross',\n",
    "            labels={'movie_id': 'Number of Movies', 'total_gross': 'Average Gross'}\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Studio performance table\n",
    "    st.subheader(\"🏢 Studio Performance Summary\")\n",
    "    \n",
    "    studio_summary = movies.groupby('studio').agg({\n",
    "        'movie_id': 'count',\n",
    "        'total_gross': ['mean', 'sum'],\n",
    "        'budget': 'mean',\n",
    "        'imdb_rating': 'mean',\n",
    "        'roi': 'mean'\n",
    "    }).round(2)\n",
    "    \n",
    "    studio_summary.columns = ['Movies', 'Avg Gross', 'Total Gross', 'Avg Budget', 'Avg Rating', 'Avg ROI']\n",
    "    studio_summary = studio_summary.reset_index().sort_values('Total Gross', ascending=False)\n",
    "    \n",
    "    # Format columns\n",
    "    for col in ['Avg Gross', 'Total Gross', 'Avg Budget']:\n",
    "        studio_summary[col] = studio_summary[col].apply(lambda x: f\"${x/1_000_000:.1f}M\")\n",
    "    \n",
    "    studio_summary['Avg ROI'] = studio_summary['Avg ROI'].apply(lambda x: f\"{x:.1f}%\")\n",
    "    studio_summary['Avg Rating'] = studio_summary['Avg Rating'].apply(lambda x: f\"{x:.1f}/10\")\n",
    "    \n",
    "    st.dataframe(studio_summary, hide_index=True)\n",
    "\ndef show_trends_analysis(movies, sales):\n",
    "    \"\"\"Trends analysis tab\"\"\"\n",
    "    \n",
    "    # Release trends over time\n",
    "    release_trends = movies.groupby('release_year').agg({\n",
    "        'movie_id': 'count',\n",
    "        'total_gross': 'mean',\n",
    "        'budget': 'mean',\n",
    "        'imdb_rating': 'mean'\n",
    "    }).reset_index()\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        # Movies per year\n",
    "        fig = px.line(\n",
    "            release_trends,\n",
    "            x='release_year',\n",
    "            y='movie_id',\n",
    "            title='Number of Movies Released per Year',\n",
    "            markers=True\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        # Average gross per year\n",
    "        fig = px.line(\n",
    "            release_trends,\n",
    "            x='release_year',\n",
    "            y='total_gross',\n",
    "            title='Average Gross Revenue per Year',\n",
    "            markers=True\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Budget vs ratings over time\n",
    "    fig = px.scatter(\n",
    "        movies,\n",
    "        x='release_year',\n",
    "        y='imdb_rating',\n",
    "        size='budget',\n",
    "        color='genre',\n",
    "        title='Movie Ratings vs Release Year (Size = Budget)'\n",
    "    )\n",
    "    st.plotly_chart(fig, use_container_width=True)\n",
    "\ndef show_sales_analysis(sales):\n",
    "    \"\"\"Sales analysis tab\"\"\"\n",
    "    \n",
    "    # Daily sales trends\n",
    "    daily_sales = sales.groupby('date').agg({\n",
    "        'tickets_sold': 'sum',\n",
    "        'revenue': 'sum'\n",
    "    }).reset_index()\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        fig = px.line(\n",
    "            daily_sales,\n",
    "            x='date',\n",
    "            y='tickets_sold',\n",
    "            title='Daily Ticket Sales Over Time'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        fig = px.line(\n",
    "            daily_sales,\n",
    "            x='date',\n",
    "            y='revenue',\n",
    "            title='Daily Revenue Over Time'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Weekend vs weekday analysis\n",
    "    weekend_analysis = sales.groupby('is_weekend').agg({\n",
    "        'tickets_sold': 'mean',\n",
    "        'revenue': 'mean'\n",
    "    }).reset_index()\n",
    "    weekend_analysis['day_type'] = weekend_analysis['is_weekend'].map({True: 'Weekend', False: 'Weekday'})\n",
    "    \n",
    "    col1, col2 = st.columns(2)\n",
    "    \n",
    "    with col1:\n",
    "        fig = px.bar(\n",
    "            weekend_analysis,\n",
    "            x='day_type',\n",
    "            y='tickets_sold',\n",
    "            title='Average Tickets Sold: Weekend vs Weekday'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    with col2:\n",
    "        fig = px.bar(\n",
    "            weekend_analysis,\n",
    "            x='day_type',\n",
    "            y='revenue',\n",
    "            title='Average Revenue: Weekend vs Weekday'\n",
    "        )\n",
    "        st.plotly_chart(fig, use_container_width=True)\n",
    "    \n",
    "    # Top movies by sales\n",
    "    st.subheader(\"🎬 Top Movies by Ticket Sales\")\n",
    "    top_sales = sales.groupby('movie_title')['tickets_sold'].sum().nlargest(15).reset_index()\n",
    "    \n",
    "    fig = px.bar(\n",
    "        top_sales,\n",
    "        x='tickets_sold',\n",
    "        y='movie_title',\n",
    "        orientation='h',\n",
    "        title='Top 15 Movies by Total Ticket Sales'\n",
    "    )\n",
    "    st.plotly_chart(fig, use_container_width=True)\n",
    "\nif __name__ == \"__main__\":\n",
    "    main()