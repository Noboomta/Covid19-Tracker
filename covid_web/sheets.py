import gspread
import datetime

from django import template
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:

    def __init__(self, username):
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("Covid-19 Tracker Users").sheet1
        self.data = self.sheet.get_all_records()
        self.username = username

    def find_username(self):
        try:
            cell = self.sheet.find(self.username)
            return cell.row
        except:
            row = self.next_available_row()
            self.create_new_user()
            return row

    def next_available_row(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        return str(len(str_list) + 1)

    def next_available_col(self, row):
        # str_list = list(filter(None, self.sheet.row_values(int(row))))
        for i in range(3, 8):
            try:
                if str(self.sheet.cell(row, i).value) == '':
                    return i
            except:
                return i
        return 10

    def create_new_user(self):
        try:
            latestrow = self.next_available_row()
            insertrow = [self.username, str(datetime.datetime.now())]
            self.sheet.append_row(insertrow, table_range=f"A{latestrow}")
        except Exception:
            create_new_user(self)

    def add_country(self, country):
        try:
            status = False
            row = self.find_username()
            col = self.next_available_col(row)
            if self.sheet.row_values(row).__contains__(country):  # already pinned
                return status
            if col < 8:
                self.sheet.update_cell(row, col, country)
                status = True
            return status
        except Exception:
            add_country(self, country)

    def call_countries(self):
        try:
            row = self.find_username()
            countries = self.sheet.row_values(row)[2:]
            return countries
        except Exception:
            call_countries(self)

    def delete_cell(self, country):
        try:
            row = self.find_username()
            for i in range(3, 8):
                if str(self.sheet.cell(row, i).value) == str(country):
                    self.sheet.update_cell(row, i, "")
        except Exception:
            delete_cell(self, country)
