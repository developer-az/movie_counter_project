# Technical Documentation

## Architecture Overview

The Movie Industry Analytics project follows a modular architecture with clear separation of concerns:

```
Data Layer → Processing Layer → Analysis Layer → Presentation Layer
```

### Data Layer
- **Raw Data Storage**: CSV files in `data/raw/`
- **Processed Data**: Cleaned and transformed data in `data/processed/`
- **Schema Validation**: Consistent data structures across datasets

### Processing Layer
- **Data Generation**: `scripts/generate_data.py`
- **Data Cleaning**: `scripts/data_processing.py`
- **Aggregation**: Statistical summaries and derived metrics

### Analysis Layer
- **Exploratory Analysis**: Jupyter notebook with comprehensive EDA
- **Statistical Analysis**: Correlation, distribution, and trend analysis
- **Visualization**: Multiple chart types and interactive plots

### Presentation Layer
- **Dashboard**: Streamlit-based interactive web application
- **Filtering**: Dynamic data exploration capabilities
- **Export**: Data download and sharing features

## Data Processing Pipeline

### 1. Data Generation
```python
generate_data.py:
├── Movie metadata generation (500 movies)
├── Realistic budget/revenue distributions
├── Time-based sales simulation (365 days)
└── Export to CSV format
```

### 2. Data Cleaning
```python
data_processing.py:
├── Date parsing and validation
├── Derived metrics calculation (ROI, profit)
├── Categorical encoding
├── Statistical aggregations
└── Multiple output datasets
```

### 3. Analysis Pipeline
```python
movie_eda.ipynb:
├── Data loading and validation
├── Descriptive statistics
├── Correlation analysis
├── Visualization generation
└── Insight extraction
```

## Database Schema

### Movies Table
```sql
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title TEXT UNIQUE NOT NULL,
    genre VARCHAR(50) NOT NULL,
    release_date DATE NOT NULL,
    rating VARCHAR(10),
    studio VARCHAR(100),
    runtime_minutes INTEGER,
    budget BIGINT,
    domestic_gross BIGINT,
    international_gross BIGINT,
    total_gross BIGINT,
    imdb_rating DECIMAL(3,1),
    roi DECIMAL(10,2),
    profit BIGINT
);
```

### Sales Table
```sql
CREATE TABLE daily_sales (
    sale_id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(movie_id),
    movie_title TEXT,
    date DATE NOT NULL,
    tickets_sold INTEGER,
    revenue DECIMAL(10,2)
);
```

## API Documentation

### Streamlit Dashboard Endpoints

#### Data Loading Functions
- `load_data()`: Cached data loading with error handling
- `filter_data()`: Dynamic filtering based on user inputs
- `aggregate_data()`: Real-time aggregation calculations

#### Visualization Functions
- `create_scatter_plot()`: Budget vs Revenue analysis
- `create_time_series()`: Temporal trend visualization
- `create_distribution()`: Statistical distribution plots
- `create_comparison()`: Category comparison charts

### Performance Optimizations
- **Caching**: `@st.cache_data` decorator for expensive operations
- **Lazy Loading**: Progressive data loading for large datasets
- **Memory Management**: Efficient pandas operations
- **Responsive Design**: Optimized for various screen sizes

## Development Setup

### Environment Configuration
```bash
# Create virtual environment
python -m venv movie-analytics-env
source movie-analytics-env/bin/activate  # Linux/Mac
# movie-analytics-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; print(streamlit.__version__)"
```

### Code Quality Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Function parameter and return type annotations
- **Docstrings**: Comprehensive function documentation
- **Error Handling**: Graceful failure and user feedback

### Testing Framework
```bash
# Run unit tests
pytest tests/

# Test data generation
python -m pytest tests/test_data_generation.py

# Test dashboard components
python -m pytest tests/test_dashboard.py
```

## Deployment Options

### Local Development
```bash
streamlit run dashboard/streamlit_app.py --server.port 8501
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/streamlit_app.py"]
```

### Cloud Deployment
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Container-based deployment
- **AWS/Azure**: Scalable cloud infrastructure
- **Docker Hub**: Containerized distribution

## Monitoring and Maintenance

### Performance Metrics
- **Load Time**: Dashboard initialization speed
- **Response Time**: User interaction responsiveness
- **Memory Usage**: Resource consumption monitoring
- **Error Rates**: Exception tracking and logging

### Maintenance Tasks
- **Data Updates**: Regular dataset refreshes
- **Dependency Updates**: Library version management
- **Security Patches**: Vulnerability assessment
- **Feature Enhancements**: User feedback integration

## Security Considerations

### Data Protection
- **Input Validation**: SQL injection prevention
- **Access Control**: Role-based permissions
- **Data Encryption**: Sensitive information protection
- **Audit Logging**: User activity tracking

### Best Practices
- **Environment Variables**: Configuration management
- **Secret Management**: API key protection
- **HTTPS Enforcement**: Secure communication
- **Regular Backups**: Data recovery planning

## Troubleshooting Guide

### Common Issues
1. **Module Not Found**: Verify virtual environment activation
2. **Data Loading Errors**: Check file paths and permissions
3. **Visualization Issues**: Ensure plotly/streamlit compatibility
4. **Performance Problems**: Monitor memory usage and caching

### Debug Commands
```bash
# Check Python environment
python --version
pip list

# Validate data files
python -c "import pandas as pd; print(pd.read_csv('data/raw/movies_raw.csv').shape)"

# Test dashboard components
streamlit run dashboard/streamlit_app.py --server.headless true
```