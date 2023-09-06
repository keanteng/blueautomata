"""
Function to fix inconsistencies in the data
The function is built specifically for the files that only contains the following columns:
- Name
And no other information can provide matching for you to obtain further information about the user.

Since unique user ID is not available and no other information are available, 
we use the name to identify the user. There are often many names that are similar to each other, for 
example, "John Smith" and "John Smith Jr." are two same people but with different names.

Funtion build specifically for file that onlt can refer with name and none other information.
"""

import fuzzywuzzy
from fuzzywuzzy import process
import warnings
import pandas as pd


class Inconsistency:
    def __init__(self, filepath, staff_data, checklist, sheet_number):
        self.filepath = filepath
        self.staff_data = staff_data
        self.checklist = checklist
        self.sheet_number = sheet_number

    def fix_inconsistency(self):
        ###################################################
        def replace_matches_in_column(df, column, string_to_match, min_ratio=88):
            # get a list of unique strings
            strings = df[column].unique()

            # get the top 10 closest matches to our input string
            matches = fuzzywuzzy.process.extract(
                string_to_match,
                strings,
                limit=10,
                scorer=fuzzywuzzy.fuzz.token_sort_ratio,
            )

            # only get matches with a ratio > 88
            close_matches = [
                matches[0] for matches in matches if matches[1] >= min_ratio
            ]

            # get the rows of all the close matches in our dataframe
            rows_with_matches = df[column].isin(close_matches)

            # replace all rows with close matches with the input matches
            df.loc[rows_with_matches, column] = string_to_match

        ###################################################

        warnings.filterwarnings("ignore")

        # read file and select the sheet
        df = pd.ExcelFile(self.filepath)
        sheetName = df.sheet_names
        df = pd.read_excel(self.filepath, sheet_name=sheetName[self.sheet_number])

        # read staff data
        staff_sheet = pd.ExcelFile(self.staff_data)
        staff_sheet_col = staff_sheet.sheet_names
        staff = pd.read_excel(staff_sheet, sheet_name=staff_sheet_col[1])

        # read checklist
        ref_code = pd.read_excel(self.checklist)

        # preparing data
        if "User Cube" in df.columns:
            df["Cube"] = df["User Cube"]

        df["Name"] = df["Name"].str.strip()
        df["Name"] = df["Name"].str.lower()

        df = df[["Name", "Cube"]]
        df = df.drop_duplicates(subset=["Name", "Cube"], keep="first")
        df["Source"] = "Original"

        temp = pd.DataFrame(staff[["Name"]])
        temp = temp.drop_duplicates(subset=["Name"], keep="first")
        temp["Source"] = "Staff"

        temp["Name"] = temp["Name"].str.strip()
        temp["Name"] = temp["Name"].str.lower()

        # combine the data
        df = pd.concat([temp, df], ignore_index=True)

        # fix the inconsistency
        # take about 10 minutes to run
        # change to len(df) to run the whole file
        for i in range(0, len(df)):
            replace_matches_in_column(df, "Name", df["Name"][i])

        # data compilation
        df = df[df["Source"] == "Original"]
        temp["LAN ID"] = staff["LAN ID"]
        temp = temp.drop_duplicates(subset=["Name"], keep="first")
        temp.reset_index(drop=True, inplace=True)

        df["User ID"] = df["Name"].map(temp.set_index("Name")["LAN ID"])
        df["Name"] = df["User ID"].map(staff.set_index("LAN ID")["Name"])
        df["Department"] = df["User ID"].map(staff.set_index("LAN ID")["Department"])
        df["Dept"] = df["Department"].map(ref_code.set_index("Department")["Dept Code"])
        df["System1"] = sheetName[self.sheet_number]

        df = df[["Department", "Dept", "User ID", "Name", "System1", "Cube"]]
        df = df.dropna(subset=["User ID"])
        df.reset_index(drop=True, inplace=True)
        df = df.drop_duplicates(subset=["User ID", "System1", "Cube"], keep="first")

        return df
        # print(df.tail())
        # print(len(df))
        # df.to_excel('Inconsistency.xlsx', index=False)


# test = Inconsistency(
# filepath='rawdata/RBCIFAS.xlsx',
# staff_data='rawdata/stafflist.xlsx',
# checklist='rawdata/Department Checklist.xlsx',
# sheet_number=1
# )
# test.fix_inconsistency()
