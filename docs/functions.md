# Package Functions 📦

## Introduction
Before using `blueautomata`, you must get 4 types of parameters for the function to make reference:

- **Folder path**: 
    - The folder storing all the raw data that you want to compile
- **References file path**: 
    - File containing all the company staff details
    - File containing list of abbreviations and their full name
- **Search key**:
    - The name key that you used to identify the file category in your raw data folder
- **Search code**: 
    - The type of file characteristics that you stored in your raw data folder

### Search Code Reference

In general, there are 7 types of search code:

| Code |  Characteristics |
| :--- | -----------------------------------------------------------------------: |
| 1    |                      Excel file that can be used directly without filter |
| 2    |        Excel file that can be used directly with one filter on column `` |
| 3    |        Excel file that can be used directly with one filter on column `` |
| 4    |        Excel file that can be used directly with one filter on column `` |
| 5    |        Excel file that can be used directly with one filter on column `` |
| 6    |       Excel file that can be used directly with two filters on column `` |
| 10   | Excel file with multiple sheets that can be used directly without filter |

## 1. Data Compilation
`BlueAutomata` is a class that is build for data compilation workflow, the class takes in 5 parameters in the form of `path` and list.

```py
BlueAutomata(    
    folder_path = 'FOLDERPATH',
    checklist = 'FILEPATH,
    staff_data = 'FILEPATH',
    name_key = [],
    name_code = [],
)
```

There is one built-in function inside the class: `automata_execution`, that uses the parameters from `BlueAutomata` to compile the raw data files stored in your specified `folder_path` and return the compiled data as a dataframe

```py
automata_execution(self)
```

!!! info
    Read this to learn more on the data compilation workflow

### 1.1 Usage Example
Read the first five rows of the compiled data

```py title='Example'
data = BlueAutomata(
    folder_path = 'data/fakesystem',
    checklist = 'data/checklist.xlsx',
    staff_data = 'data/fakedata.xlsx',
    name_key = ['NASDAQ', 'KLSE', 'NYSE'],
    name_code = [1, 1, 1]
)

df = data.automata_execution
df.head()
```

!!! tips
    Go to this notebook section to see the code in action using Jupyter notebook

## 2. Categorized File Export
To quickly export the large compiled dataset into individual Excel files for each category, you can work with the `BatchExport` class that takes two input parameters:

```py
BatchExport(
    destination = 'PATH',
    masterlist = 'PATH'
)
```

You tell the class where your `masterlist` or your compiled data is stored and where your want to store the output from the function. You can then call the function `batch_export` to start the operation:

```py
batch_export(self)
```

### 2.1 Usage Example
Export `masterlist` into individuals Excel files by category:

```py title='Example'
df = BatchExport(
    destination = 'data/fakedept',
    masterlist = 'data/automataoutput.xlsx',
)

df.batch_export
```

!!! tips
    Go to this notebook section to see the code in action using Jupyter notebook

## 3. Using VBA
If you want to apply some VBA functions on the exported Excel files, you can call the class `automate_vba` that takes two parameters `filepath` and `macro`.

- `filepath` is the path towards as macro-enabled notebook where your macro modules are stored.
- `macro` is the name of the macro that you want to apply on the selected files

```py
automate_vba(
    filepath = 'MACRO_ENABLED_WORKBOOK_FILEPATH',
    macro = 'YOURMACRONAME'
)
```

!!! warning
    In this function, it requires the VBA itself to allow user to select file by popping up a file explorer window, thus the function is meant to call the VBA function, but is not able to know which files that the macro will be executed on.

    To add file selection function to your VBA program, see this.

Inside `automate_vba` class, there is a `templatize` function that will call the macro code from your Excel workbook:

```py
templatetize(self)
```

### 3.1 Usage Example
Executing the macro from your Excel workbook:

```py title='Example'
start = automate_vba(
    filepath = 'vbanew.xlsm',
    macro = 'vbanew.xlsm!Module1.kt_template'
)

start.templatetize()
```

!!! tips
    Go to this notebook section to see the code in action using Jupyter notebook

## Reporting Tools (TBA)