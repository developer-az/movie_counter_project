#!/usr/bin/env python3
"""
Terminal Analytics Interface

A comprehensive command-line interface for movie industry analytics.
Provides the same insights as the dashboard but in a terminal-friendly format.
Supports multiple output formats and interactive exploration.
"""

import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from analytics import MovieAnalytics


class TerminalInterface:
    """Terminal interface for movie analytics."""
    
    def __init__(self, data_path: str = "data/processed"):
        """Initialize with data path."""
        self.analytics = MovieAnalytics(data_path)
        self.loaded = False
    
    def load_data(self) -> bool:
        """Load data and check if successful."""
        print("Loading movie industry data...")
        self.loaded = self.analytics.load_data()
        if self.loaded:
            print("✅ Data loaded successfully!")
            return True
        else:
            print("❌ Failed to load data. Please ensure data files exist.")
            return False
    
    def print_header(self, title: str, width: int = 80):
        """Print a formatted header."""
        print()
        print("=" * width)
        print(f" {title} ".center(width))
        print("=" * width)
    
    def print_section(self, title: str, width: int = 80):
        """Print a section header."""
        print()
        print("-" * width)
        print(f"📊 {title}")
        print("-" * width)
    
    def format_currency(self, amount: float) -> str:
        """Format currency values."""
        if amount >= 1_000_000_000:
            return f"${amount/1_000_000_000:.1f}B"
        elif amount >= 1_000_000:
            return f"${amount/1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"${amount/1_000:.1f}K"
        else:
            return f"${amount:.0f}"
    
    def format_number(self, number: float) -> str:
        """Format large numbers."""
        if number >= 1_000_000:
            return f"{number/1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number/1_000:.1f}K"
        else:
            return f"{number:.0f}"
    
    def show_overview(self):
        """Display overview analytics."""
        self.print_header("MOVIE INDUSTRY OVERVIEW")
        
        overview = self.analytics.get_overview_metrics()
        
        if not overview:
            print("No data available.")
            return
        
        print(f"📈 Dataset Summary:")
        print(f"   • Total Movies: {overview['total_movies']:,}")
        print(f"   • Total Revenue: {self.format_currency(overview['total_revenue'])}")
        print(f"   • Average IMDb Rating: {overview['avg_rating']:.1f}/10")
        print(f"   • Profitable Movies: {overview['profitable_movies']:,} ({overview['profitable_percentage']:.1f}%)")
        print(f"   • Average ROI: {overview['avg_roi']:.1f}%")
        print(f"   • Unique Genres: {overview['genres_count']}")
        print(f"   • Studios: {overview['studios_count']}")
        
        date_range = overview['date_range']
        print(f"   • Date Range: {date_range['start'].strftime('%Y-%m-%d')} to {date_range['end'].strftime('%Y-%m-%d')}")
    
    def show_genre_analysis(self):
        """Display genre analysis."""
        self.print_section("GENRE ANALYSIS")
        
        genre_data = self.analytics.get_genre_analysis()
        
        if not genre_data:
            print("No genre data available.")
            return
        
        print("🎭 Top Performing Genres:")
        print(f"   • Highest Revenue: {genre_data['top_revenue_genre']['name']} ({self.format_currency(genre_data['top_revenue_genre']['revenue'])})")
        print(f"   • Highest Rating: {genre_data['top_rating_genre']['name']} ({genre_data['top_rating_genre']['rating']:.1f}/10)")
        print(f"   • Most Profitable: {genre_data['top_profit_genre']['name']} ({self.format_currency(genre_data['top_profit_genre']['profit'])})")
        
        print("\n📊 Genre Distribution:")
        distribution = genre_data['genre_distribution']
        for genre, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / sum(distribution.values())) * 100
            print(f"   • {genre}: {count} movies ({percentage:.1f}%)")
    
    def show_studio_analysis(self):
        """Display studio analysis."""
        self.print_section("STUDIO ANALYSIS")
        
        studio_data = self.analytics.get_studio_analysis()
        
        if not studio_data:
            print("No studio data available.")
            return
        
        print("🏢 Top Performing Studios:")
        print(f"   • Highest Revenue: {studio_data['top_revenue_studio']['name']} ({self.format_currency(studio_data['top_revenue_studio']['revenue'])})")
        print(f"   • Most Active: {studio_data['most_active_studio']['name']} ({studio_data['most_active_studio']['movie_count']} movies)")
        print(f"   • Best Average: {studio_data['top_avg_revenue_studio']['name']} ({self.format_currency(studio_data['top_avg_revenue_studio']['avg_revenue'])} avg)")
    
    def show_temporal_trends(self):
        """Display temporal trend analysis."""
        self.print_section("TEMPORAL TRENDS")
        
        trends = self.analytics.get_temporal_trends()
        
        if not trends:
            print("No trend data available.")
            return
        
        print("📅 Release Patterns:")
        movies_by_year = trends['movies_by_year']
        revenue_trends = trends['revenue_trends']
        rating_trends = trends['rating_trends']
        
        print(f"   • Years covered: {trends['total_years']}")
        print(f"   • Peak year (movies): {max(movies_by_year, key=movies_by_year.get)} ({movies_by_year[max(movies_by_year, key=movies_by_year.get)]} movies)")
        print(f"   • Best revenue year: {max(revenue_trends, key=revenue_trends.get)} ({self.format_currency(revenue_trends[max(revenue_trends, key=revenue_trends.get)])} avg)")
        print(f"   • Best rating year: {max(rating_trends, key=rating_trends.get)} ({rating_trends[max(rating_trends, key=rating_trends.get)]:.1f}/10 avg)")
    
    def show_sales_analysis(self):
        """Display sales analysis."""
        self.print_section("SALES ANALYSIS")
        
        sales_data = self.analytics.get_sales_analysis()
        
        if not sales_data:
            print("No sales data available.")
            return
        
        print("🎫 Ticket Sales Overview:")
        print(f"   • Total Tickets Sold: {self.format_number(sales_data['total_tickets_sold'])}")
        print(f"   • Total Sales Revenue: {self.format_currency(sales_data['total_sales_revenue'])}")
        print(f"   • Average Daily Tickets: {sales_data['avg_daily_tickets']:.0f}")
        
        weekend_data = sales_data['weekend_vs_weekday']
        print(f"\n📈 Weekend vs Weekday Performance:")
        print(f"   • Weekend Average: {weekend_data['weekend_avg']:.0f} tickets/day")
        print(f"   • Weekday Average: {weekend_data['weekday_avg']:.0f} tickets/day")
        print(f"   • Weekend Boost: {weekend_data['weekend_boost']:.1f}%")
        
        print(f"\n🏆 Top Movies by Ticket Sales:")
        top_movies = sales_data['top_movies_by_tickets']
        for i, (movie, tickets) in enumerate(list(top_movies.items())[:5], 1):
            print(f"   {i}. {movie}: {self.format_number(tickets)} tickets")
    
    def show_top_performers(self, metric: str = 'revenue', limit: int = 10):
        """Display top performing movies."""
        self.print_section(f"TOP PERFORMERS BY {metric.upper()}")
        
        performers = self.analytics.get_top_performers(metric, limit)
        
        if not performers:
            print("No performance data available.")
            return
        
        metric_format = {
            'revenue': lambda x: self.format_currency(x['total_gross']),
            'profit': lambda x: self.format_currency(x['profit']),
            'rating': lambda x: f"{x['imdb_rating']:.1f}/10",
            'roi': lambda x: f"{x['roi']:.1f}%"
        }
        
        format_func = metric_format.get(metric, lambda x: str(x.get(metric, 'N/A')))
        
        for i, movie in enumerate(performers, 1):
            print(f"{i:2d}. {movie['title']} ({movie['genre']}) - {format_func(movie)}")
            print(f"     Studio: {movie['studio']} | Budget: {self.format_currency(movie['budget'])}")
    
    def show_interactive_menu(self):
        """Display interactive menu for exploration."""
        while True:
            self.print_header("MOVIE ANALYTICS - INTERACTIVE MODE")
            print("Select an analysis to view:")
            print()
            print("1. 📊 Overview")
            print("2. 🎭 Genre Analysis")
            print("3. 🏢 Studio Analysis")
            print("4. 📈 Temporal Trends")
            print("5. 🎫 Sales Analysis")
            print("6. 🏆 Top Performers (Revenue)")
            print("7. 💰 Top Performers (Profit)")
            print("8. ⭐ Top Performers (Rating)")
            print("9. 📈 Top Performers (ROI)")
            print("10. 📋 Full Report")
            print("11. 💾 Export Report")
            print("0. Exit")
            print()
            
            try:
                choice = input("Enter your choice (0-11): ").strip()
                
                if choice == '0':
                    print("👋 Thanks for using Movie Analytics!")
                    break
                elif choice == '1':
                    self.show_overview()
                elif choice == '2':
                    self.show_genre_analysis()
                elif choice == '3':
                    self.show_studio_analysis()
                elif choice == '4':
                    self.show_temporal_trends()
                elif choice == '5':
                    self.show_sales_analysis()
                elif choice == '6':
                    self.show_top_performers('revenue')
                elif choice == '7':
                    self.show_top_performers('profit')
                elif choice == '8':
                    self.show_top_performers('rating')
                elif choice == '9':
                    self.show_top_performers('roi')
                elif choice == '10':
                    self.show_full_report()
                elif choice == '11':
                    self.export_report_interactive()
                else:
                    print("❌ Invalid choice. Please enter a number between 0-11.")
                
                if choice != '0':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n👋 Thanks for using Movie Analytics!")
                break
    
    def show_full_report(self):
        """Display comprehensive analytics report."""
        self.show_overview()
        self.show_genre_analysis()
        self.show_studio_analysis()
        self.show_temporal_trends()
        self.show_sales_analysis()
        self.show_top_performers('revenue', 5)
    
    def export_report_interactive(self):
        """Interactive report export."""
        print("\n💾 Export Report")
        print("Choose format:")
        print("1. JSON")
        print("2. CSV")
        
        format_choice = input("Enter choice (1-2): ").strip()
        
        if format_choice == '1':
            format_type = 'json'
        elif format_choice == '2':
            format_type = 'csv'
        else:
            print("❌ Invalid choice.")
            return
        
        default_filename = f"movie_analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        filename = input(f"Enter filename (default: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        try:
            result = self.analytics.export_report(format_type, filename)
            print(f"✅ Report exported to: {result}")
        except Exception as e:
            print(f"❌ Export failed: {e}")


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Movie Industry Analytics - Terminal Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python movie_analytics_terminal.py                    # Interactive mode
  python movie_analytics_terminal.py --overview         # Show overview only
  python movie_analytics_terminal.py --full-report      # Show full report
  python movie_analytics_terminal.py --export json      # Export JSON report
  python movie_analytics_terminal.py --top revenue 10   # Top 10 by revenue
        """
    )
    
    parser.add_argument(
        '--data-path', 
        default='data/processed',
        help='Path to processed data files (default: data/processed)'
    )
    
    parser.add_argument(
        '--overview',
        action='store_true',
        help='Show overview metrics only'
    )
    
    parser.add_argument(
        '--genre',
        action='store_true',
        help='Show genre analysis only'
    )
    
    parser.add_argument(
        '--studio',
        action='store_true',
        help='Show studio analysis only'
    )
    
    parser.add_argument(
        '--trends',
        action='store_true',
        help='Show temporal trends only'
    )
    
    parser.add_argument(
        '--sales',
        action='store_true',
        help='Show sales analysis only'
    )
    
    parser.add_argument(
        '--top',
        nargs=2,
        metavar=('METRIC', 'LIMIT'),
        help='Show top performers by metric (revenue, profit, rating, roi) with limit'
    )
    
    parser.add_argument(
        '--full-report',
        action='store_true',
        help='Show comprehensive report'
    )
    
    parser.add_argument(
        '--export',
        choices=['json', 'csv'],
        help='Export report in specified format'
    )
    
    parser.add_argument(
        '--output',
        help='Output filename for export (optional)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Start interactive mode (default if no other options)'
    )
    
    args = parser.parse_args()
    
    # Initialize interface
    interface = TerminalInterface(args.data_path)
    
    # Load data
    if not interface.load_data():
        sys.exit(1)
    
    # Determine mode
    any_flag = any([
        args.overview, args.genre, args.studio, args.trends, 
        args.sales, args.top, args.full_report, args.export
    ])
    
    if not any_flag or args.interactive:
        # Interactive mode
        interface.show_interactive_menu()
    else:
        # Command-line mode
        if args.overview:
            interface.show_overview()
        
        if args.genre:
            interface.show_genre_analysis()
        
        if args.studio:
            interface.show_studio_analysis()
        
        if args.trends:
            interface.show_temporal_trends()
        
        if args.sales:
            interface.show_sales_analysis()
        
        if args.top:
            metric, limit = args.top
            try:
                limit = int(limit)
                interface.show_top_performers(metric, limit)
            except ValueError:
                print(f"❌ Invalid limit: {limit}. Must be a number.")
        
        if args.full_report:
            interface.show_full_report()
        
        if args.export:
            try:
                result = interface.analytics.export_report(args.export, args.output)
                if args.output:
                    print(f"✅ Report exported to: {result}")
                else:
                    print(result)
            except Exception as e:
                print(f"❌ Export failed: {e}")


if __name__ == "__main__":
    main()