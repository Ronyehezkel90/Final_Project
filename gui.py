from Tkinter import *
from basic_measures import BasicMeasures
import tkMessageBox
import numpy as np
import matplotlib.pyplot as plt
from connector import Connector
import webbrowser


class GUI:
    def __init__(self):
        self.connector = None
        self.basic_measures = None
        self.authorization_type = None
        self.root = Tk()
        self.root.geometry('{}x{}'.format(500, 500))
        self.root.resizable(width=False, height=False)
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
        but_5 = Button(self.root, text="Search shortcut \nMeasures", fg="black", bd=5)
        but_6 = Button(self.root, text="Add user", fg="black", bg="gray", bd=5, command=self.add_user_frame_on_click)
        but_7 = Button(self.root, text="Remove user", fg="black", bg="gray", bd=5)

        but_1.grid(row=1, column=1, sticky=S)
        but_2.grid(row=2, column=1, sticky=S)
        but_3.grid(row=3, column=1, sticky=S)
        but_4.grid(row=4, column=1, sticky=S)
        but_5.grid(row=6, column=1, sticky=S)
        but_6.grid(row=7, column=0, sticky=S)
        but_7.grid(row=7, column=1, sticky=S)

        self.root.title("Twitter")

        self.root.mainloop()

    def add_user_frame_on_click(self):
        add_user_root = Tk()
        user = Label(add_user_root, text="Insert screen name:", font="-weight bold")
        self.entry_user = Entry(add_user_root)

        user.grid(row=1, columnspan=3)
        self.entry_user.grid(row=2, columnspan=3)

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

    def basic_measure_frame_on_click(self):
        dict_of_users_dicts = {}
        for user in self.users:
            dict_of_users_dicts[user.name] = self.basic_measures.get_all_basic_measures(user)

        # self.basic_measures_plot(dict_of_users_dicts)

    def add_user_on_click(self):
        screen_name = self.entry_user.get()
        try:
            user = self.basic_measures.api.get_user('@' + screen_name)
            self.users.append(user)
            self.listbox.insert(0, user.name)
        except:
            tkMessageBox.showinfo("Wrong Input", "No User Found")
        self.entry_user.delete(0, 'end')
