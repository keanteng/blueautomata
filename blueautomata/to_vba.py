'''
This program will trigger VBA module in Excel
Make sure you have a macro-enabled Excel file with the module in it
Make sure the correct filepath and macro path are defined

Warnings:
1. The VBA program will only work once and no reverse, make sure all the files are correct and backed up before running the program
2. The program is very sensitve the macro and filepath parameters, for incompelete execution, please close the background Excel process in Task Manager
'''

import win32com.client

class automate_vba:
    def __init__(self, filepath, macro):
        self.filepath = filepath
        self.macro = macro

    def templatetize(self):
            xl = win32com.client.Dispatch("Excel.Application")
            wb = xl.Workbooks.Open(self.filepath)
            xl.Application.Run(self.macro)
            wb.Save()
            xl.Application.Quit()
            print('Execution Completed')