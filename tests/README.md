# 🧪 Test Suite

This directory contains all test files and utilities for the Calculadora Modalidad 40 IMSS project.

## 📁 Test Files

### Core Tests
- `test_calculadora_elegibilidad.py` - Tests for Ley 97 eligibility validation
- `test_calculadora_ley73.py` - Tests for pension calculation logic  
- `test_calculadora_modalidad40.py` - Tests for Modalidad 40 specific calculations
- `test_pdf_generation.py` - Tests for PDF report generation

### Utilities
- `fix_js_scope.py` - JavaScript debugging and scope analysis utility

## 🚀 Running Tests

### All Tests
```bash
# From project root
python -m pytest tests/ -v
```

### Specific Test Categories
```bash
# Elegibilidad tests
python -m pytest tests/test_calculadora_elegibilidad.py -v

# Ley 73 calculation tests  
python -m pytest tests/test_calculadora_ley73.py -v

# Modalidad 40 tests
python -m pytest tests/test_calculadora_modalidad40.py -v

# PDF generation tests
python -m pytest tests/test_pdf_generation.py -v
```

### JavaScript Debugging
```bash
# Analyze JavaScript scope issues
python tests/fix_js_scope.py
```

## 🎯 Test Coverage Areas

### Elegibilidad Validation
- ✅ Ley 97 cutoff date (July 1, 1997) validation
- ✅ CURP format validation
- ✅ Birth date calculations
- ✅ Contribution start date logic

### Pension Calculations
- ✅ Ley 73 formula accuracy
- ✅ UMA progression calculations
- ✅ Monthly payment timelines
- ✅ Retirement age scenarios

### PDF Generation  
- ✅ Report template rendering
- ✅ Data field mapping
- ✅ Error handling for missing data
- ✅ Multiple output formats

### Integration Tests
- ✅ Flask route testing
- ✅ Frontend-backend communication
- ✅ Error propagation handling

## 📊 Test Data

All tests use realistic Mexican pension system data:
- Real CURP formats and validation rules
- Actual UMA progression values (2025-2035)
- Valid birth year ranges (1960-1975)
- Authentic Modalidad 40 contribution scenarios

## 🔧 Test Configuration

### Dependencies
Tests require all main project dependencies plus:
- `pytest` - Test framework
- `pytest-flask` - Flask-specific testing utilities

### Test Environment
- Uses isolated test database/calculations
- Mock external service calls
- Validates both positive and negative scenarios

## 📝 Adding New Tests

When adding functionality:
1. Create corresponding test in appropriate file
2. Follow existing naming conventions
3. Include both success and failure scenarios  
4. Update this README if adding new test categories