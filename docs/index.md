# 👋 Welcome to BlueAutomata 

[![](https://img.shields.io/badge/project-website-brightgreen)](https://keanteng.github.io/blueautomata/)
![Static Badge](https://img.shields.io/badge/python-3.11-blue)
![Static Badge](https://img.shields.io/pypi/v/BlueAutomata)
![Static Badge](https://static.pepy.tech/badge/BlueAutomata)
![Static Badge](https://img.shields.io/badge/license-MIT-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


<figure markdown>
  ![Image title](images/../assets/logo.png){ width="200" }
  <figcaption>BlueAutomata</figcaption>
</figure>

## Introduction

Reporting is common in financial institution to ensure their operations are compliant and transparent. It also helps in decision-making to build trust, manage risk and informed decision. Workflows for reporting generally involves gathering raw data, cleaning of raw data and compiling raw data into their respective template using Microsoft Excel. For large organization, such procedure can be repetitive, lackluster and time-consuming. Oftentimes, mistakes could be made when dealing with large number of raw data during these processes due to human errors.

Thus, `blueautomata` is introduced as a package to provide a framework to ease the workflow for reporting in a company. This package aims **to automate the workflow of cleaning data, compiling data and preparing the data in reportable format on Excel by auto-calling the corresponding VBA function**.

``` mermaid
---
title: Package Algorithm
---
flowchart TD
    subgraph main
    A[Raw Data] --> B{Cleaning}
    C[Compiling Cleaned Data] --No--> D[Organize Data By Category]
    D[Organize Data By Category] --> E[Create Template]
    end

    subgraph sub1
    B[Cleaning] --> B1[User ID Matching]
    B1[User ID Matching] --> B2[User Name Reverse Lookup]
    B2[User Name Reverse Lookup] --> B3[Conditional Filterings]
    B3[Conditional Filterings] --> B4[Granularity Provisioning]
    B4[Granularity Provisioning] --> C[Compiling Cleaned Data]
    end

    subgraph sub2
    B[Cleaning] --If Required--> B11[Fuzzywuzzy Matching]
    B11[fuzzywuzzy Matching] --> B12[Update Data]
    B12[Update Data]--> B13[sub1 Process]
    B13[sub1 Process] --> C[Compiling Cleaning Data]
    end

    subgraph sub3
    B[Cleaning] --If Required--> B21[Output Foresight Reporting]
    end

    subgraph sub4
    C[Compiling Cleaned Data] --Yes--> C1[Data Labels Checker]
    C1[Data Labels Checker] --> D[Output Data By Category]
    end 
```

## Installation
- On Windows Terminal
```py title='Terminal'
py -m pip install BlueAutomata
```

- Latest development version
```py title='Terminal'
pip install git+https://github.com/keanteng/BlueAutomata
```

## Package Functions
1. Data Compilation 
      1. Data cleaning such as renaming columns and conditional filtering
      2. Data lookup and matching support
         1. Auto reverse lookup to update mislabelled cells
      3. Auto [`fuzzywuzzy`](https://pypi.org/project/fuzzywuzzy/) matching and update for similar data
2. Exports large dataset into categorized files 
3. Template creation for categorized files (report template) by calling written macros on Excel
