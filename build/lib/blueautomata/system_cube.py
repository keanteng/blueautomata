"""
A function that will check the system cube for the system.
This function will correct the system cube and system if it is not correct.
"""

import pandas as pd
import warnings


class SystemCubeChecker:
    def __init__(self, masterlistpath, system_to_check, cube_to_assign):
        self.masterlistpath = masterlistpath
        self.system_to_check = system_to_check
        self.cube_to_assign = cube_to_assign

    def system_cube_update(self):
        # ignore warnings
        warnings.filterwarnings("ignore")

        # read the data
        df = pd.read_excel(self.masterlistpath)

        # make sure that the system cube is correct
        for i in range(0, len(df)):
            for j in range(0, len(self.system_to_check)):
                if df["System1"][i] == self.system_to_check[j]:
                    df["System1"][i] = self.cube_to_assign
                    df["Cube"][i] = self.system_to_check[j]
                else:
                    pass
        return df


# test = SystemCubeChecker(
# masterlistpath = 'C:/Users/limzi/OneDrive/Desktop',
# system_to_check= ['NAPIC', 'BSH-BPN', 'EPF', 'BR1M', 'HIES'],
# cube_to_assign='Administration Data'
# )
# test.system_cube_update()
