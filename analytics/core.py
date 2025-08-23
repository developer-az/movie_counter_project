"""
Core Analytics Functions

Shared analytics functions that can be used by both dashboard and terminal interfaces.
Provides consistent data analysis capabilities across different output formats.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any


class MovieAnalytics:
    """
    Core analytics class for movie industry data analysis.
    
    Provides methods for loading data, calculating metrics, and generating insights
    that can be used by different interfaces (dashboard, terminal, API).
    """
    
    def __init__(self, data_path: str = "data/processed"):
        """
        Initialize MovieAnalytics with data path.
        
        Args:
            data_path: Path to processed data files
        """
        self.data_path = Path(data_path)
        self._movies = None
        self._sales = None
        self._genre_stats = None
        self._studio_stats = None
        self._monthly_sales = None
    
    def load_data(self) -> bool:
        """
        Load all datasets from processed files.
        
        Returns:
            bool: True if all data loaded successfully, False otherwise
        """
        try:
            self._movies = pd.read_csv(self.data_path / 'movies_processed.csv')
            self._sales = pd.read_csv(self.data_path / 'sales_processed.csv')
            self._genre_stats = pd.read_csv(self.data_path / 'genre_stats.csv')
            self._studio_stats = pd.read_csv(self.data_path / 'studio_stats.csv')
            self._monthly_sales = pd.read_csv(self.data_path / 'monthly_sales.csv')
            
            # Convert date columns
            self._movies['release_date'] = pd.to_datetime(self._movies['release_date'])
            self._sales['date'] = pd.to_datetime(self._sales['date'])
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_overview_metrics(self) -> Dict[str, Any]:
        """
        Get key overview metrics for the dataset.
        
        Returns:
            Dict containing overview metrics
        """
        if self._movies is None:
            return {}
        
        total_movies = len(self._movies)
        total_revenue = self._movies['total_gross'].sum()
        avg_rating = self._movies['imdb_rating'].mean()
        profitable_movies = len(self._movies[self._movies['profit'] > 0])
        profitable_pct = (profitable_movies / total_movies) * 100
        avg_roi = self._movies['roi'].mean()
        
        return {
            'total_movies': total_movies,
            'total_revenue': total_revenue,
            'avg_rating': avg_rating,
            'profitable_movies': profitable_movies,
            'profitable_percentage': profitable_pct,
            'avg_roi': avg_roi,
            'genres_count': self._movies['genre'].nunique(),
            'studios_count': self._movies['studio'].nunique(),
            'date_range': {
                'start': self._movies['release_date'].min(),
                'end': self._movies['release_date'].max()
            }
        }
    
    def get_genre_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive genre analysis.
        
        Returns:
            Dict containing genre analysis data
        """
        if self._movies is None or self._genre_stats is None:
            return {}
        
        # Genre distribution
        genre_counts = self._movies['genre'].value_counts()
        
        # Top performing genres by different metrics - handle empty dataframe
        if len(self._genre_stats) == 0:
            return {'genre_distribution': genre_counts.to_dict()}
        
        # Find columns that exist
        revenue_col = 'total_gross' if 'total_gross' in self._genre_stats.columns else 'total_revenue'
        rating_col = 'avg_rating' if 'avg_rating' in self._genre_stats.columns else 'rating'  
        profit_col = 'avg_profit' if 'avg_profit' in self._genre_stats.columns else 'profit'
        
        top_revenue_genre = self._genre_stats.loc[self._genre_stats[revenue_col].idxmax()]
        top_rating_genre = self._genre_stats.loc[self._genre_stats[rating_col].idxmax()]
        top_profit_genre = self._genre_stats.loc[self._genre_stats[profit_col].idxmax()]
        
        return {
            'genre_distribution': genre_counts.to_dict(),
            'top_revenue_genre': {
                'name': top_revenue_genre['genre'],
                'revenue': top_revenue_genre[revenue_col]
            },
            'top_rating_genre': {
                'name': top_rating_genre['genre'],
                'rating': top_rating_genre[rating_col]
            },
            'top_profit_genre': {
                'name': top_profit_genre['genre'],
                'profit': top_profit_genre[profit_col]
            },
            'genre_stats': self._genre_stats.to_dict('records')
        }
    
    def get_studio_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive studio analysis.
        
        Returns:
            Dict containing studio analysis data
        """
        if self._movies is None or self._studio_stats is None:
            return {}
        
        # Top performing studios
        revenue_col = 'total_gross' if 'total_gross' in self._studio_stats.columns else 'total_revenue'
        avg_revenue_col = 'avg_gross' if 'avg_gross' in self._studio_stats.columns else 'avg_revenue'
        
        top_revenue_studio = self._studio_stats.loc[self._studio_stats[revenue_col].idxmax()]
        most_active_studio = self._studio_stats.loc[self._studio_stats['movie_count'].idxmax()]
        top_avg_revenue_studio = self._studio_stats.loc[self._studio_stats[avg_revenue_col].idxmax()]
        
        return {
            'top_revenue_studio': {
                'name': top_revenue_studio['studio'],
                'revenue': top_revenue_studio[revenue_col]
            },
            'most_active_studio': {
                'name': most_active_studio['studio'],
                'movie_count': most_active_studio['movie_count']
            },
            'top_avg_revenue_studio': {
                'name': top_avg_revenue_studio['studio'],
                'avg_revenue': top_avg_revenue_studio[avg_revenue_col]
            },
            'studio_stats': self._studio_stats.to_dict('records')
        }
    
    def get_temporal_trends(self) -> Dict[str, Any]:
        """
        Get temporal analysis of movie trends.
        
        Returns:
            Dict containing temporal analysis data
        """
        if self._movies is None:
            return {}
        
        # Movies by release year
        movies_by_year = self._movies.groupby(self._movies['release_date'].dt.year).size()
        
        # Revenue trends by year
        revenue_by_year = self._movies.groupby(self._movies['release_date'].dt.year)['total_gross'].mean()
        
        # Rating trends by year
        rating_by_year = self._movies.groupby(self._movies['release_date'].dt.year)['imdb_rating'].mean()
        
        return {
            'movies_by_year': movies_by_year.to_dict(),
            'revenue_trends': revenue_by_year.to_dict(),
            'rating_trends': rating_by_year.to_dict(),
            'total_years': len(movies_by_year)
        }
    
    def get_sales_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive sales analysis.
        
        Returns:
            Dict containing sales analysis data
        """
        if self._sales is None:
            return {}
        
        # Total sales metrics
        total_tickets = self._sales['tickets_sold'].sum()
        total_sales_revenue = self._sales['revenue'].sum()
        avg_daily_tickets = self._sales['tickets_sold'].mean()
        
        # Top movies by ticket sales
        top_movies_tickets = self._sales.groupby('movie_title')['tickets_sold'].sum().sort_values(ascending=False).head(10)
        
        # Weekend vs weekday analysis
        self._sales['day_of_week'] = self._sales['date'].dt.dayofweek
        weekend_sales = self._sales[self._sales['day_of_week'].isin([5, 6])]['tickets_sold'].mean()
        weekday_sales = self._sales[~self._sales['day_of_week'].isin([5, 6])]['tickets_sold'].mean()
        
        return {
            'total_tickets_sold': total_tickets,
            'total_sales_revenue': total_sales_revenue,
            'avg_daily_tickets': avg_daily_tickets,
            'top_movies_by_tickets': top_movies_tickets.to_dict(),
            'weekend_vs_weekday': {
                'weekend_avg': weekend_sales,
                'weekday_avg': weekday_sales,
                'weekend_boost': (weekend_sales / weekday_sales - 1) * 100 if weekday_sales > 0 else 0
            },
            'sales_date_range': {
                'start': self._sales['date'].min(),
                'end': self._sales['date'].max()
            }
        }
    
    def get_top_performers(self, metric: str = 'revenue', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top performing movies by specified metric.
        
        Args:
            metric: Metric to sort by ('revenue', 'profit', 'rating', 'roi')
            limit: Number of top performers to return
            
        Returns:
            List of movie dictionaries
        """
        if self._movies is None:
            return []
        
        metric_column_map = {
            'revenue': 'total_gross',
            'profit': 'profit',
            'rating': 'imdb_rating',
            'roi': 'roi'
        }
        
        if metric not in metric_column_map:
            return []
        
        column = metric_column_map[metric]
        top_movies = self._movies.nlargest(limit, column)
        
        return top_movies[['title', 'genre', 'studio', 'release_date', 'budget', 'total_gross', 'profit', 'imdb_rating', 'roi']].to_dict('records')
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive analytics report.
        
        Returns:
            Dict containing all analytics data
        """
        return {
            'overview': self.get_overview_metrics(),
            'genre_analysis': self.get_genre_analysis(),
            'studio_analysis': self.get_studio_analysis(),
            'temporal_trends': self.get_temporal_trends(),
            'sales_analysis': self.get_sales_analysis(),
            'top_performers': {
                'by_revenue': self.get_top_performers('revenue', 5),
                'by_profit': self.get_top_performers('profit', 5),
                'by_rating': self.get_top_performers('rating', 5),
                'by_roi': self.get_top_performers('roi', 5)
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def export_report(self, format_type: str = 'json', output_path: str = None) -> str:
        """
        Export comprehensive report to specified format.
        
        Args:
            format_type: Export format ('json', 'csv')
            output_path: Output file path (optional)
            
        Returns:
            String representation of the report or file path
        """
        report = self.get_comprehensive_report()
        
        if format_type.lower() == 'json':
            if output_path:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                return output_path
            else:
                return json.dumps(report, indent=2, default=str)
        
        elif format_type.lower() == 'csv':
            # For CSV, export key metrics as a flat structure
            overview = report['overview']
            csv_data = {
                'metric': ['total_movies', 'total_revenue', 'avg_rating', 'profitable_percentage', 'avg_roi'],
                'value': [
                    overview['total_movies'],
                    overview['total_revenue'],
                    overview['avg_rating'],
                    overview['profitable_percentage'],
                    overview['avg_roi']
                ]
            }
            df = pd.DataFrame(csv_data)
            
            if output_path:
                df.to_csv(output_path, index=False)
                return output_path
            else:
                return df.to_csv(index=False)
        
        return json.dumps(report, indent=2, default=str)
    
    @property
    def movies(self) -> Optional[pd.DataFrame]:
        """Get movies dataframe."""
        return self._movies
    
    @property
    def sales(self) -> Optional[pd.DataFrame]:
        """Get sales dataframe."""
        return self._sales
    
    @property
    def is_data_loaded(self) -> bool:
        """Check if data is loaded."""
        return all([
            self._movies is not None,
            self._sales is not None,
            self._genre_stats is not None,
            self._studio_stats is not None,
            self._monthly_sales is not None
        ])