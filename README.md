# ShopLink Data Pipeline - ETL & Testing Framework

## 📋 Project Overview

A robust, production-ready ETL pipeline for processing e-commerce order data with comprehensive testing and data validation. This project demonstrates enterprise-level data engineering practices for ensuring data quality and reliability in fast-growing online marketplaces.

## 🎯 Business Context

At **ShopLink**, we connect thousands of buyers and sellers across the country. This pipeline processes raw order data that, while standardized in format, contains hidden data quality issues that could lead to faulty business decisions if not properly handled.

## ⚠️ The Challenge

Raw order data may contain:
- **Out-of-range quantities** or negative prices
- **Multi-currency price formats** (`₦2500`, `$35`, `45 dollars`)
- **Missing or inconsistent fields**
- **Payment status variations** (`Paid`, `pending`, `REFUND`)
- **Silent data corruption** risks

## 🛠️ Technical Solution

### Pipeline Architecture
```
Raw Data → Reader → Validator → Transformer → Analyzer → Exporter
```

### Key Components
- **ShoplinkReader**: Multi-format data ingestion (CSV/JSON)
- **ShoplinkValidator**: Data quality checks & normalization
- **ShoplinkTransformer**: Business logic & data enrichment
- **ShoplinkAnalyzer**: Business intelligence & insights
- **ShoplinkExporter**: Multi-format output generation

## 📊 Features

### Data Validation
- Schema enforcement & required field validation
- Numeric value cleaning & currency normalization
- Timestamp format standardization
- Payment status normalization
- Automated missing value computation

### Business Insights
- Sales aggregation by item, status, and time periods
- Price anomaly detection
- Top seller identification
- Conversion rate analysis
- Refund impact assessment

### Testing Framework
- Comprehensive unit test coverage
- Edge case simulation
- Data fixture management
- Integration testing
- Coverage reporting

## 🚀 Quick Start

### Installation
```bash
git clone <repository-url>
cd shoplink-pipeline
poetry install
```

### Usage
```bash
# Run the complete pipeline
python -m order_pipeline.pipeline

# Run tests with coverage
poetry run pytest --cov=order_pipeline 

# Test specific components
poetry run pytest tests/test_validator.py -v
```

## 📁 Project Structure
```
order_pipeline/
├── reader.py          # Data ingestion
├── validator.py       # Data quality & validation
├── transformer.py     # Data transformation
├── analyzer.py        # Business intelligence
├── exporter.py        # Data export
├── pipeline.py        # ETL orchestration
└── __init__.py

tests/
├── test_reader.py
├── test_validator.py
├── test_transformer.py
├── test_analyzer.py
├── test_exporter.py
└── test_pipeline.py
```

## 🧪 Testing Strategy

### Unit Testing
- **Data Validation**: Edge cases, malformed inputs, boundary values
- **Business Logic**: Calculation accuracy, aggregation correctness
- **Error Handling**: Exception scenarios, recovery mechanisms

### Test Coverage
```bash
# Generate coverage report
poetry run pytest --cov=order_pipeline --cov-report=term-missing

# HTML report for detailed analysis
poetry run pytest --cov=order_pipeline --cov-report=html
```

## 🎓 Learning Outcomes

By exploring this project, you'll master:

1. **Data Quality Engineering**: Building robust validation systems
2. **Test-Driven Development**: Writing comprehensive test suites
3. **ETL Pipeline Design**: Modular, maintainable data workflows
4. **Production Readiness**: Handling real-world data challenges
5. **Python OOP**: Clean, extensible code architecture

## 🔧 Technical Stack

- **Python 3.8+** with type hints
- **pytest** for testing framework
- **pytest-cov** for coverage reporting
- **Poetry** for dependency management
- **Regular Expressions** for data cleaning
- **Dataclasses** for data modeling

## 📈 Business Impact

This pipeline ensures:
- **Accurate revenue reporting**
- **Reliable inventory planning**
- **Trustworthy business intelligence**
- **Data-driven decision making**
- **Customer satisfaction** through order accuracy

---

*Built with production-grade reliability for ShopLink's growing marketplace ecosystem.*