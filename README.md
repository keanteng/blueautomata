# BlueAutomata ⚙️ <!-- omit in toc -->

[![](https://img.shields.io/badge/project-website-brightgreen)](https://keanteng.github.io/blueautomata/)
![Static Badge](https://img.shields.io/badge/license-MIT-blue)
![Static Badge](https://img.shields.io/badge/python-3.11-blue)
![Static Badge](https://img.shields.io/pypi/v/blueautomata)
![Static Badge](https://static.pepy.tech/badge/blueautomata)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**A Python package for reporting workflow automation**
- PyPI: https://pypi.org/project/blueautomata/
- Documentation: https://keanteng.github.io/blueautomata/
- MIT Licensed

**Table of Contents:**
- [Introduction](#introduction)
- [Organization Benefits](#organization-benefits)
- [Functionality](#functionality)
- [Installation](#installation)

## Introduction

Reporting is common in financial institution to ensure their operations are compliant and transparent. It also helps in decision-making to build trust, manage risk and informed decision. Workflows for reporting generally involves gathering raw data, cleaning of raw data and compiling raw data into their respective template using Microsoft Excel. For large organization, such procedure can be repetitive, lackluster and time-consuming. Oftentimes, mistakes could be made when dealing with large number of raw data during these processes due to human errors. 

Thus, `blueautomata` is introduced as a package to ease the workflow for reporting in a company. This package aims to automate the workflow of cleaning data, compiling data and preparing the data in reportable format on Excel by auto-calling the corresponding VBA function. 

## Organization Benefits
`blueautomata` is good for organization usage because of:

- **Modularity**
  - Easier to manage and maintain, allow developers to create components that can be used in different reporting scenarios, saving time and effort.
- **Version Control**
  - Track changes and updates to the codebase over time. This is crucial for package's compatibility and ensure the older version can continue to be used if necessary. 
- **Distribution**
  - Packaging allow `blueautomata` to be distributed, updated and maintained easily firm wide

## Functionality
1. Data Compilation 
   - Data cleaning such as renaming columns and conditional filtering
   - Data lookup and matching support
   - Auto reverse lookup to update mislabelled cells
   - Auto [`fuzzywuzzy`](https://pypi.org/project/fuzzywuzzy/) matching for similar data (using [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance) ratio)
2. Exports large dataset into categorized files 
3. Template creation for categorized files (report template) by calling written macros on Excel

## Installation

How to install this package:

```py
pip install blueautomata
```

To install the development version from GitHub using Git, run the following command in your terminal:

```py
pip install git+https://github.com/keanteng/blueautomata
```

Internship Project © 2023
