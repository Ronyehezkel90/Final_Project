from Tkinter import *

from activity_measures import ActivityMeasures
from basic_measures import BasicMeasures
import tkMessageBox
import numpy as np
import matplotlib.pyplot as plt
from connector import Connector
import webbrowser
import time
import pandas as pd
from tkFileDialog import askopenfilename
from utils import write_user_data_to_file, iniatilize_results_file, get_current_time
from conf import BASIC_MEASURES


class GUI:
    def __init__(self):
        self.connector = None
        self.basic_measures = None
        self.activity_measures = None
        self.authorization_type = None
        self.root = Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.geometry('{}x{}'.format(500, 500))
        # self.root.resizable(width=False, height=False)
        self.users = []
        self.login_gui()

    def login_gui(self):
        self.connector = Connector()
        user_login_button = Button(self.root, text="Login as user", fg="white", bg="black", bd=5,
                                   command=lambda: self.login_controller('user'))
        app_login_button = Button(self.root, text="Login as applicaton", fg="white", bg="black", bd=5,
                                  command=lambda: self.login_controller('app'))
        user_login_button.grid(row=1, column=1, sticky=S)
        user_login_button.place(relx=0.3, rely=0.5, anchor=CENTER)
        app_login_button.grid(row=1, column=1, sticky=S)
        app_login_button.place(relx=0.7, rely=0.5, anchor=CENTER)
        self.root.title("Twitter")
        self.root.mainloop()

    def clear_root_frame(self):
        for ele in self.root.winfo_children():
            ele.destroy()

    def user_authorization_button(self, verifier_code):
        self.connector.user_authorization(verifier_code)
        self.basic_measures = BasicMeasures(self.connector)
        self.activity_measures = ActivityMeasures()
        self.clear_root_frame()
        self.create_gui()

    def create_user_login_gui(self):
        self.clear_root_frame()
        Label(text='Please go to this address and authorize yourself\n').pack(side=TOP, padx=10, pady=10)
        link = Label(text='Authorization Link', fg="blue", cursor="hand2")
        link.pack()

        def callback(event):
            webbrowser.open_new(self.connector.auth.get_authorization_url())

        link.bind("<Button-1>", callback)
        Label(text='Write here your code').pack(side=TOP, padx=10, pady=10)
        '+self.connector.auth.get_authorization_url()+'
        entry = Entry(self.root, width=10)
        entry.pack(side=TOP, padx=10, pady=10)

        user_login_button = Button(self.root, text="Authorize", fg="white", bg="black", bd=5,
                                   command=lambda: self.user_authorization_button(entry.get()))
        user_login_button.pack(side=TOP, padx=10, pady=10)
        user_login_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.root.mainloop()

    def login_controller(self, authorization_type):
        self.authorization_type = authorization_type
        self.create_user_login_gui() if self.authorization_type == 'user' else self.connector.application_authorization()
        self.basic_measures = BasicMeasures(self.connector)
        self.activity_measures = ActivityMeasures()
        self.clear_root_frame()
        self.create_gui()

    def create_gui(self):
        user = Label(self.root, text="Members:", font="-weight bold")
        user.grid(row=0, sticky=W)
        self.listbox = Listbox(self.root, width=18, height=10)
        self.listbox.grid(row=1, rowspan=6)

        but_1 = Button(self.root, text="Basic Measures", fg="white", bg="black", bd=5,
                       command=self.basic_measure_frame_on_click)
        but_2 = Button(self.root, text="Activity Measures", fg="white", bg="black", bd=5)
        but_3 = Button(self.root, text="Popularity Measures", fg="white", bg="black", bd=5)
        but_4 = Button(self.root, text="Influence Measures", fg="white", bg="black", bd=5)
        but_6 = Button(self.root, text="Add user", fg="black", bg="gray", bd=5, command=self.add_user_frame_on_click)
        but_7 = Button(self.root, text="Remove user", fg="black", bg="gray", bd=5, command=self.remove_user_on_click)
        but_8 = Button(self.root, text="Choose File", fg="black", bg="gray", bd=5, command=self.add_users_from_file)

        but_1.grid(row=1, column=1, sticky=S)
        but_2.grid(row=2, column=1, sticky=S)
        but_3.grid(row=3, column=1, sticky=S)
        but_4.grid(row=4, column=1, sticky=S)
        but_6.grid(row=7, column=0, sticky=S)
        but_7.grid(row=7, column=1, sticky=S)
        but_8.grid(row=8, column=1, sticky=S)
        self.root.title("Twitter")
        self.root.mainloop()

    def remove_user_on_click(self):
        selection = self.listbox.curselection()
        self.listbox.delete(selection[0])
        for i, screen_name in self.users:
            if screen_name == '':
                self.users.remove(i)
        ron = 2

    def add_user_frame_on_click(self):
        add_user_root = Tk()
        add_user_root.wm_attributes("-topmost", 1)
        user = Label(add_user_root, text="Insert screen name:", font="-weight bold")
        self.entry_user = Entry(add_user_root)
        user.grid(row=1, columnspan=3)
        self.entry_user.grid(row=2, columnspan=3)
        # TEST
        self.entry_user.insert(0, 'yaniv33martin')
        dot_2 = Label(add_user_root, text=".", fg="gray")
        but_2 = Button(add_user_root, text="Add User", bd=5, width=15, command=self.add_user_on_click)
        dot_2.grid(row=3, sticky=W)
        but_2.grid(row=4, column=2, sticky=S)
        add_user_root.title("Twitter - Add User")
        add_user_root.geometry("250x150")
        add_user_root.mainloop()

    def basic_measures_plot(self, dict_of_users_dicts):
        x = 0
        my_xticks = ''
        max_value = 0
        for user_dict in dict_of_users_dicts.values():
            x = np.arange(user_dict.__len__())
            plt.plot(x, user_dict.values())
            my_xticks = user_dict.keys()
            if max(user_dict.values()) > max_value:
                max_value = max(user_dict.values())
        plt.xticks(x, my_xticks)
        # y= np.arange(max_value+1)
        plt.show()

    def calculate_measures(self, user, dict_of_users_dicts, results_df, count_users):
        screen_name = user[0]['screen_name']
        dict_of_users_dicts[screen_name] = self.basic_measures.get_all_basic_measures(user)
        dict_of_users_dicts[screen_name].update(
            self.activity_measures.get_all_activity_measures(dict_of_users_dicts[screen_name]))
        df = pd.DataFrame([dict_of_users_dicts[screen_name]])
        df['USER'] = screen_name
        results_df = results_df.append(df)
        results_df.to_excel('a.xlsx', index=False)
        print str(count_users) + '. ' + screen_name + ' ::: ' + get_current_time()
        return results_df

    def basic_measure_frame_on_click(self):
        print 'calculation started: ' + get_current_time()
        dict_of_users_dicts = {}
        count_users = 0
        results_df = pd.DataFrame()
        for user in self.users:
            screen_name = user[0]['screen_name']
            try:
                results_df = self.calculate_measures(user, dict_of_users_dicts, results_df, count_users)
                # write_user_data_to_file(count_users, writer, user, dict_of_users_dicts[user.name].values())
                count_users += 1
            except Exception as e:
                print 'e: ' + e.message
                print 'Limit Reached\nUser: ' + screen_name + '\nUser Number:' + str(count_users)
                i = 0
                while i <= 16:
                    time.sleep(60)
                    i += 1
                    print str(i) + ' min passed'
                    # self.basic_measures_plot(dict_of_users_dicts)
                try:
                    results_df = self.calculate_measures(user, dict_of_users_dicts, results_df, count_users)
                except Exception as e:
                    print screen_name + ' --- Failed after failure - e: ' + e.message

    def add_users_from_file(self):
        Tk().withdraw()
        file_name = askopenfilename()
        with open(file_name) as f:
            users_from_file = f.readlines()
        users_from_file = [x.strip() for x in users_from_file]
        user_count = 1
        failed_users = []
        authrized_users = self.basic_measures.check_all_users(users_from_file)

        for user_name in users_from_file:
            if user_name in authrized_users['screen_name'].tolist():
                user = authrized_users[authrized_users['screen_name'] == user_name]
                self.users.append(user.to_dict(orient='records'))
                self.listbox.insert(0, user.to_dict(orient='records')[0]['screen_name'])
                print str(user_count) + '. ' + user.screen_name
                user_count += 1
            else:
                failed_users.append(user_name)
        if failed_users:
            tkMessageBox.showinfo("Add user", "Failed users:\n" + str(failed_users))
        else:
            tkMessageBox.showinfo("Add user", "All users added successfully")

    def add_user_on_click(self):
        user_name = self.entry_user.get()
        try:
            authrized_users = self.basic_measures.check_all_users([user_name])
            if user_name in authrized_users['screen_name'].tolist():
                user = authrized_users[authrized_users['screen_name'] == user_name]
                self.users.append(user.to_dict(orient='records'))
                self.listbox.insert(0, user.to_dict(orient='records')[0]['screen_name'])
                # user = self.basic_measures.api.get_user('@' + screen_name)
                # self.users.append(user)
        except:
            tkMessageBox.showinfo("Wrong Input", "No User Found")
            self.entry_user.delete(0, 'end')
