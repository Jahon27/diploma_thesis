# Generating Source Code from UML Diagrams

## Project Description

This project focuses on automated source code generation from UML diagrams.  
The aim of the thesis is to analyze possibilities of model-driven code generation and compare classical parser-based approaches with AI-assisted generation using Large Language Models (LLMs).

The implemented prototype processes UML diagrams exported from draw.io XML files and generates Python source code from:
- UML class diagrams
- UML sequence diagrams

The project combines:
- procedural parsing techniques,
- grammar-based parsing using ANTLR,
- intermediate textual representations,
- and future AI-assisted approaches for UML understanding and code generation.

---

# Thesis Goals

- Analyze existing approaches for UML-based source code generation
- Study Model-Driven Development (MDD)
- Investigate parser generators and ANTLR
- Study AI-assisted code generation approaches
- Implement UML class diagram extraction
- Implement UML sequence diagram parsing
- Design intermediate SQD language
- Generate Python source code from UML diagrams
- Compare parser-based and AI-based approaches

---

# Current Progress

Implemented:
- UML class diagram XML extraction
- UML sequence diagram extraction
- Intermediate SQD language
- ANTLR grammar for sequence diagrams
- Visitor-based semantic analysis
- Python source code generation
- Initial support for:
  - method calls
  - return messages
  - self-calls
  - alt fragments
  - loop fragments

In Progress:
- Extended semantic analysis
- More advanced UML fragment support
- AI-assisted code generation experiments

---

# Weekly Progress Timeline

## Week 1 (20.02 – 26.02)
- Initial research on diploma thesis topic
- Study of UML diagrams and Model-Driven Development
- Search for scientific papers related to code generation
- Analysis of existing UML-to-code approaches

## Week 2 (27.02 – 05.03)
- Research on parser generators and ANTLR
- Study of grammar-based parsing techniques
- Analysis of UML sequence and class diagrams
- Investigation of draw.io XML structure

## Week 3 (06.03 – 12.03)
- Selection and study of scientific papers
- Research on AI-assisted code generation
- Investigation of ChatGPT and LLM-based approaches
- Comparison of parser-based and AI-based generation concepts

## Week 4 (13.03 – 19.03)
- Search and analysis of UML datasets
- Investigation of synthetic UML datasets
- Selection of datasets for future experiments and AI training

## Week 5 (20.03 – 26.03)
- Design of overall project architecture
- Definition of UML processing pipeline
- Preparation of Python project structure
- Setup of ANTLR environment

## Week 6 (27.03 – 02.04)
- Implementation of UML class diagram extractor
- XML parsing of draw.io class diagrams
- Extraction of classes, attributes, methods, and relationships

## Week 7 (03.04 – 09.04)
- Development of internal semantic model
- Initial Python code generation from UML class diagrams
- Testing on sample UML diagrams

## Week 8 (10.04 – 16.04)
- Design of intermediate SQD language
- Development of sequence diagram extraction
- Transformation of UML sequence diagrams into SQD format

## Week 9 (17.04 – 23.04)
- Creation of ANTLR grammar for SQD language
- Generation of lexer and parser using ANTLR4
- Implementation of visitor-based semantic analysis

## Week 10 (24.04 – 30.04)
- Development of sequence diagram code generator
- Generation of Python method calls from parsed sequence models
- Integration of parser pipeline components

## Week 11 (01.05 – 08.05)
- Extension of sequence diagram support
- Initial implementation of:
  - alt fragments
  - loop fragments
- Creation of experimental UML examples
- Preparation of thesis presentation and documentation

---

# Planned Tasks

- Improve support for advanced UML sequence fragments
- Extend semantic validation
- Improve generated source code quality
- Add support for additional UML diagram types
- Compare generated code with LLM-based approaches
- Investigate AI model training using UML datasets
- Evaluate the system on larger UML datasets

---

# Technologies Used

- Python
- ANTLR4
- draw.io
- UML
- PlantUML
- XML
- Model-Driven Development (MDD)
- Large Language Models (LLMs)

---

# Project Structure

```text
src/
├── antlr/
├── extractors/
├── generators/
├── models/
├── outputs/
├── diagrams/
└── main.py