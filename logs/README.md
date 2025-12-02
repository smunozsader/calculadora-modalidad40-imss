# 📊 Deployment Logs

This directory contains deployment and runtime logs for the Calculadora Modalidad 40 IMSS project.

## 📁 Log Structure

### Deployment Logs
- `railway-deploy.log` - Railway deployment logs and build output
- `docker-build.log` - Local Docker build logs  
- `error.log` - Critical deployment errors and failures

### Runtime Logs  
- `app.log` - Flask application runtime logs
- `calculator.log` - Pension calculation processing logs
- `pdf-generation.log` - PDF report generation logs
- `access.log` - HTTP request access logs

## 🔍 Log Monitoring

### Key Events to Monitor
- ✅ Successful deployments and builds
- ❌ Calculation errors or edge cases
- 📄 PDF generation failures
- 🚨 Security-related access attempts
- ⚡ Performance bottlenecks

### Log Rotation
Logs are automatically rotated to prevent disk space issues:
- Daily rotation for high-volume logs
- 7-day retention for debug logs  
- 30-day retention for error logs
- Permanent retention for deployment logs

## 📈 Analytics Tracking

### User Interaction Logs
- Calculator usage patterns
- Most common calculation scenarios
- Error rates by functionality
- Geographic usage distribution (if available)

### Performance Metrics
- Response time measurements  
- Memory usage patterns
- Database query performance
- PDF generation timing

## 🛠️ Troubleshooting

### Common Issues

**PDF Generation Failures**
```bash
# Check PDF logs
tail -f logs/pdf-generation.log

# Look for ReportLab errors
grep "ReportLab" logs/error.log
```

**Calculation Errors**
```bash  
# Monitor calculator processing
tail -f logs/calculator.log

# Check for Ley 97 validation issues
grep "elegibilidad" logs/app.log
```

**Deployment Issues**
```bash
# Review Railway deployment
cat logs/railway-deploy.log

# Check Docker build problems
cat logs/docker-build.log
```

## 📊 Log Analysis

### Regular Maintenance
- Weekly review of error patterns
- Monthly performance analysis  
- Quarterly usage trend reporting
- Annual log archival process

### Alerting Thresholds
- Error rate > 5% triggers investigation
- Response time > 3s requires optimization
- PDF failure rate > 2% needs attention
- Memory usage > 80% triggers scaling review

## 🔒 Security Considerations

### Sensitive Data
- No personal data (CURP, names) logged
- IP addresses anonymized after 24 hours
- Calculation results not permanently stored
- PII scrubbed from error messages

### Access Control
- Logs accessible only to development team
- Production log access requires authorization
- Log rotation removes old sensitive data
- Regular security audits of log content

## 📝 Log Format Standards

All logs follow structured format:
```
[TIMESTAMP] [LEVEL] [COMPONENT] [ACTION] - [MESSAGE]
```

Example:
```
[2025-01-10 14:30:25] [INFO] [Calculator] [Ley73Calculation] - Processed calculation for birth year 1964, retirement age 65
[2025-01-10 14:30:26] [ERROR] [PDFGenerator] [ReportGeneration] - Failed to generate PDF: Missing field total_años
```