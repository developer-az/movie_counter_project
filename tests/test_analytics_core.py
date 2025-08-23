#!/usr/bin/env python3
"""
Test Analytics Core Module

Tests the shared analytics functionality to ensure it works correctly
with both terminal and dashboard interfaces.
"""

import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from analytics import MovieAnalytics

def test_analytics_core():
    """Test the analytics core functionality."""
    print("Testing Analytics Core Module...")
    print("=" * 50)
    
    # Initialize analytics
    analytics = MovieAnalytics('data/processed')
    
    # Test data loading
    print("📊 Testing data loading...")
    if analytics.load_data():
        print("✅ Data loaded successfully")
    else:
        print("❌ Failed to load data")
        return False
    
    # Test overview metrics
    print("\n📈 Testing overview metrics...")
    overview = analytics.get_overview_metrics()
    if overview and 'total_movies' in overview:
        print(f"✅ Overview metrics: {overview['total_movies']} movies, ${overview['total_revenue']/1e9:.1f}B revenue")
    else:
        print("❌ Failed to get overview metrics")
        return False
    
    # Test genre analysis
    print("\n🎭 Testing genre analysis...")
    genre_data = analytics.get_genre_analysis()
    if genre_data and 'top_revenue_genre' in genre_data:
        print(f"✅ Genre analysis: Top revenue genre is {genre_data['top_revenue_genre']['name']}")
    else:
        print("❌ Failed to get genre analysis")
        return False
    
    # Test top performers
    print("\n🏆 Testing top performers...")
    top_movies = analytics.get_top_performers('revenue', 5)
    if top_movies and len(top_movies) > 0:
        print(f"✅ Top performers: Found {len(top_movies)} movies, top is '{top_movies[0]['title']}'")
    else:
        print("❌ Failed to get top performers")
        return False
    
    # Test export functionality
    print("\n💾 Testing export functionality...")
    try:
        json_export = analytics.export_report('json')
        if json_export and '"overview":' in json_export:
            print("✅ JSON export working")
        else:
            print("❌ JSON export failed")
            return False
    except Exception as e:
        print(f"❌ JSON export error: {e}")
        return False
    
    # Test comprehensive report
    print("\n📋 Testing comprehensive report...")
    try:
        report = analytics.get_comprehensive_report()
        if report and all(key in report for key in ['overview', 'genre_analysis', 'studio_analysis']):
            print("✅ Comprehensive report working")
        else:
            print("❌ Comprehensive report incomplete")
            return False
    except Exception as e:
        print(f"❌ Comprehensive report error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All analytics core tests passed!")
    return True

if __name__ == "__main__":
    success = test_analytics_core()
    sys.exit(0 if success else 1)