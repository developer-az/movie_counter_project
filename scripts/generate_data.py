"""
Movie Data Generator

This script generates synthetic movie data for analysis and visualization.
It creates realistic movie datasets with information about genres, ratings,
box office performance, and ticket sales.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_movie_data(n_movies=500):
    """Generate synthetic movie dataset"""
    
    # Movie titles (combination of adjectives and nouns)
    adjectives = ['Amazing', 'Incredible', 'Ultimate', 'Dark', 'Brilliant', 'Epic', 'Hidden', 
                  'Lost', 'Golden', 'Secret', 'Mysterious', 'Fantastic', 'Wild', 'Dangerous']
    nouns = ['Adventure', 'Mystery', 'Legacy', 'Quest', 'Journey', 'Chronicles', 'Saga', 
             'Tales', 'Dreams', 'Destiny', 'Warrior', 'Guardian', 'Kingdom', 'Empire']
    
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 
              'Animation', 'Documentary', 'Fantasy']
    
    ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
    
    studios = ['Universal Pictures', 'Warner Bros', 'Disney', 'Sony Pictures', 'Paramount', 
               '20th Century Fox', 'MGM', 'Lionsgate', 'Netflix', 'Amazon Studios']
    
    data = []
    
    for i in range(n_movies):
        # Generate movie title
        title = f"{random.choice(adjectives)} {random.choice(nouns)}"
        if random.random() < 0.3:  # 30% chance of sequel
            title += f" {random.choice(['II', 'III', 'Returns', 'Reloaded', 'Rising'])}"
        
        # Generate release date (last 10 years)
        start_date = datetime.now() - timedelta(days=10*365)
        end_date = datetime.now()
        release_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        
        # Generate other attributes
        genre = random.choice(genres)
        rating = random.choice(ratings)
        studio = random.choice(studios)
        
        # Runtime (80-200 minutes, normally distributed around 120)
        runtime = max(80, min(200, int(np.random.normal(120, 25))))
        
        # Budget (influenced by genre and studio)
        base_budget = np.random.lognormal(16, 1)  # Log-normal distribution
        if genre in ['Action', 'Sci-Fi', 'Fantasy']:
            base_budget *= 1.5
        if studio in ['Disney', 'Warner Bros', 'Universal Pictures']:
            base_budget *= 1.3
        budget = max(1_000_000, min(300_000_000, int(base_budget)))
        
        # Box office (related to budget but with variance)
        box_office_multiplier = np.random.lognormal(0, 1)  # Can be flop or hit
        domestic_gross = int(budget * box_office_multiplier * random.uniform(0.5, 4.0))
        international_gross = int(domestic_gross * random.uniform(0.3, 2.5))
        
        # IMDb rating (0-10, normally distributed around 6.5)
        imdb_rating = max(1, min(10, np.random.normal(6.5, 1.5)))
        
        # Tickets sold (based on domestic gross, average ticket price ~$10)
        avg_ticket_price = random.uniform(8, 15)
        tickets_sold = int(domestic_gross / avg_ticket_price)
        
        # Current tickets available (for the original database concept)
        tickets_available = random.randint(0, 500)
        
        data.append({
            'movie_id': i + 1,
            'title': title,
            'genre': genre,
            'release_date': release_date.strftime('%Y-%m-%d'),
            'rating': rating,
            'studio': studio,
            'runtime_minutes': runtime,
            'budget': budget,
            'domestic_gross': domestic_gross,
            'international_gross': international_gross,
            'total_gross': domestic_gross + international_gross,
            'imdb_rating': round(imdb_rating, 1),
            'tickets_sold': tickets_sold,
            'tickets_available': tickets_available
        })
    
    return pd.DataFrame(data)

def generate_daily_sales_data(movies_df, days_back=365):
    """Generate daily ticket sales data for dashboard time series"""
    
    sales_data = []
    
    # Get top 20 movies by total gross for daily sales tracking
    top_movies = movies_df.nlargest(20, 'total_gross')
    
    start_date = datetime.now() - timedelta(days=days_back)
    
    for _, movie in top_movies.iterrows():
        # Generate daily sales for each movie
        movie_release = datetime.strptime(movie['release_date'], '%Y-%m-%d')
        
        # Only generate sales data after movie release
        movie_start_date = max(start_date, movie_release)
        
        current_date = movie_start_date
        while current_date <= datetime.now():
            # Simulate daily sales with some randomness
            # Sales peak in first few weeks then decline
            days_since_release = (current_date - movie_release).days
            
            if days_since_release < 30:  # First month - peak sales
                base_sales = random.randint(100, 1000)
            elif days_since_release < 90:  # Next 2 months - declining
                base_sales = random.randint(50, 300)
            else:  # Long tail
                base_sales = random.randint(0, 50)
            
            # Weekend boost
            if current_date.weekday() >= 5:  # Saturday, Sunday
                base_sales = int(base_sales * 1.5)
            
            sales_data.append({
                'movie_id': movie['movie_id'],
                'movie_title': movie['title'],
                'date': current_date.strftime('%Y-%m-%d'),
                'tickets_sold': base_sales,
                'revenue': base_sales * random.uniform(8, 15)
            })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(sales_data)

def main():
    """Main function to generate and save datasets"""
    
    print("Generating movie dataset...")
    movies_df = generate_movie_data(500)
    
    print("Generating daily sales data...")
    sales_df = generate_daily_sales_data(movies_df)
    
    # Create data directories if they don't exist
    os.makedirs('../data/raw', exist_ok=True)
    os.makedirs('../data/processed', exist_ok=True)
    
    # Save raw data
    movies_df.to_csv('../data/raw/movies_raw.csv', index=False)
    sales_df.to_csv('../data/raw/daily_sales_raw.csv', index=False)
    
    print(f"Generated {len(movies_df)} movies and {len(sales_df)} daily sales records")
    print("Data saved to:")
    print("- data/raw/movies_raw.csv")
    print("- data/raw/daily_sales_raw.csv")
    
    # Display basic statistics
    print("\n=== Dataset Overview ===")
    print(f"Movies dataset shape: {movies_df.shape}")
    print(f"Sales dataset shape: {sales_df.shape}")
    print(f"Date range: {sales_df['date'].min()} to {sales_df['date'].max()}")
    print(f"Genres: {', '.join(movies_df['genre'].unique())}")
    print(f"Average IMDb rating: {movies_df['imdb_rating'].mean():.1f}")
    print(f"Total box office (all movies): ${movies_df['total_gross'].sum():,.0f}")

if __name__ == "__main__":
    main()