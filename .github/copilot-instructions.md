# Copilot Instructions - IMSS Semanas Cotizadas Project

## Project Overview

This is a personal documentation and tracking project for IMSS (Instituto Mexicano del Seguro Social) Modalidad 40 requirements and contribution weeks analysis. The project focuses on documenting eligibility requirements, tracking contribution history, and managing Mexican social security documentation.

## Key Context & Domain Knowledge

### IMSS Terminology
- **Modalidad 40**: Voluntary Continuation in the Mandatory Regime - allows inactive workers to continue contributing
- **Semanas Cotizadas**: Contribution weeks - the fundamental unit for pension calculations
- **Ley 73**: 1973 Social Security Law - determines pension calculation method
- **CURP**: Unique Population Registry Code (Mexican national ID)
- **NSS**: Social Security Number (IMSS-specific identifier)
- **UMA**: Unit of Measure and Update (used for salary caps and calculations)

### Critical Requirements Pattern
When documenting IMSS requirements, always structure as:
1. **Eligibility criteria** (with specific time limits and thresholds)
2. **Required documentation** (originals vs copies, validity periods)
3. **Additional considerations** (payment options, consequences of interruption)

## File Patterns & Conventions

### Documentation Structure
- Use `.md` files for requirements and procedures
- Include both Spanish terms and English explanations in parentheses
- Bold key requirements and thresholds (e.g., **52 semanas cotizadas**, **5 años**)
- Use bullet points for requirement lists, numbered lists for procedures

### PDF Handling
- Contribution reports are typically named: `[CURP] reporteSemanasCotizadas.pdf`
- These contain official IMSS contribution history data
- Always preserve original filenames for traceability

## Project-Specific Patterns

### Time Sensitivity
- All IMSS procedures have strict time limits (typically 5 years from last employment)
- When documenting timelines, always specify the reference date clearly
- Current context: Analysis performed in 2025 for historical contribution periods

### Bilingual Documentation
- Primary language: Spanish (official IMSS language)
- Include English clarifications for technical terms
- Maintain official IMSS terminology even when translating

## Common Tasks

When updating requirements documentation:
1. Verify current IMSS regulations (they change frequently)
2. Include specific threshold numbers (weeks, years, salary multiples)
3. Cross-reference with actual contribution reports when available
4. Maintain clear distinction between requirements vs. recommendations

When working with contribution data:
- Preserve exact dates and periods from official reports
- Calculate gaps in coverage periods
- Track eligibility windows for different modalities

## Key Files

- `Requisitos Modalidad 40.md`: Core eligibility requirements for voluntary contributions
- `MUMS640728UQ0 reporteSemanasCotizadas.pdf`: Official contribution history report
- Directory structure follows year-based organization for pension planning periods