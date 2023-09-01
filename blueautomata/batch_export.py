'''
When running batch export function make sure
- department and department code column exist
- the program will check this two columns and export the data
- the naming of the two columns should follow the naming convention: dept, dept_code

- make sure the correct masterlist file is attached
'''

def batchExport(status = 'START', masterlist = 'data/fakedata.csv'):
    if status == 'START':
        # get the name of department and department code
        dept_name = masterlist['dept_name'].unique()
        dept_code = masterlist['dept_code'].unique()
        
        for i in range(0, len(dept_name)):
            # filter the dataframe by dept
            filter = masterlist[masterlist['dept_name'] == dept_name[i]]
            # name the file using department code
            filecode = dept_code[i]
            # export the file
            filter.to_excel('data/dept_' + filecode + '.xlsx', index=True)
    
        # print the status
        print('Export Completed')
    else:
        print('Export Failed. Please enter the correct status and check the masterlist path')