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

### ⚡ Quick Setup Checklist
- [ ] Install system dependencies (`python3-full`, `python3-venv`)
- [ ] Install Python packages (`pip install --break-system-packages -r requirements.txt`)
- [ ] Generate data (`python3 scripts/generate_data.py`)
- [ ] Process data (`python3 scripts/data_processing.py`)
- [ ] Run tests (`python3 tests/test_basic.py`)
- [ ] Launch dashboard (`streamlit run dashboard/streamlit_app.py --server.port 8501`)
- [ ] Access at `http://localhost:8501`

### Prerequisites
- **Python 3.8+**: Required for all dependencies
- **pip**: Python package manager
- **python3-venv** (recommended): For virtual environment management
- **python3-full**: Complete Python installation with all components

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/developer-az/movie_counter_project.git
   cd movie_counter_project
   ```

2. **Install system dependencies** (Ubuntu/Debian):
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv python3-full
   ```

3. **Install Python dependencies**:
   
   **Option A: Using system packages (if you encounter externally-managed-environment error)**:
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```
   
   **Option B: Using virtual environment (recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Generate sample data**:
   ```bash
   cd scripts
   python3 generate_data.py
   python3 data_processing.py
   cd ..
   ```

5. **Test the setup**:
   ```bash
   cd tests
   python3 test_basic.py
   cd ..
   ```

6. **Launch the dashboard**:
   ```bash
   cd dashboard
   streamlit run streamlit_app.py --server.port 8501
   ```

7. **Open your browser** to `http://localhost:8501`

### Alternative: Jupyter Analysis
To explore the data analysis notebooks:
```bash
jupyter notebook notebooks/movie_eda.ipynb
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### **1. Externally Managed Environment Error**
**Error**: `error: externally-managed-environment`

**Solution**: Use one of these approaches:
```bash
# Option 1: Install with system override
pip install --break-system-packages -r requirements.txt

# Option 2: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **2. Python Command Not Found**
**Error**: `Command 'python' not found, did you mean: command 'python3'`

**Solution**: Use `python3` instead of `python`:
```bash
python3 generate_data.py
python3 data_processing.py
```

#### **3. Dashboard Syntax Errors**
**Error**: `SyntaxError: unexpected character after line continuation character`

**Solution**: The dashboard file has been fixed. If you encounter this:
1. Ensure you have the latest version of `dashboard/streamlit_app.py`
2. Check for any malformed string literals
3. Run: `python3 -m py_compile dashboard/streamlit_app.py`

#### **4. Data Files Not Found**
**Error**: `FileNotFoundError: [Errno 2] No such file or directory`

**Solution**: Ensure data generation completed successfully:
```bash
cd scripts
python3 generate_data.py
python3 data_processing.py
cd ..
ls -la data/processed/  # Should show CSV files
```

#### **5. Port Already in Use**
**Error**: `Port 8501 is already in use`

**Solution**: Use a different port or kill existing process:
```bash
# Kill existing streamlit process
pkill -f streamlit

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

#### **6. Virtual Environment Issues**
**Error**: `bash: venv/bin/activate: No such file or directory`

**Solution**: Recreate the virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verification Steps

After installation, verify everything works:

1. **Check Python version**:
   ```bash
   python3 --version  # Should be 3.8+
   ```

2. **Verify dependencies**:
   ```bash
   python3 -c "import streamlit, pandas, plotly; print('All dependencies installed!')"
   ```

3. **Test data generation**:
   ```bash
   cd tests
   python3 test_basic.py
   ```

4. **Check dashboard syntax**:
   ```bash
   python3 -m py_compile dashboard/streamlit_app.py
   ```

5. **Verify dashboard access**:
   ```bash
   curl -s -I http://localhost:8501 | head -1
   # Should return: HTTP/1.1 200 OK
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

### Recent Fixes and Improvements

#### **Dashboard Syntax Issues (Fixed)**
- **Problem**: Malformed string literals in `dashboard/streamlit_app.py` caused syntax errors
- **Solution**: Completely rewrote the dashboard file with proper Python syntax
- **Status**: ✅ **RESOLVED**

#### **Python Environment Issues (Addressed)**
- **Problem**: Ubuntu's externally-managed-environment prevented pip installations
- **Solution**: Added `--break-system-packages` flag and virtual environment options
- **Status**: ✅ **RESOLVED**

#### **Command Compatibility (Fixed)**
- **Problem**: `python` command not available, only `python3`
- **Solution**: Updated all documentation to use `python3` explicitly
- **Status**: ✅ **RESOLVED**

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