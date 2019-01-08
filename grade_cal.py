import pandas as pd
from tabulate import tabulate
import art

class dbGrade():
    ''' This program is a basic virsual database system that provide some basic method in database such as create,
    update, edit and also can display and calculale GPA from data that read from CSV file, All of the python module
    that i use in this programe is all basic method that you can find and download, Hope you enjoy. '''

    # This function use for read file CSV and clean data into pandas dataframe.
    def readCSV(self):
        self.dataCSV = pd.read_csv("Grade Report - Grade Report (1) - Grade Report - Grade Report (1).csv", index_col= False)
        # self.data.loc[:, ~self.data.columns.str.contains('^Unnamed')]
        self.naClean = self.dataCSV.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
        self.db = self.naClean
        print(tabulate(self.db, headers='keys', tablefmt='psql'))

    # For display homepage.
    def homepage(self):
        self.lookUp = {
            'A': 4,
            'B+': 3.5,
            'B': 3,
            'C+': 2.5,
            'C': 2,
            'D+': 1.5,
            'D': 1,
            'F': 0
        }
        self.homepageText = art.tprint("TextBase_DB", font="3d_diagonal")
        self.readCSV()
        self.modeControl()

    def modeControl(self):
        print("What mode do you want to use ? \n [1] Insert \n [2] Edit \n [3] View grade\n [4] Save%Exit")
        try:
            self.modeStatus = int(input("Please insert mode here: "))
            if not isinstance(self.modeStatus, str):
                self.modeCheck(self.modeStatus)
            else:
                # print('else')
                print("\n\nPlease insert number follow by instruction below !!")
                self.modeControl()
        except ValueError:
            # print('except')
            print("\n\nPlease insert number follow by instruction below !!")
            self.modeControl()

    def modeCheck(self, status):
        if status == 1:
            self.addData()
        elif status == 2:
            self.editData()
        elif status == 3:
            self.gradeChecker()
        elif status == 4:
            self.saveFile()
        else:
            self.modeCheck(status)

    # This function provide a input to db or dataframe in add mode
    def addData(self):
        self.addDataText = art.tprint("Add_data", font="3d_diagonal")
        self.subjectName = input('Please insert ชื่อวิชา here: ')
        self.degree = int(input('Please insert หน่วยกิต here: '))
        self.section = int(input('Please insert ตอนเรียน here: '))
        self.semester = int(input('Please insert เทอม here: '))
        self.grade = input('Please insert เกรด(for example A, B, C) here: ')

        self.db = self.db.append({'ชื่อวิชา': self.subjectName, 'หน่วยกิต': self.degree, 'ตอนเรียน': self.section,
                                  'เกรด': self.grade, 'เทอม': self.semester,
                                  'เกรดที่เป็นตัวเลข': self.lookUp[self.grade]}, ignore_index=True)
        print(self.db)
        print(tabulate(self.db, headers='keys', tablefmt='psql'))
        self.addStatusChecker()

    def addStatusChecker(self):
        try:
            status = input('do you want to continue ? (y/n):   ')
            if status == 'y':
                self.addData()
            elif status == 'n':
                self.homepage()
            else:
                self.addStatusChecker()
        except:
            self.addStatusChecker()

    def editStatusChecker(self):
        try:
            status = input('do you want to continue ? (y/n):   ')

            if status == 'y':
                self.editData()
            elif status == 'n':
                self.homepage()
            else:
                self.editStatusChecker()


        except:
            self.addStatusChecker()

    def gradeStatusChecker(self):
        try:
            status = input('do you want to continue ? (y/n):   ')

            if status == 'y':
                self.gradeChecker()
            elif status == 'n':
                self.homepage()
            else:
                self.gradeStatusChecker()


        except:
            self.gradeStatusChecker()

    # This funtion will get dataframe index and edit data in that specific index.
    def editData(self):
        self.editDataText = art.tprint("Update_data", font="3d_diagonal")
        print(tabulate(self.db, headers='keys', tablefmt='psql'))
        self.editInput = int(input("Please select number of subject that you want to edit: "))
        self.columnList = ['ชื่อวิชา', 'หน่วยกิต', 'ตอนเรียน', 'เกรด', 'เทอม']
        for i in self.columnList:
            if i == 'ชื่อวิชา' or i == 'เกรด':
                strInput = self.db.loc[self.editInput, i] = input("Please insert {}(Character): ".format(i))
            else:
                self.editInputMeth(i)

        self.db.loc[self.editInput, 'เกรดที่เป็นตัวเลข'] = self.lookUp[self.db.loc[self.editInput, 'เกรด']]
        print(tabulate(self.db, headers='keys', tablefmt='psql'))
        self.editStatusChecker()

    def editInputMeth(self, i):
        try:
            intInput = self.db.loc[self.editInput, i] = int(input("Please insert {} (Integer): ".format(i)))
            return intInput
        except:
            print("Please insert the correct type of {} !!".format(i))
            self.editInputMeth(i)

    # This function use to show grade in summary and semester type.
    def gradeChecker(self):
        self.editDataText = art.tprint("Grade_Checker", font="3d_diagonal")
        gradeQuestion = int(input("[1] Grade summary \n[2] Grade for each term \n "
                                  "Please select mode that you want to use: "))
        if gradeQuestion == 1:
            self.db = self.db.astype({'หน่วยกิต': int})
            pointOrder = self.db['เกรดที่เป็นตัวเลข'] * self.db['หน่วยกิต']
            finalGrade = pointOrder.sum() / self.db['หน่วยกิต'].sum()
            art.tprint("GPA = {}".format(str(finalGrade)[:4]), font='roman')
        elif gradeQuestion == 2:
            term = int(input("Which term that you want to see ?: "))
            dbCleaned = self.db[(self.db["เทอม"] == term)]
            dbCleaned = dbCleaned.astype({'หน่วยกิต': int})
            pointOrder = dbCleaned['เกรดที่เป็นตัวเลข'] * dbCleaned['หน่วยกิต']
            finalGrade = pointOrder.sum() / dbCleaned['หน่วยกิต'].sum()
            art.tprint("GPA = {}".format(str(finalGrade)[:4]), font='roman')

    def saveFile(self):
        self.db.to_csv('GPA.csv', encoding='utf-8', index=False)
        art.tprint("BYE !!!", font='roman')

main = dbGrade()
main.homepage()



# print(os.listdir(os.getcwd()))
