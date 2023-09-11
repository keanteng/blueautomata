"""
This class will be used to automate the report generation process
- The class will take in the folder path, checklist, staff data, name key and name code
- The class will read the excel files in the folder path
- The class will read the checklist and staff data
- The class will read the name key and name code
- The class will clean the data and generate the report where it will shows the
number of data that is available in the checklist and the number of data that is
not available in the checklist
"""

import os
import pandas as pd
import warnings


class AutomataReport:
    def __init__(self, folder_path, checklist, staff_data, name_key, name_code):
        self.folder_path = folder_path
        self.checklist = checklist
        self.staff_data = staff_data
        self.name_key = name_key
        self.name_code = name_code

    #################################################### start function
    def automata_report_unmatch(self):
        ##############################################
        def report_unmatch(dataframe, staff_data, checklist, key):
            warnings.filterwarnings("ignore")
            ref_data = pd.ExcelFile(checklist)
            ref_cols = ref_data.sheet_names
            # ref_code = pd.read_excel(checklist, sheet_name = ref_cols[0])
            ref_cube = pd.read_excel(checklist, sheet_name=ref_cols[1])
            # keyname is sheet name
            staff_sheet = pd.ExcelFile(staff_data)
            staff_sheet_col = staff_sheet.sheet_names
            staff = pd.read_excel(staff_sheet, sheet_name=staff_sheet_col[1])

            if key == 1:
                # read the necessary data
                df = pd.read_excel(dataframe)

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                # clean user ID for white space and lower case
                # check if the user ID is in the staff list
                df["User ID"] = df["User ID"].str.lower()
                df["User ID"] = df["User ID"].str.strip()

                # conditional filtering
                if "Status" in df.columns:
                    df = df[df["Status"] == "*ENABLED"]
                if "Disable Flag *" in df.columns:
                    df = df[df["Disable Flag *"] == "N"]

                df["check"] = df["User ID"].isin(staff["LAN ID"])

                # auto fix wrong user ID
                # We will check the availability of the Name column
                # there are two persons with the same name
                if "Name" in df:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    dfnew = df[df["check"] == False]
                    dfnew["User ID"] = dfnew["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    dfnew["check"] = dfnew["User ID"].isin(staff["LAN ID"])
                    dfnew = dfnew[dfnew["check"] == True]
                    df = pd.concat([df, dfnew], ignore_index=True)

                df["System1"] = dataframe.sheet_names[0].upper()

                # only statsmartcube need unique filtering
                if "STATSMART CUBE" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["STATSMART CUBE"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )

                    df = df.drop_duplicates(
                        subset=["User ID", "Cube", "System1"], keep="first"
                    )
                if "role code" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["role code"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )

                    df = df.drop_duplicates(
                        subset=["User ID", "Cube", "System1"], keep="first"
                    )

                if "Name" in df:
                    df["Name"] = df["Name"].astype(str)
                else:
                    df["Name"] = None

                # adding details to the data
                # match_case = len(df[df["check"] == True])
                not_match_case = df[df["check"] == False]
                report = pd.DataFrame(not_match_case)
                report = report[["User ID", "check", "System1", "Name"]]

            elif key == 6:
                # read the necessary data
                df = pd.read_excel(dataframe)

                # create two dataframes for based on the access
                df1 = df[df["RBC Access"] == "Yes"]
                df2 = df[df["IFAS Access"] == "Yes"]

                # clean up user ID
                df1["User ID"] = df1["User ID"].str.lower()
                df1["User ID"] = df1["User ID"].str.strip()
                df2["User ID"] = df2["User ID"].str.lower()
                df2["User ID"] = df2["User ID"].str.strip()

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                # check if the user ID is in the staff list
                df1["check"] = df1["User ID"].isin(staff["LAN ID"])
                df2["check"] = df2["User ID"].isin(staff["LAN ID"])

                # auto fix wrong user ID
                # We will check the availability of the Name column
                # there are two persons with the same name
                if "Name" in df1:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    df1new = df1[df1["check"] == False]
                    df1new["User ID"] = df1new["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    df1new["check"] = df1new["User ID"].isin(staff["LAN ID"])
                    df1new = df1new[df1new["check"] == True]
                    df1 = pd.concat([df1, df1new], ignore_index=True)

                if "Name" in df2:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    df2new = df2[df2["check"] == False]
                    df2new["User ID"] = df2new["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    df2new["check"] = df2new["User ID"].isin(staff["LAN ID"])
                    df2new = df2new[df2new["check"] == True]
                    df2 = pd.concat([df2, df2new], ignore_index=True)

                df1["System1"] = "RBC"
                df2["System1"] = "IFAS"

                df1 = df1.drop_duplicates(subset=["User ID", "System1"], keep="first")
                df2 = df2.drop_duplicates(subset=["User ID", "System1"], keep="first")

                if "Name" in df1:
                    df1["Name"] = df1["Name"].astype(str)
                else:
                    df1["Name"] = None

                if "Name" in df2:
                    df2["Name"] = df2["Name"].astype(str)
                else:
                    df2["Name"] = None

                # adding details to the data
                # match_case1 = len(df1[df1["check"] == True])
                not_match_case1 = df1[df1["check"] == False]
                report1 = pd.DataFrame(not_match_case1)

                # match_case2 = len(df2[df2["check"] == True])
                not_match_case2 = df2[df2["check"] == False]
                report2 = pd.DataFrame(not_match_case2)
                report = pd.concat([report1, report2], ignore_index=True)
                report = report[["User ID", "check", "System1", "Name"]]

            else:
                # read the necessary data
                sheetName = dataframe.sheet_names
                # dfs = []
                reports = []

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                for i in range(len(sheetName)):
                    # read the sheet
                    df = pd.read_excel(dataframe, sheet_name=sheetName[i])
                    # due to the nature of the data, we need to only select the User ID
                    # df = pd.DataFrame(df['User ID'])
                    # df = df[df["User ID"]]
                    # remove empty rows
                    # df = df.dropna(axis=0)

                    # clean up user ID
                    df["User ID"] = df["User ID"].str.lower()
                    df["User ID"] = df["User ID"].str.strip()

                    # check if the user ID is in the staff list
                    df["check"] = df["User ID"].isin(staff["LAN ID"])

                    # auto fix wrong user ID
                    # We will check the availability of the Name column
                    # there are two persons with the same name
                    if "Name" in df:
                        unique_name = pd.DataFrame(
                            staff["Name"].drop_duplicates(keep="first")
                        )
                        unique_name["LAN ID"] = staff["LAN ID"]
                        dfnew = df[df["check"] == False]
                        dfnew["User ID"] = dfnew["Name"].map(
                            unique_name.set_index("Name")["LAN ID"]
                        )

                        # update the the check column
                        # now the false positive should be corrected
                        dfnew["check"] = dfnew["User ID"].isin(staff["LAN ID"])
                        dfnew = dfnew[dfnew["check"] == True]
                        df = pd.concat([df, dfnew], ignore_index=True)

                    df["System1"] = sheetName[i].upper()
                    df = df.drop_duplicates(subset=["User ID", "System1"], keep="first")

                    if "Name" in df:
                        df["Name"] = df["Name"].astype(str)
                    else:
                        df["Name"] = None

                    # adding details to the data
                    # match_case = len(df[df["check"] == True])
                    not_match_case = df[df["check"] == False]
                    report = pd.DataFrame(not_match_case)
                    report = report[["User ID", "check", "System1", "Name"]]
                    reports.append(report)
                # df = pd.concat([df for df in dfs], ignore_index=True)
                report = pd.concat([report for report in reports], ignore_index=True)

            return report

        ##############################################

        dfs = []

        folder_list = pd.Series(os.listdir(self.folder_path))

        for k in range(0, len(folder_list)):
            if folder_list[k].endswith(".xlsx"):
                for j in range(0, len(self.name_key)):
                    checker = self.name_key[j].upper()
                    if checker in folder_list[k]:
                        file_path = self.folder_path + "/" + folder_list[k]
                        excelFile = pd.ExcelFile(file_path)

                        if self.name_code[j] == 1:
                            df = report_unmatch(
                                excelFile, self.staff_data, self.checklist, key=1
                            )
                            dfs.append(df)
                        elif self.name_code[j] == 6:
                            df = report_unmatch(
                                excelFile, self.staff_data, self.checklist, key=6
                            )
                            dfs.append(df)
                        else:
                            df = report_unmatch(
                                excelFile, self.staff_data, self.checklist, key=10
                            )
                            dfs.append(df)

        dataframes = pd.concat([df for df in dfs], ignore_index=True)
        # print(dataframes.head(n=10))
        # print(dataframes.tail(n=10))
        return dataframes

    #################################################### end function

    def automata_report_summary(self):
        ##############################################
        def report_summary(dataframe, staff_data, checklist, key):
            warnings.filterwarnings("ignore")
            ref_data = pd.ExcelFile(checklist)
            ref_cols = ref_data.sheet_names
            # ref_code = pd.read_excel(checklist, sheet_name = ref_cols[0])
            ref_cube = pd.read_excel(checklist, sheet_name=ref_cols[1])
            # keyname is sheet name
            staff_sheet = pd.ExcelFile(staff_data)
            staff_sheet_col = staff_sheet.sheet_names
            staff = pd.read_excel(staff_sheet, sheet_name=staff_sheet_col[1])

            if key == 1:
                # read the necessary data
                df = pd.read_excel(dataframe)

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                # clean user ID for white space and lower case
                # check if the user ID is in the staff list
                df["User ID"] = df["User ID"].str.lower()
                df["User ID"] = df["User ID"].str.strip()

                # conditional filtering
                if "Status" in df.columns:
                    df = df[df["Status"] == "*ENABLED"]
                if "Disable Flag *" in df.columns:
                    df = df[df["Disable Flag *"] == "N"]

                df["check"] = df["User ID"].isin(staff["LAN ID"])

                # auto fix wrong user ID
                # We will check the availability of the Name column
                # there are two persons with the same name
                if "Name" in df:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    dfnew = df[df["check"] == False]
                    dfnew["User ID"] = dfnew["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    dfnew["check"] = dfnew["User ID"].isin(staff["LAN ID"])
                    dfnew = dfnew[dfnew["check"] == True]
                    df = pd.concat([df, dfnew], ignore_index=True)

                df["System1"] = dataframe.sheet_names[0].upper()

                # only statsmartcube need unique filtering
                if "STATSMART CUBE" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["STATSMART CUBE"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )

                    df = df.drop_duplicates(
                        subset=["User ID", "Cube", "System1"], keep="first"
                    )
                if "role code" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["role code"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )

                    df = df.drop_duplicates(
                        subset=["User ID", "Cube", "System1"], keep="first"
                    )

                # adding details to the data
                match_case = len(df[df["check"] == True])
                not_match_case = len(df[df["check"] == False])
                report = pd.DataFrame(
                    {
                        "System": [dataframe.sheet_names[0].upper()],
                        "Match IDs": [match_case],
                        "Not Match IDs": [not_match_case],
                        "Total IDs": [match_case + not_match_case],
                    }
                )

            elif key == 6:
                # read the necessary data
                df = pd.read_excel(dataframe)

                # create two dataframes for based on the access
                df1 = df[df["RBC Access"] == "Yes"]
                df2 = df[df["IFAS Access"] == "Yes"]

                # clean up user ID
                df1["User ID"] = df1["User ID"].str.lower()
                df1["User ID"] = df1["User ID"].str.strip()
                df2["User ID"] = df2["User ID"].str.lower()
                df2["User ID"] = df2["User ID"].str.strip()

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                # check if the user ID is in the staff list
                df1["check"] = df1["User ID"].isin(staff["LAN ID"])
                df2["check"] = df2["User ID"].isin(staff["LAN ID"])

                # auto fix wrong user ID
                # We will check the availability of the Name column
                # there are two persons with the same name
                if "Name" in df1:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    df1new = df1[df1["check"] == False]
                    df1new["User ID"] = df1new["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    df1new["check"] = df1new["User ID"].isin(staff["LAN ID"])
                    df1new = df1new[df1new["check"] == True]
                    df1 = pd.concat([df1, df1new], ignore_index=True)

                if "Name" in df2:
                    unique_name = pd.DataFrame(
                        staff["Name"].drop_duplicates(keep="first")
                    )
                    unique_name["LAN ID"] = staff["LAN ID"]
                    df2new = df2[df2["check"] == False]
                    df2new["User ID"] = df2new["Name"].map(
                        unique_name.set_index("Name")["LAN ID"]
                    )

                    # update the the check column
                    # now the false positive should be corrected
                    df2new["check"] = df2new["User ID"].isin(staff["LAN ID"])
                    df2new = df2new[df2new["check"] == True]
                    df2 = pd.concat([df2, df2new], ignore_index=True)

                df1["System1"] = "RBC"
                df2["System1"] = "IFAS"

                df1 = df1.drop_duplicates(subset=["User ID", "System1"], keep="first")
                df2 = df2.drop_duplicates(subset=["User ID", "System1"], keep="first")

                # adding details to the data
                match_case1 = len(df1[df1["check"] == True])
                not_match_case1 = len(df1[df1["check"] == False])
                report1 = pd.DataFrame(
                    {
                        "System": ["RBC"],
                        "Match IDs": [match_case1],
                        "Not Match IDs": [not_match_case1],
                        "Total IDs": [match_case1 + not_match_case1],
                    }
                )

                match_case2 = len(df2[df2["check"] == True])
                not_match_case2 = len(df2[df2["check"] == False])
                report2 = pd.DataFrame(
                    {
                        "System": ["IFAS"],
                        "Match IDs": [match_case2],
                        "Not Match IDs": [not_match_case2],
                        "Total IDs": [match_case2 + not_match_case2],
                    }
                )
                report = pd.concat([report1, report2], ignore_index=True)

            else:
                # read the necessary data
                sheetName = dataframe.sheet_names
                # dfs = []
                reports = []

                # clean up staff data
                staff["LAN ID"] = staff["LAN ID"].str.lower()
                staff["LAN ID"] = staff["LAN ID"].str.strip()

                for i in range(len(sheetName)):
                    # read the sheet
                    df = pd.read_excel(dataframe, sheet_name=sheetName[i])
                    # due to the nature of the data, we need to only select the User ID
                    # df = pd.DataFrame(df['User ID'])
                    df = df[["User ID"]]
                    # remove empty rows
                    df = df.dropna(axis=0)

                    # clean up user ID
                    df["User ID"] = df["User ID"].str.lower()
                    df["User ID"] = df["User ID"].str.strip()

                    # check if the user ID is in the staff list
                    df["check"] = df["User ID"].isin(staff["LAN ID"])

                    # auto fix wrong user ID
                    # We will check the availability of the Name column
                    # there are two persons with the same name
                    if "Name" in df:
                        unique_name = pd.DataFrame(
                            staff["Name"].drop_duplicates(keep="first")
                        )
                        unique_name["LAN ID"] = staff["LAN ID"]
                        dfnew = df[df["check"] == False]
                        dfnew["User ID"] = dfnew["Name"].map(
                            unique_name.set_index("Name")["LAN ID"]
                        )

                        # update the the check column
                        # now the false positive should be corrected
                        dfnew["check"] = dfnew["User ID"].isin(staff["LAN ID"])
                        dfnew = dfnew[dfnew["check"] == True]
                        df = pd.concat([df, dfnew], ignore_index=True)

                    df["System1"] = sheetName[i].upper()
                    df = df.drop_duplicates(subset=["User ID", "System1"], keep="first")

                    # adding details to the data
                    match_case = len(df[df["check"] == True])
                    not_match_case = len(df[df["check"] == False])
                    report = pd.DataFrame(
                        {
                            "System": [dataframe.sheet_names[i].upper()],
                            "Match IDs": [match_case],
                            "Not Match IDs": [not_match_case],
                            "Total IDs": [match_case + not_match_case],
                        }
                    )
                    reports.append(report)
                # df = pd.concat([df for df in dfs], ignore_index=True)
                report = pd.concat([report for report in reports], ignore_index=True)

            return report

        ##############################################

        dfs = []

        folder_list = pd.Series(os.listdir(self.folder_path))

        for k in range(0, len(folder_list)):
            if folder_list[k].endswith(".xlsx"):
                for j in range(0, len(self.name_key)):
                    checker = self.name_key[j].upper()
                    if checker in folder_list[k]:
                        file_path = self.folder_path + "/" + folder_list[k]
                        excelFile = pd.ExcelFile(file_path)

                        if self.name_code[j] == 1:
                            df = report_summary(
                                excelFile, self.staff_data, self.checklist, key=1
                            )
                            dfs.append(df)
                        elif self.name_code[j] == 6:
                            df = report_summary(
                                excelFile, self.staff_data, self.checklist, key=6
                            )
                            dfs.append(df)
                        else:
                            df = report_summary(
                                excelFile, self.staff_data, self.checklist, key=10
                            )
                            dfs.append(df)

        dataframes = pd.concat([df for df in dfs], ignore_index=True)

        return dataframes


# test = AutomataReport(
# folder_path=r"C:\Users\Khor Kean Teng\Downloads\AUP Automata\rawdata",
# checklist = 'rawdata/Department Checklist.xlsx',
# staff_data = 'rawdata/stafflist.xlsx',
# name_key= ['CCRIS', 'DP', 'STATSMART1', 'ADMIN'],
# name_code= [1, 1, 1, 10],
# )
# test.automata_report_unmatch()
# test.automata_report_summary()
# print(df.head())


# test = AutomataReport(
# folder_path=r"C:\Users\Khor Kean Teng\Downloads\AUP Automata\data\fakesystem",
# checklist = 'data/checklist.xlsx',
# staff_data = 'data/fake_hr_data.xlsx',
# name_key= ['BSE', 'HKEX', 'KLSE', 'LSE1' 'NASDAQ', 'NYSE', 'SGX', 'SSE', 'TSE'],
# name_code= [1, 1, 1, 1, 1, 1, 1, 1, 1],
# )
# test.automata_report_unmatch()

# test.automata_report_summary()
