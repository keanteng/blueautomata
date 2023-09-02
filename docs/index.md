# 👋 Welcome to BlueAutomata 

## Introduction

Reporting is common in financial institution to ensure their operations are compliant and transparent. It also helps in decision-making to build trust, manage risk and informed decision. Workflows for reporting generally involves gathering raw data, cleaning of raw data and compiling raw data into their respective template using Microsoft Excel. For large organization, such procedure can be repetitive, lackluster and time-consuming. Oftentimes, mistakes could be made when dealing with large number of raw data during these processes due to human errors.

Thus, `blueautomata` is introduced as a package to ease the workflow for reporting in a company. This package aims **to automate the workflow of cleaning data, compiling data and preparing the data in reportable format on Excel by auto-calling the corresponding VBA function**.

``` mermaid
graph LR
A[Raw Data] --> B[Cleaning];
B[Cleaning] --> C[Compiling Cleaned Data];
C[Compiling Cleaned Data] --> D[Organize Data By Category]
D[Organize Data By Category] --> E[Create Template]
```

## Package Functions
1. Data Compilation with automated cleaning and automated correction on mislabelled data items
2. Exports large dataset into categorized files 
3. Auto template creation for categorized files (report template)

## Installation
- On Windows Terminal
```py
py -m pip install blueautomata
```

- Latest development version
  ```py
  pip install git+https://github.com/keanteng/blueautomata
  ```

## A Case Study

### Getting a New Job
In the year 2055, a guy named Travis Umbrella.[^1] become the Manager of LightSpeed Investment under the Department of Data Management. At that time, Travis is in his forties, and he studies Economics back in college. Previously, he works as the Manager under the Department of Investment. Well, he is an adventurous person and dare to try something new, so when opportunities come, he decided to advance in the field of managing data to get some new perspective in his work. 

In fact, Travis works in a weird company where the company makes investment in a weird way but with a high return. The company gives stocks to the employee so that they can sell in stock markets around the world. 

For each employee, they can only receive one type of stock like Google `GOOG`, but they are allowed to sell in a few markets such as New York Stock Exchange `NYSE` and Hong Kong Stock Exchange `HKSE`. Travis does not concern with whether the employee can make money or not since it is not part of his job.

Every month, Travis needs to submit a report for auditing where he needs to track down the employees stock holding type and the market that they sell their stock. Well, LightSpeed Investment is a fast-moving company, where employees come and go. So at the end of the month when Travis submits his report he has to make sure that employees that resigned should not be included in his report.

### Time For Action
For Travis to complete his report he would first need to get hold of the stocks' data that are traded by the firms' employees in worldwide stock markets. He then stored the transactions record for each stock market in an individual file. Since there is no well-build system for the data collection, each of the file looks different, some contains more columns than the other, some with missing information such as employees' name and some even contains wrong employee IDs and outdated information. 

Travis realizes that he would need some other data to validate his collected data, so he reached out to his friend, James Claude Diamond from the Human Resources Department to get the latest copy of the staff data where it contains the staff's assigned stocks and stock market that they can sell their stock. He also compiles a copy of checklist data by himself to match up the stock code and stock market code to their respective stock name and stock market name.

### Think Different
Travis is good at math and logical thinking, so he knows for resigned employees their names will not be in the staff dataset. In fact, what he will do is he will match the staff ID from the stock market data he collected with the staff data to obtain information as follows:

- The staff's name
- The staff's assigned stock
- The staff's status (resigned or not)

That approach, allows him to work quickly to compile the data he collects from the stock markets, what he will then, is to create file for each stock to see where they are traded around the world - of course with a nice looking template before submitting for audit review after the quarter ends.

Let's now see why Travis is able to work effectively in the next section 👉

[^1]: This story is a work of fiction. Names, characters, places, and incidents are the products of the author's imagination or are used fictitiously. Any resemblance to actual events, locales, or persons, living or dead, is entirely coincidental.

