# Package Functions 📦

## 0. Introduction
Before using `blueautomata`, you must get 4 types of parameters for the function to make reference:

=== "Parameters"
    - **Folder path**: 
        - The folder storing all the raw data that you want to compile
    - **References file path**: 
        - File containing all the company staff details
        - File containing list of abbreviations and their full name
    - **Search key**:
        - The name key that you used to identify the file category in your raw data folder
    - **Search code**: 
        - The type of file characteristics that you stored in your raw data folder

### 0.1 Search Code Reference

In general, there are 3 types of search code:

| Code |  Characteristics |
| :--- | -----------------------------------------------------------------------: |
| 1    |                      Excel file that can be used directly with or without filter[^1] |
| 6    |       Excel file that can be used directly with two filters on column `RBC Access` and `IFAS Access` |
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
    Read [this](https://keanteng.github.io/blueautomata/concepts/) to learn more on the data compilation workflow

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
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/01BlueAutomata/) notebook section to see the code in action using Jupyter notebook

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
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/05BatchExport/) notebook section to see the code in action using Jupyter notebook

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

    To add file selection function to your VBA program, see [this](https://keanteng.github.io/blueautomata/vba_integrate/).

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
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/06AutomateVBA/) notebook section to see the code in action using Jupyter notebook

## 4. Output Foresight
This package also provides function for you to take a preview at the output with a summary report based on your input parameter, for example:

=== "Output Foresight"
    System | Matched IDs | Unmatched IDs | Total IDs
    :-- | -- | -- | --:
    GOOG | 123 | 3 | 126
    NFLX | 24 | 5 | 29
    SPOT | 45 | 0 | 45

From the table, you can see the number of `Matched IDs` that will be compiled when you execute the `BlueAutomata` function. To produce the output report, you can call the class `AutomataReport` that takes in 5 parameters:

```py
AutomataReport(
    folder_path = 'PATH',
    checklist = 'PATH',
    staff_data = 'PATH,
    name_key = [],
    name_code = [],
)
```

Inside the `Automata Report` class, there is a function `automata_report_summary` that will produce the output summary report:

```py
automata_report_summary(self)
```

If you would like to know what exactly are the unmatched items, you can simply call:

```py
automata_report_unmatch(self)
```

### 4.1 Usage Example
Producing the output summary report

```py title='Example'
df = AutomataReport(
    folder_path = 'data/fakesystem',
    checklist = 'data/checklist.xlsx',
    staff_data = 'data/fake_hr_data.xlsx',
    name_key = ['NASDAQ', 'KLSE', 'NYSE', 'TSE'],
    name_code = [1,1,1,1],
)

df.automata_report_summary()
```

Get a list of the unmatched items

```py title='Example'
df = AutomataReport(
    folder_path = 'data/fakesystem',
    checklist = 'data/checklist.xlsx',
    staff_data = 'data/fake_hr_data.xlsx',
    name_key = ['NASDAQ', 'KLSE', 'NYSE', 'TSE'],
    name_code = [1,1,1,1],
)

df.automata_report_unmatch()
```

!!! tips
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/02AutomataReport/) notebook section to see the code in action using Jupyter notebook

## 5. Inconsistent Data Entry
A special class named `Inconsistency` is created to deal with Excel file that:

- Does not have a `User ID` column
- Have a `Name` column, but the names are written in format different from the staff data. Even for files with only `Name` column and all the names are correct but no `User ID`, this class is still able to compile the data.
    - For example: "Davida Faris Hill" and "faris Hill Davida" are the same person

This class takes in 4 parameters, as follows:

```py
Inconsistency(
    filepath = 'PATH',
    staff_data = 'PATH',
    checklist = 'PATH',
    sheet_number = 1
)
```

Inside the `Inconsistency` class there is a function called `fix_inconsistency` that will automatically rectify the wrong names and update the dataset with information such as `User ID`, `Department`, `Dept Code`, `System1` and `Cube`

```py
fix_inconsistency(self)
```

Of course, there will be time all the wrong names could not be fixed, you can cal the `inconsistency_report` function to extract out the name that could not be fixed:

```py
inconsistency_report(self)
```

### 5.1 Usage Example
- Compiling data

```py title='Example'
test = Inconsistency(
    filepath = 'PATH',
    staff_data = 'PATH',
    checklist = 'PATH',
    sheet_number = 1
)

df = test.fix_inconsistency()
```

- Get summary for unmatched staff names

```py title='Example'
test = Inconsistency(
    filepath = 'PATH',
    staff_data = 'PATH',
    checklist = 'PATH',
    sheet_number = 1
)

df = test.inconsistency_report()
```

!!! tips
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/03Inconsistency/) notebook section to see the code in action using Jupyter notebook

## 6. System & Cube Checking
This package also contains a class called `SystemCubeChecker` to update the wrongly assigned system and cube. In other words, it will update the entries where the cube names are put as system names by moving the cube names to the cube column and re-assigning a system name to them. The class takes in 3 parameters:

```py
SystemCubeChecker(
    masterlistpath = 'PATH',
    system_to_check = [],
    cube_to_assign = [],
)
```

You can use the `system_cube_update` function to perform the reassignment:

```py
system_cube_update(self)
```

### 6.1 Usage Example
Here is how you can perform the reassignment:

```py title='Example'
test = SystemCubeChecker(
    masterlistpath = 'C:/Users/limzi/OneDrive/Desktop',
    system_to_check= ['GOOG', 'NFLX'],
    cube_to_assign='KLSE'
)

test.system_cube_update()
```

!!! tips
    Go to [this](https://keanteng.github.io/blueautomata/notebooks/04SystemCube/) notebook section to see the code in action using Jupyter notebook

[^1]: For with filter Excel file, the filter only applies to column with the following names: `status` and `Disable Flag *`