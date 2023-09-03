# BlueAutomata ⚙️ <!-- omit in toc -->

[![](https://img.shields.io/badge/project-website-brightgreen)](https://keanteng.github.io/blueautomata/)
![Static Badge](https://img.shields.io/badge/license-MIT-blue)
![Static Badge](https://img.shields.io/badge/python-3.11-blue)

**A Python package for reporting workflow automation**
- PyPI: https://pypi.org/project/BlueAutomata/
- Documentation https://keanteng.github.io/blueautomata/
- MIT License

**Table of Contents:**
- [Introduction](#introduction)
- [Functionality](#functionality)
- [Installation](#installation)

## Introduction

Reporting is common in financial institution to ensure their operations are compliant and transparent. It also helps in decision-making to build trust, manage risk and informed decision Workflows for reporting generally involves gathering raw data, cleaning of raw data and compiling raw data into their respective template using Microsoft Excel. For large organization, such procedure can be repetitive, lackluster and time-consuming. Oftentimes, mistakes could be made when dealing with large number of raw data during these processes due to human errors. 

Thus, `blueautomata` is introduced as a package to ease the workflow for reporting in a company. This package aims to automate the workflow of cleaning data, compiling data and preparing the data in reportable format on Excel by auto-calling the corresponding VBA function. 

`blueautomata` is good because of:
- **Modularity**
  - Easier to manage and maintain, allow developers to create components that can be used in different reporting scenarios, saving time and effort.
- **Version Control**
  - Track changes and updates to the codebase over time. This is crucial for package's compatibility and ensure the older version can continue to be used if necessary. 
- **Distribution**
  - Packaging allow `blueautomata` to be distributed, updated and maintained easily firm wide

## Functionality
- Effective data cleaning with a compiled output
  - Auto correction and referencing for wrong data content
- Miscellaneous data items reporting
- Fast exporting of large dataset into individual Excel sheets filtered by a Firm's Department
- Automatic template creation on exported Excel sheets

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
