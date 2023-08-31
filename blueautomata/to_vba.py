'''
This program will trigger VBA module in Excel
Make sure you have a macro-enabled Excel file with the module in it
Make sure the correct filepath and macro path are defined

Warnings:
1. The VBA program will only work once and no reverse, make sure all the files are correct and backed up before running the program
2. The program is very sensitve the macro and filepath parameters, for incompelete execution, please close the background Excel process in Task Manager
'''

import win32com.client

def templatetize(status = 'START', filepath = r'C:\\Users\\Khor Kean Teng\\Downloads\\AUP Automata\\vbanew.xlsm', macro = 'vbanew.xlsm!Module1.kt_template'):
    if status == 'START':
        xl = win32com.client.Dispatch("Excel.Application")
        wb = xl.Workbooks.Open(filepath)
        xl.Application.Run(macro)
        wb.Save()
        xl.Application.Quit()
        print('Execution Completed')
    else:
        xl = win32com.client.Dispatch("Excel.Application")
        xl.Application.Quit()
        print('Execution Failed. Please enter the correct status')