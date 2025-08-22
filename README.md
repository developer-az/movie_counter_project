# Movie Industry Analytics Project

A comprehensive data science project analyzing movie industry trends, box office performance, and consumer behavior through interactive visualizations and statistical analysis.

## 🎯 Project Overview

This project transforms movie industry data into actionable insights through advanced analytics and interactive dashboards. It demonstrates proficiency in data collection, processing, analysis, and visualization using modern data science tools and techniques.

### Key Objectives
- **Data Analysis**: Comprehensive exploration of movie industry trends and patterns
- **Visualization**: Professional, interactive dashboards for data storytelling
- **Insights Generation**: Extract actionable business intelligence from raw data
- **Technical Excellence**: Showcase best practices in data science workflow

## 📊 Features

### Data Analytics
- **500+ Movies**: Comprehensive dataset with budget, revenue, ratings, and metadata
- **Time Series Analysis**: Daily sales tracking and seasonal patterns
- **Genre & Studio Analysis**: Performance metrics across categories
- **ROI Calculations**: Financial performance and profitability analysis

### Interactive Dashboard
- **Real-time Filtering**: Dynamic data exploration with multiple filter options
- **Multiple Views**: Overview, Genre Analysis, Studio Performance, Trends, and Sales
- **Professional Visualizations**: Plotly-powered interactive charts and graphs
- **Key Performance Indicators**: At-a-glance metrics and insights

### Technical Features
- **Automated Data Pipeline**: Scripts for data generation and processing
- **Jupyter Notebooks**: Detailed exploratory data analysis
- **Clean Architecture**: Well-organized codebase with separation of concerns
- **Documentation**: Comprehensive project documentation and code comments

## 🏗️ Project Structure

```
movie_counter_project/
├── data/                     # Data storage
│   ├── raw/                  # Raw datasets
│   │   ├── movies_raw.csv
│   │   └── daily_sales_raw.csv
│   └── processed/            # Cleaned and processed data
│       ├── movies_processed.csv
│       ├── sales_processed.csv
│       ├── genre_stats.csv
│       ├── studio_stats.csv
│       └── monthly_sales.csv
├── notebooks/                # Jupyter notebooks for analysis
│   └── movie_eda.ipynb      # Exploratory Data Analysis
├── scripts/                  # Data processing scripts
│   ├── generate_data.py     # Synthetic data generation
│   ├── data_processing.py   # Data cleaning and transformation
│   ├── database_operations.py # Original database operations
│   └── create_table.sql     # Database schema
├── dashboard/                # Interactive dashboard
│   └── streamlit_app.py     # Main dashboard application
├── tests/                    # Unit tests (placeholder)
├── docs/                     # Additional documentation
├── .github/workflows/        # CI/CD workflows (placeholder)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/developer-az/movie_counter_project.git
   cd movie_counter_project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data**:
   ```bash
   cd scripts
   python generate_data.py
   python data_processing.py
   ```

4. **Launch the dashboard**:
   ```bash
   cd dashboard
   streamlit run streamlit_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

### Alternative: Jupyter Analysis
To explore the data analysis notebooks:
```bash
jupyter notebook notebooks/movie_eda.ipynb
```

## 📈 Dashboard Features

### Overview Tab
- **Key Metrics**: Total movies, box office revenue, ratings, profitability
- **Scatter Plot**: Budget vs Revenue with genre coloring
- **ROI Distribution**: Histogram of return on investment
- **Top Performers**: Tables of highest-grossing and most profitable movies

### Genre Analysis Tab
- **Distribution**: Pie chart of movies by genre
- **Performance**: Average revenue and ratings by genre
- **Detailed Metrics**: Comprehensive genre performance table

### Studio Analysis Tab
- **Studio Rankings**: Top studios by total revenue
- **Performance Scatter**: Movies count vs average revenue
- **Studio Metrics**: Detailed performance statistics

### Trends Analysis Tab
- **Release Patterns**: Movies released per year
- **Revenue Trends**: Average revenue over time
- **Rating Evolution**: IMDb ratings vs release year with budget sizing

### Sales Analysis Tab
- **Daily Sales**: Time series of ticket sales and revenue
- **Weekend Effect**: Comparison of weekend vs weekday performance
- **Top Movies**: Ranking by total ticket sales

## 🔍 Data Insights

### Key Findings
- **Fantasy** genre shows highest profitability on average
- **Action** movies receive highest average IMDb ratings
- **Warner Bros** is the most active studio by movie count
- Weekend sales are approximately **50%** higher than weekday sales
- **68%** of movies in the dataset are profitable

### Business Intelligence
- Budget allocation strategies by genre performance
- Seasonal release timing optimization
- Studio partnership and investment decisions
- Market trend identification and forecasting

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Streamlit**: Interactive web dashboard framework

### Visualization Libraries
- **Plotly**: Interactive charts and graphs
- **Matplotlib**: Statistical plotting
- **Seaborn**: Statistical data visualization
- **Altair**: Declarative statistical visualization

### Data Science Tools
- **Jupyter**: Interactive development environment
- **Scikit-learn**: Machine learning library
- **psycopg2**: PostgreSQL database connectivity

## 📊 Data Schema

### Movies Dataset
- **movie_id**: Unique identifier
- **title**: Movie title
- **genre**: Movie category
- **release_date**: Release date
- **rating**: MPAA rating (G, PG, PG-13, R, NC-17)
- **studio**: Production studio
- **runtime_minutes**: Movie duration
- **budget**: Production budget
- **domestic_gross**: US box office revenue
- **international_gross**: International revenue
- **total_gross**: Combined revenue
- **imdb_rating**: IMDb score (1-10)
- **roi**: Return on investment percentage
- **profit**: Net profit (revenue - budget)

### Sales Dataset
- **movie_id**: Reference to movies table
- **movie_title**: Movie name
- **date**: Sale date
- **tickets_sold**: Number of tickets
- **revenue**: Daily revenue

## 🧪 Development

### Data Generation
The project includes synthetic data generation that creates realistic movie industry datasets:
- **Realistic Distributions**: Log-normal budget distributions, genre-based adjustments
- **Temporal Patterns**: Release date trends, seasonal variations
- **Market Dynamics**: Studio influences, rating correlations

### Testing
Run tests to validate data processing:
```bash
cd tests
python -m pytest
```

### Code Quality
- **PEP 8**: Python style guide compliance
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust exception management
- **Performance**: Optimized data processing with caching

## 📈 Future Enhancements

### Planned Features
- **Machine Learning**: Predictive models for box office success
- **Real-time Data**: Integration with live movie APIs
- **Advanced Analytics**: Sentiment analysis, market segmentation
- **Mobile Optimization**: Responsive dashboard design

### Technical Improvements
- **Database Integration**: PostgreSQL backend implementation
- **API Development**: RESTful API for data access
- **Docker Deployment**: Containerized application
- **Cloud Deployment**: AWS/Azure hosting options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Developer**: developer-az
**Project**: Movie Industry Analytics
**Repository**: https://github.com/developer-az/movie_counter_project

---

*Built with ❤️ using Python, Streamlit, and modern data science tools*