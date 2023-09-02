'''
This function performs data cleaning for function based on 3 different keys:
1. Key 1: Data cleaning for files that can be read directly
2. Key 2: Data cleaning for files that can be read directly but need filter with some condition
3. Key 3: Data cleaning for files that cannot be read directly because of different sheet

There are two same name person in the HR data, so we need to remove one of them to enable auto correction
Upper or Lower all columns for easy processing
'''

import pandas as pd
import warnings

def dataCleaning(dataframe, staff_data, checklist, key):
    warnings.filterwarnings("ignore")
    ref_data = pd.ExcelFile(checklist)
    ref_cols = ref_data.sheet_names
    ref_code = pd.read_excel(checklist, sheet_name = ref_cols[0])
    ref_cube = pd.read_excel(checklist, sheet_name = ref_cols[1])
    #keyname is sheet name
    staff_sheet = pd.ExcelFile(staff_data)
    staff_sheet_col = staff_sheet.sheet_names
    staff = pd.read_excel(staff_sheet, sheet_name = staff_sheet_col[1])
    
    if key == 1:
        # read the necessary data
        df = pd.read_excel(dataframe)
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        # clean user ID for white space and lower case
        # check if the user ID is in the staff list
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            dfnew = df[df['check'] == False]
            dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            dfnew = dfnew[dfnew['check'] == True]
            df = pd.concat([df, dfnew], ignore_index=True)
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = dataframe.sheet_names[0].upper()
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
        
    elif key == 2:
        # read the necessary data
        # key 2 is for statsmart system
        df = pd.read_excel(dataframe)
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        # clean user ID for white space and lower case
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            dfnew = df[df['check'] == False]
            dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            dfnew = dfnew[dfnew['check'] == True]
            df = pd.concat([df, dfnew], ignore_index=True)
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = dataframe.sheet_names[0].upper()
        temp = ref_cube.columns
        df['Cube'] = df['role code'].map(ref_cube.set_index(temp[0])[temp[1]])
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    elif key == 3:
        # key 3 is for stasmart cube system
        # read the necessary data
        df = pd.read_excel(dataframe)
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            dfnew = df[df['check'] == False]
            dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            dfnew = dfnew[dfnew['check'] == True]
            df = pd.concat([df, dfnew], ignore_index=True)
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = dataframe.sheet_names[0].upper()
        temp = ref_cube.columns
        df['Cube'] = df['STATSMART CUBE'].map(ref_cube.set_index(temp[0])[temp[1]])
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 4:
        # read the necessary data
        df = pd.read_excel(dataframe)
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        
        # filter the data, only enabled user will be considered
        # we put a condition in case the status column is not available
        if 'Status' in df.columns:
            df = df[df['Status']== '*ENABLED']
            
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            dfnew = df[df['check'] == False]
            dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            dfnew = dfnew[dfnew['check'] == True]
            df = pd.concat([df, dfnew], ignore_index=True)
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = dataframe.sheet_names[0].upper()
        temp = ref_cube.columns
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 5:
        # read the necessary data
        df = pd.read_excel(dataframe)
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        # clean user ID for white space and lower case
        df['User ID'] = df['User ID'].str.lower()
        df['User ID'] = df['User ID'].str.strip()
        
        # filter the data, only enabled user will be considered
        # we put a condition in case the disable flag * column is not available
        if 'Disable Flag *' in df.columns:
            df = df[df['Disable Flag *'] == 'N']
            
        df['check'] = df['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            dfnew = df[df['check'] == False]
            dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
            dfnew = dfnew[dfnew['check'] == True]
            df = pd.concat([df, dfnew], ignore_index=True)
        
        # adding details to the data
        df = df[df['check'] == True]
        df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
        df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
        df['System1'] = dataframe.sheet_names[0].upper()
        temp = ref_cube.columns
        df['Cube'] = None
        df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df.reset_index(drop=True, inplace=True)
        df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
    
    elif key == 6:
        # read the necessary data
        df = pd.read_excel(dataframe)
        
        # create two dataframes for based on the access
        df1 = df[df['RBC Access'] == 'Yes']
        df2 = df[df['IFAS Access'] == 'Yes']
        
        # clean up user ID
        df1['User ID'] = df1['User ID'].str.lower()
        df1['User ID'] = df1['User ID'].str.strip()
        df2['User ID'] = df2['User ID'].str.lower()
        df2['User ID'] = df2['User ID'].str.strip()
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        # check if the user ID is in the staff list
        df1['check'] = df1['User ID'].isin(staff['LAN ID'])
        df2['check'] = df2['User ID'].isin(staff['LAN ID'])
        
        # auto fix wrong user ID
        # We will check the availability of the Name column
        # there are two persons with the same name
        if 'Name' in df1:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            df1new = df1[df1['check'] == False]
            df1new['User ID'] = df1new['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            df1new['check'] = df1new['User ID'].isin(staff['LAN ID'])
            df1new = df1new[df1new['check'] == True]
            df1 = pd.concat([df1, df1new], ignore_index=True)
        
        if 'Name' in df2:
            unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
            unique_name['LAN ID'] = staff['LAN ID']
            df2new = df2[df2['check'] == False]
            df2new['User ID'] = df2new['Name'].map(unique_name.set_index('Name')['LAN ID'])
            
            # update the the check column
            # now the false positive should be corrected
            df2new['check'] = df2new['User ID'].isin(staff['LAN ID'])
            df2new = df2new[df2new['check'] == True]
            df2 = pd.concat([df2, df2new], ignore_index=True)
        
        # adding details to the data
        df1 = df1[df1['check'] == True]
        df2 = df2[df2['check'] == True]
        df1['Department'] = df1['User ID'].map(staff.set_index('LAN ID')['Department'])
        df2['Department'] = df2['User ID'].map(staff.set_index('LAN ID')['Department'])
        df1['Dept'] = df1['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df2['Dept'] = df2['Department'].map(ref_code.set_index('Department')['Dept Code'])
        df1['Name'] = df1['User ID'].map(staff.set_index('LAN ID')['Name'])
        df2['Name'] = df2['User ID'].map(staff.set_index('LAN ID')['Name'])
        # we do not use keyname variable due to the nature of this dataset
        # two system in one file
        df1['System1'] = 'RBC'
        df2['System1'] = 'IFAS'
        df1['Cube'] = None
        df2['Cube'] = None
        
        # reset the index and select the necessary columns
        df1.reset_index(drop=True, inplace=True)
        df2.reset_index(drop=True, inplace=True)
        df1 = df1[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
        df2 = df2[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
        
        # merge the two dataframes
        df = pd.concat([df1, df2], ignore_index=True)
    
    else:
        # read the necessary data
        sheetName = dataframe.sheet_names
        dfs = []
        
        # clean up staff data
        staff['LAN ID'] = staff['LAN ID'].str.lower()   
        staff['LAN ID'] = staff['LAN ID'].str.strip()
        
        for i in range(len(sheetName)):
            # read the sheet
            df = pd.read_excel(dataframe, sheet_name = sheetName[i])
            # due to the nature of the data, we need to only select the User ID
            # df = pd.DataFrame(df['User ID'])
            df = df[['User ID']]
            # remove empty rows
            df = df.dropna(axis = 0)
            
            # clean up user ID
            df['User ID'] = df['User ID'].str.lower()
            df['User ID'] = df['User ID'].str.strip()
            
            # check if the user ID is in the staff list
            df['check'] = df['User ID'].isin(staff['LAN ID'])
            
            # auto fix wrong user ID
            # We will check the availability of the Name column
            # there are two persons with the same name
            if 'Name' in df:
                unique_name = pd.DataFrame(staff['Name'].drop_duplicates(keep = 'first'))
                unique_name['LAN ID'] = staff['LAN ID']
                dfnew = df[df['check'] == False]
                dfnew['User ID'] = dfnew['Name'].map(unique_name.set_index('Name')['LAN ID'])
                
                # update the the check column
                # now the false positive should be corrected
                dfnew['check'] = dfnew['User ID'].isin(staff['LAN ID'])
                dfnew = dfnew[dfnew['check'] == True]
                df = pd.concat([df, dfnew], ignore_index=True)
            
            # adding details to the data
            df = df[df['check'] == True]
            df['Department'] = df['User ID'].map(staff.set_index('LAN ID')['Department'])
            df['Name'] = df['User ID'].map(staff.set_index('LAN ID')['Name'])
            df['Dept'] = df['Department'].map(ref_code.set_index('Department')['Dept Code'])
            df['System1'] = sheetName[i].upper()
            df['Cube'] = None
            
            # reset the index and select the necessary columns
            df.reset_index(drop=True, inplace=True)
            df = df[['Department', 'Dept', 'User ID', 'Name', 'System1', 'Cube']]
            dfs.append(df)
        df = pd.concat([df for df in dfs], ignore_index=True)
            
            
    #print(df.head())
    #print(len(df))
    return df

excelFile = pd.ExcelFile('rawdata/USERSBANKING.xlsx')
dataCleaning(excelFile , staff_data = 'rawdata/stafflist.xlsx', 
              checklist = 'rawdata/Department Checklist.xlsx', key = 10)