from tkinter import *
from basic_measures import BasicMeasures
import tkMessageBox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.root = Tk()
        self.basic_measures = BasicMeasures()
        self.users = []

    def create_gui(self):
        # dot_1 = Label(self.root, text=".", fg="gray")
        # dot_1.grid(row=7, sticky=W)

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
        my_xticks =''
        max_value=0
        for user_dict in dict_of_users_dicts.values():
            x= np.arange(user_dict.__len__())
            plt.plot(x, user_dict.values())
            my_xticks=user_dict.keys()
            if max(user_dict.values())>max_value:
                max_value = max(user_dict.values())
        plt.xticks(x, my_xticks)
        # y= np.arange(max_value+1)
        plt.show()

    def basic_measure_frame_on_click(self):
        dict_of_users_dicts = {}
        for user in self.users:
            dict_of_users_dicts[user.name] = self.basic_measures.get_all_basic_measures(user)
        self.basic_measures_plot(dict_of_users_dicts)



    def add_user_on_click(self):
        screen_name = self.entry_user.get()
        try:
            user = self.basic_measures.api.get_user('@' + screen_name)
            self.users.append(user)
            self.listbox.insert(0, user.name)
        except:
            tkMessageBox.showinfo("Wrong Input", "No User Found")
        self.entry_user.delete(0, 'end')
