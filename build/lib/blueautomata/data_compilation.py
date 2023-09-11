"""
This function will read the folder containing all the raw data files generated from the system
Subsequently, it will read and clean the data, so that they have the same format a
"""

"""
This function performs data cleaning for function based on 3 different keys:
1. Key 1: Data cleaning for files that can be read directly
2. Key 2: Data cleaning for files that can be read directly but need filter with some condition
3. Key 3: Data cleaning for files that cannot be read directly because of different sheet

There are two same name person in the HR data, so we need to remove one of them to enable auto correction
Upper or Lower all columns for easy processing
"""

import os
import pandas as pd
import warnings


class BlueAutomata:
    def __init__(self, folder_path, checklist, staff_data, name_key, name_code):
        self.folder_path = folder_path
        self.checklist = checklist
        self.staff_data = staff_data
        self.name_key = name_key
        self.name_code = name_code

    def automata_execution(self):
        ##############################################
        def dataCleaning(dataframe, staff_data, checklist, key):
            warnings.filterwarnings("ignore")
            ref_data = pd.ExcelFile(checklist)
            ref_cols = ref_data.sheet_names
            ref_code = pd.read_excel(checklist, sheet_name=ref_cols[0])
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
                # filter the data, only enabled user will be considered
                # we put a condition in case the status column is not available
                if "Status" in df.columns:
                    df = df[df["Status"] == "*ENABLED"]

                # filter the data only no flag use will be considered
                # we put a condition in case the disable flag * column is not available
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

                # adding details to the data
                df = df[df["check"] == True]
                df["Department"] = df["User ID"].map(
                    staff.set_index("LAN ID")["Department"]
                )
                df["Name"] = df["User ID"].map(staff.set_index("LAN ID")["Name"])
                df["System1"] = dataframe.sheet_names[0].upper()

                # conditional filtering
                # for system with column role code
                if "role code" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["role code"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )
                elif "STATSMART CUBE" in df.columns:
                    temp = ref_cube.columns
                    df["Cube"] = df["STATSMART CUBE"].map(
                        ref_cube.set_index(temp[0])[temp[1]]
                    )
                else:
                    df["Cube"] = None

                df["Dept"] = df["Department"].map(
                    ref_code.set_index("Department")["Dept Code"]
                )
                df.reset_index(drop=True, inplace=True)
                df = df[["Department", "Dept", "User ID", "Name", "System1", "Cube"]]

                # unique filter
                df = df.drop_duplicates(
                    subset=["User ID", "System1", "Cube"], keep="first"
                )

            # elif key == 2:
            # read the necessary data
            # key 2 is for statsmart system
            # df = pd.read_excel(dataframe)

            # clean up staff data
            # staff['LAN ID'] = staff['LAN ID'].str.lower()
            # staff['LAN ID'] = staff['LAN ID'].str.strip()

            # clean user ID for white space and lower case
            # df['User ID'] = df['User ID'].str.lower()
            # df['User ID'] = df['User ID'].str.strip()
            # df['check'] = df['User ID'].isin(staff['LAN ID'])

            # auto fix wrong user ID
            # We will check the availability of the Name column
            # there are two persons with the same name
            # if 'Name' in df:
            # unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            # unique_name['LAN ID'] = staff['LAN ID']
            # dfnew = df[df['check'] == False]
            # dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])

            # update the the check column
            # now the false positive should be corrected
            # dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            # dfnew = dfnew[dfnew['check'] == True]
            # df = pd.concat([df, dfnew], ignore_index=True)

            # adding details to the data
            # df = df[df['check'] == True]
            # df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
            # df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
            # df['System1'] = dataframe.sheet_names[0].upper()
            # temp = ref_cube.columns
            # df['Cube'] = df['role code'].map(ref_cube.set_index(temp[0])[temp[1]])
            # df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
            # df.reset_index(drop=True, inplace=True)
            # df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
            # elif key == 3:
            # key 3 is for stasmart cube system
            # read the necessary data
            # df = pd.read_excel(dataframe)

            # clean up staff data
            # staff['LAN ID'] = staff['LAN ID'].str.lower()
            # staff['LAN ID'] = staff['LAN ID'].str.strip()

            # df['User ID'] = df['User ID'].str.lower()
            # df['User ID'] = df['User ID'].str.strip()
            # df['check'] = df['User ID'].isin(staff['LAN ID'])

            # auto fix wrong user ID
            # We will check the availability of the Name column
            # there are two persons with the same name
            # if 'Name' in df:
            # unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            # unique_name['LAN ID'] = staff['LAN ID']
            # dfnew = df[df['check'] == False]
            # dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])

            # update the the check column
            # now the false positive should be corrected
            # dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            # dfnew = dfnew[dfnew['check'] == True]
            # df = pd.concat([df, dfnew], ignore_index=True)

            # adding details to the data
            # df = df[df['check'] == True]
            # df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
            # df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
            # df['System1'] = dataframe.sheet_names[0].upper()
            # temp = ref_cube.columns
            # df['Cube'] = df['STATSMART CUBE'].map(ref_cube.set_index(temp[0])[temp[1]])
            # df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
            # df.reset_index(drop=True, inplace=True)
            # df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]

            # elif key == 4:
            # read the necessary data
            # df = pd.read_excel(dataframe)

            # clean up staff data
            # staff['LAN ID'] = staff['LAN ID'].str.lower()
            # staff['LAN ID'] = staff['LAN ID'].str.strip()

            # df['User ID'] = df['User ID'].str.lower()
            # df['User ID'] = df['User ID'].str.strip()

            # filter the data, only enabled user will be considered
            # we put a condition in case the status column is not available
            # if 'Status' in df.columns:
            # df = df[df['Status']== '*ENABLED']

            # df['check'] = df['User ID'].isin(staff['LAN ID'])

            # auto fix wrong user ID
            # We will check the availability of the Name column
            # there are two persons with the same name
            # if 'Name' in df:
            # unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            # unique_name['LAN ID'] = staff['LAN ID']
            # dfnew = df[df['check'] == False]
            # dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])

            # update the the check column
            # now the false positive should be corrected
            # dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            # dfnew = dfnew[dfnew['check'] == True]
            # df = pd.concat([df, dfnew], ignore_index=True)

            # adding details to the data
            # df = df[df['check'] == True]
            # df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
            # df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
            # df['System1'] = dataframe.sheet_names[0].upper()
            # temp = ref_cube.columns
            # df['Cube'] = None
            # df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
            # df.reset_index(drop=True, inplace=True)
            # df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]

            # elif key == 5:
            # read the necessary data
            # df = pd.read_excel(dataframe)

            # clean up staff data
            # staff['LAN ID'] = staff['LAN ID'].str.lower()
            # staff['LAN ID'] = staff['LAN ID'].str.strip()

            # clean user ID for white space and lower case
            # df['User ID'] = df['User ID'].str.lower()
            # df['User ID'] = df['User ID'].str.strip()

            # filter the data, only enabled user will be considered
            # we put a condition in case the disable flag * column is not available
            # if 'Disable Flag *' in df.columns:
            # df = df[df['Disable Flag *'] == 'N']

            # df['check'] = df['User ID'].isin(staff['LAN ID'])

            # auto fix wrong user ID
            # We will check the availability of the Name column
            # there are two persons with the same name
            # if 'Name' in df:
            # unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            # unique_name['LAN ID'] = staff['LAN ID']
            # dfnew = df[df['check'] == False]
            # dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])

            # update the the check column
            # now the false positive should be corrected
            # dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            # dfnew = dfnew[dfnew['check'] == True]
            # df = pd.concat([df, dfnew], ignore_index=True)

            # adding details to the data
            # df = df[df['check'] == True]
            # df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
            # df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
            # df['System1'] = dataframe.sheet_names[0].upper()
            # temp = ref_cube.columns
            # df['Cube'] = None
            # df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
            # df.reset_index(drop=True, inplace=True)
            # df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]

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

                # adding details to the data
                df1 = df1[df1["check"] == True]
                df2 = df2[df2["check"] == True]
                df1["Department"] = df1["User ID"].map(
                    staff.set_index("LAN ID")["Department"]
                )
                df2["Department"] = df2["User ID"].map(
                    staff.set_index("LAN ID")["Department"]
                )
                df1["Dept"] = df1["Department"].map(
                    ref_code.set_index("Department")["Dept Code"]
                )
                df2["Dept"] = df2["Department"].map(
                    ref_code.set_index("Department")["Dept Code"]
                )
                df1["Name"] = df1["User ID"].map(staff.set_index("LAN ID")["Name"])
                df2["Name"] = df2["User ID"].map(staff.set_index("LAN ID")["Name"])
                # we do not use keyname variable due to the nature of this dataset
                # two system in one file
                df1["System1"] = dataframe.sheet_names[0].upper()
                df2["System1"] = dataframe.sheet_names[0].upper()
                df1["Cube"] = "RBC"
                df2["Cube"] = "IFAS"

                # reset the index and select the necessary columns
                df1.reset_index(drop=True, inplace=True)
                df2.reset_index(drop=True, inplace=True)
                df1 = df1[["Department", "Dept", "User ID", "Name", "System1", "Cube"]]
                df2 = df2[["Department", "Dept", "User ID", "Name", "System1", "Cube"]]

                # merge the two dataframes
                df = pd.concat([df1, df2], ignore_index=True)

                # perform unique filtering
                df = df.drop_duplicates(
                    subset=["User ID", "System1", "Cube"], keep="first"
                )

            else:
                # read the necessary data
                sheetName = dataframe.sheet_names
                dfs = []

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

                    # adding details to the data
                    df = df[df["check"] == True]
                    df["Department"] = df["User ID"].map(
                        staff.set_index("LAN ID")["Department"]
                    )
                    df["Name"] = df["User ID"].map(staff.set_index("LAN ID")["Name"])
                    df["Dept"] = df["Department"].map(
                        ref_code.set_index("Department")["Dept Code"]
                    )
                    df["System1"] = sheetName[i].upper()
                    df["Cube"] = None

                    # reset the index and select the necessary columns
                    df.reset_index(drop=True, inplace=True)
                    df = df[
                        ["Department", "Dept", "User ID", "Name", "System1", "Cube"]
                    ]
                    dfs.append(df)

                # merge the dataframes together
                df = pd.concat([df for df in dfs], ignore_index=True)

                # perform unique filtering
                df = df.drop_duplicates(
                    subset=["User ID", "System1", "Cube"], keep="first"
                )

            # print(df.head())
            # print(len(df))
            return df

        ##############################################

        dfs = []

        folder_list = pd.Series(os.listdir(self.folder_path))

        for k in range(0, len(folder_list)):
            if folder_list[k].endswith(".xlsx"):
                for j in range(0, len(self.name_key)):
                    checker = self.name_key[j].upper()
                    if checker in folder_list[k]:
                        # file_path = self.folder_path + '/*' + checker.upper() + '*.xlsx'
                        file_path = self.folder_path + "/" + folder_list[k]
                        excelFile = pd.ExcelFile(file_path)

                        if self.name_code[j] == 1:
                            df = dataCleaning(
                                excelFile, self.staff_data, self.checklist, key=1
                            )
                            dfs.append(df)
                        # elif self.name_code[j] == 2:
                        # df = dataCleaning(excelFile, self.staff_data, self.checklist, key = 2)
                        # dfs.append(df)
                        # elif self.name_code[j] == 3:
                        # df = dataCleaning(excelFile, self.staff_data, self.checklist, key = 3)
                        # dfs.append(df)
                        # elif self.name_code[j] == 4:
                        # df = dataCleaning(excelFile, self.staff_data, self.checklist, key = 4)
                        # dfs.append(df)
                        # elif self.name_code[j] == 5:
                        # df = dataCleaning(excelFile, self.staff_data, self.checklist, key = 5)
                        # dfs.append(df)
                        elif self.name_code[j] == 6:
                            df = dataCleaning(
                                excelFile, self.staff_data, self.checklist, key=6
                            )
                            dfs.append(df)
                        else:
                            df = dataCleaning(
                                excelFile, self.staff_data, self.checklist, key=10
                            )
                            # df = dataCleaning(pd.ExcelFile('rawdata/ADMIN.xlsx') , staff_data = 'rawdata/stafflist.xlsx', checklist = 'rawdata/Department Checklist.xlsx', key = 10)
                            dfs.append(df)

        dataframes = pd.concat([df for df in dfs], ignore_index=True)
        # dataframes['User ID'] = dataframes['User ID'].dropna(axis = 0)

        return dataframes
        # dataframes.to_excel('data/automataoutput.xlsx', index = False)
        # return dataframes

    # automata_execution(
    # name_key= ['DP', 'STATSMART', 'ADMIN'],
    # name_code= [1, 2, 10],
    # )


#test = BlueAutomata(
    #folder_path=r"C:\Users\Khor Kean Teng\Downloads\AUP Automata\rawdata",
    #checklist="rawdata/Department Checklist.xlsx",
    #staff_data="rawdata/stafflist.xlsx",
    #name_key=["RBCIFAS"],
    #name_code=[6],
#)
#test.automata_execution()
