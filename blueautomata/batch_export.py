"""
When running batch export function make sure
- department and department code column exist
- the program will check this two columns and export the data
- the naming of the two columns should follow the naming convention: dept, dept_code

- make sure the correct masterlist file is attached
"""

import pandas as pd
import os


class BatchExport:
    def __init__(self, destination, masterlist):
        self.destination = destination
        self.masterlist = masterlist

    def batch_export(self):
        # get the name of department and department code
        dept_name = self.masterlist["Department"].unique()
        #dept_code = self.masterlist["Dept"].unique()

        for i in range(0, len(dept_name)):
            # filter the dataframe by dept
            filter = self.masterlist[self.masterlist["Department"] == dept_name[i]]
            filter.reset_index(drop=True, inplace=True)
            # name the file using department code
            filecode = filter["Dept"][0]
            # export the file
            filter.to_excel(self.destination + "/" + str(filecode) + ".xlsx", index=True)

        # print the status
        print("Export Completed")
