from Tkinter import *
import datetime
from activity_measures import ActivityMeasures
from basic_measures import BasicMeasures
import tkMessageBox
from connector import Connector
import webbrowser
import pandas as pd
from tkFileDialog import askopenfilename
from utils import get_current_time, handle_exception, sleep_15_min, remove_prob_users, get_default_date, get_dates, \
    write_files, finish_calculation
from conf import EXCEL_FILE, SYSTEM_TITLE, SYSTEM_DESCRIPTION, SYSTEM_CREATORS


class GUI:
    def __init__(self):
        self.connector = None
        self.root = Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.geometry('{}x{}'.format(600, 400))
        self.root.resizable(width=False, height=False)
        self.back_on_click()

    def login_gui(self):
        self.connector = Connector()
        Label(text=SYSTEM_TITLE, font=("Helvetica", 20)).pack(side=TOP, padx=10, pady=10)
        Label(text=SYSTEM_CREATORS, font=("Helvetica", 13)).pack(side=BOTTOM, padx=10, pady=10)
        Label(text=SYSTEM_DESCRIPTION, font=("Helvetica", 10)).pack(side=BOTTOM, padx=10, pady=10)
        user_login_button = Button(self.root, text="Login as twitter user", fg="white", bg="black", bd=5,
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
        if self.connector.user_authorization(verifier_code):
            self.basic_measures = BasicMeasures(self.connector)
            self.activity_measures = ActivityMeasures()
            self.clear_root_frame()
            self.create_gui()
        else:
            tkMessageBox.showinfo("Wrong Authorization", "Please check your code")

    def create_user_login_gui(self):
        self.clear_root_frame()
        Label(text='Please go to this address and authorize yourself\n').pack(side=TOP, padx=10, pady=10)
        link = Label(text='Authorization Link', fg="blue", cursor="hand2")
        link.pack()

        def callback(event):
            webbrowser.open_new(self.connector.auth.get_authorization_url())

        link.bind("<Button-1>", callback)
        Label(text='Enter your code').pack(side=TOP, padx=10, pady=10)
        '+self.connector.auth.get_authorization_url()+'
        entry = Entry(self.root, width=10)
        entry.pack(side=TOP, padx=10, pady=10)

        user_login_button = Button(self.root, text="Authorize", fg="white", bg="black", bd=5,
                                   command=lambda: self.user_authorization_button(entry.get()))
        user_login_button.pack(side=TOP, padx=10, pady=10)
        user_login_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        back_button = Button(self.root, text="Back", fg="white", bg="black", bd=5, command=self.back_on_click)
        back_button.pack(side=TOP, padx=10, pady=10)
        back_button.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.root.mainloop()

    def back_on_click(self):
        self.clear_root_frame()
        self.basic_measures = None
        self.activity_measures = None
        self.authorization_type = None
        self.users = []
        self.hashtags = []
        self.dates = None
        self.prob_users = {'not_active': [], 'protected': [], 'unknown_prob': []}
        self.login_gui()

    def login_controller(self, authorization_type):
        self.authorization_type = authorization_type
        self.create_user_login_gui() if self.authorization_type == 'user' else self.connector.application_authorization()
        self.basic_measures = BasicMeasures(self.connector)
        self.activity_measures = ActivityMeasures()
        self.clear_root_frame()
        self.create_gui()

    def create_gui(self):
        users_labels = Label(self.root, text="Users:", font="-weight bold")
        users_labels.grid(row=0, sticky=W)
        hashtags_labels = Label(self.root, text="Hashtags:", font="-weight bold")
        hashtags_labels.grid(row=0, column=1, sticky=W)
        self.listbox = Listbox(self.root, width=20, height=20)
        self.listbox.grid(row=1, rowspan=6)
        self.hashtags_listbox = Listbox(self.root, width=20, height=20)
        self.hashtags_listbox.grid(row=1, rowspan=6, column=1)

        but_date = Button(self.root, text="Choose Dates", fg="black", bg="gray", bd=5, command=self.date_frame_on_click)
        but_1 = Button(self.root, text="Calculate", fg="white", bg="black", bd=5,
                       command=self.basic_measure_frame_on_click)
        back_button = Button(self.root, text="Back", fg="white", bg="black", bd=5, command=self.back_on_click)
        but_2 = Button(self.root, text="Add Hashtags", fg="black", bg="gray", bd=5,
                       command=self.insert_hashtags_frame_on_click)
        but_6 = Button(self.root, text="Add user", fg="black", bg="gray", bd=5, command=self.add_user_frame_on_click)
        but_7 = Button(self.root, text="Remove", fg="black", bg="gray", bd=5, command=self.remove_user_on_click)
        but_8 = Button(self.root, text="Users File", fg="black", bg="gray", bd=5, command=self.add_users_from_file)
        but_9 = Button(self.root, text="Remove all", fg="black", bg="gray", bd=5,
                       command=self.remove_all_users_on_click)

        but_date.grid(row=1, column=2, sticky=S)
        but_1.grid(row=3, column=3, sticky=S)
        back_button.grid(row=4, column=3, sticky=S)
        but_2.grid(row=7, column=2, sticky=S)
        but_6.grid(row=2, column=2, sticky=S)
        but_7.grid(row=3, column=2, sticky=S)
        but_8.grid(row=4, column=2, sticky=S)
        but_9.grid(row=5, column=2, sticky=S)
        self.root.title("Twitter")
        self.root.mainloop()

    def slash_label(self, parent, row, column):
        slash = Label(parent, text="/")
        slash.grid(row=row, column=column, sticky=S)

    def set_dates(self):
        self.dates = get_dates(self.from_d.get(), self.from_m.get(), self.from_y.get(), self.to_d.get(),
                               self.to_m.get(), self.to_y.get())
        if self.dates:
            self.dates_root.destroy()
        else:
            tkMessageBox.showinfo("Wrong Input", "Wrong Date Format")

    def date_frame_on_click(self):
        from_row = 1
        to_row = 2
        d, m, y = get_default_date()
        self.dates_root = Tk()
        self.dates_root.wm_attributes("-topmost", 1)
        from_label = Label(self.dates_root, text="From Date: ", font="-weight bold")
        to_label = Label(self.dates_root, text="To Date: ", font="-weight bold")
        d_label = Label(self.dates_root, text="d")
        m_label = Label(self.dates_root, text="m")
        y_label = Label(self.dates_root, text="y")
        self.from_d = Entry(self.dates_root, width=2)
        self.from_m = Entry(self.dates_root, width=2)
        self.from_y = Entry(self.dates_root, width=4)
        self.to_d = Entry(self.dates_root, width=2)
        self.to_m = Entry(self.dates_root, width=2)
        self.to_y = Entry(self.dates_root, width=4)
        button = Button(self.dates_root, text="Set Dates", fg="black", bg="gray", bd=5, command=self.set_dates)
        d_label.grid(row=0, column=2, sticky=S)
        m_label.grid(row=0, column=4, sticky=S)
        y_label.grid(row=0, column=6, sticky=S)
        from_label.grid(row=from_row, column=1, sticky=W)
        self.from_d.grid(row=from_row, column=2, sticky=S)
        self.slash_label(self.dates_root, from_row, 3)
        self.from_m.grid(row=from_row, column=4, sticky=S)
        self.slash_label(self.dates_root, from_row, 5)
        self.from_y.grid(row=from_row, column=6, sticky=S)
        to_label.grid(row=to_row, column=1, sticky=W)
        self.to_d.grid(row=to_row, column=2, sticky=S)
        self.slash_label(self.dates_root, to_row, 3)
        self.to_m.grid(row=to_row, column=4, sticky=S)
        self.slash_label(self.dates_root, to_row, 5)
        self.to_y.grid(row=to_row, column=6, sticky=S)
        button.grid(row=to_row + 3, column=4, sticky=S)
        self.from_d.insert(END, str(d))
        self.from_m.insert(END, str(m))
        self.from_y.insert(END, str(y - 1))
        self.to_d.insert(END, str(d))
        self.to_m.insert(END, str(m))
        self.to_y.insert(END, str(y))

        self.dates_root.title("Twitter - Choose Dates")
        self.dates_root.geometry("300x100")

    def hashtag_alert(self):
        tkMessageBox.showinfo("HELP",
                              "Insert HASHTAG or list of HASHTAGS separated by comma\nFor Example: elections2017,DonaldTrump,HillaryCllinton")

    def add_hashtag_on_click(self):
        hashtag_list = self.entry_hashtag.get()
        hashtag_list = hashtag_list.split(",")
        for hashtag in hashtag_list:
            self.hashtags.append(hashtag.lower())
            self.hashtags_listbox.insert(0, hashtag)

    def insert_hashtags_frame_on_click(self):
        add_user_root = Tk()
        add_user_root.wm_attributes("-topmost", 1)
        hashtag_label = Label(add_user_root, text="Insert HASHTAG(S)", font="-weight bold")
        self.entry_hashtag = Entry(add_user_root)
        hashtag_label.grid(row=1, column=1)
        self.entry_hashtag.grid(row=2, column=1)
        dot_2 = Label(add_user_root, text=".", fg="gray")
        but_1 = Button(add_user_root, text="ReadMe", bd=5, width=15, command=self.hashtag_alert)
        but_2 = Button(add_user_root, text="Add", bd=5, width=15, command=self.add_hashtag_on_click)
        dot_2.grid(row=3, sticky=W)
        but_1.grid(row=4, column=1, sticky=S)
        but_2.grid(row=5, column=1, sticky=S)
        add_user_root.title("Twitter - Add HASHTAG")
        add_user_root.geometry("250x150")

    def remove_all_users_on_click(self):
        for idx, user in enumerate(self.users):
            del (self.users[idx])
        self.listbox.delete(0, END)
        self.prob_users = {'not_active': [], 'protected': [], 'unknown_prob': []}

    def remove_user_on_click(self):
        if len(self.listbox.curselection()) == 1:
            list_index = self.listbox.curselection()[0]
            user_name = self.listbox.get(list_index)
            for idx, user in enumerate(self.users):
                if user[0]['screen_name'] == user_name:
                    del (self.users[idx])
                    break
            self.listbox.delete(list_index)
        elif len(self.hashtags_listbox.curselection()) == 1:
            list_index = self.hashtags_listbox.curselection()[0]
            hashtag = self.hashtags_listbox.get(list_index)
            for idx, user in enumerate(self.hashtags):
                if user == hashtag:
                    del (self.hashtags[idx])
                    break
            self.hashtags_listbox.delete(list_index)
        else:
            tkMessageBox.showinfo("Remove None", "Please choose user/hashtag to remove")

    def add_user_frame_on_click(self):
        self.add_user_root = Tk()
        self.add_user_root.wm_attributes("-topmost", 1)
        user = Label(self.add_user_root, text="Insert screen name:", font="-weight bold")
        self.entry_user = Entry(self.add_user_root)
        user.grid(row=1, columnspan=3)
        self.entry_user.grid(row=2, columnspan=3)
        self.entry_user.insert(0, '')
        dot_2 = Label(self.add_user_root, text=".", fg="gray")
        but_2 = Button(self.add_user_root, text="Add User", bd=5, width=15, command=self.add_user_on_click)
        dot_2.grid(row=3, sticky=W)
        but_2.grid(row=4, column=2, sticky=S)
        self.add_user_root.title("Twitter - Add User")
        self.add_user_root.geometry("250x150")

    def calculate_basic_measures(self, user, dict_of_users_dicts, results_df, count_users):
        screen_name = user[0]['screen_name']
        dict_of_users_dicts[screen_name] = self.basic_measures.get_all_basic_measures(user, self.hashtags, self.dates)
        df = pd.DataFrame([dict_of_users_dicts[screen_name]])
        df['USER'] = screen_name
        results_df = results_df.append(df)
        print str(count_users) + '. ' + screen_name + ' ::: ' + get_current_time()
        return results_df

    def calculate_activity_measures(self, user, dict_of_users_dicts):
        screen_name = user[0]['screen_name']
        activity_dict = self.activity_measures.get_all_activity_measures(dict_of_users_dicts[screen_name])
        for measure in activity_dict:
            dict_of_users_dicts[screen_name][measure] = activity_dict[measure]

    def add_user_based_measures_to_dataframe(self, df, dict_of_users_dicts):
        df['m3'] = df['USER'].apply(lambda user_name: self.basic_measures.mentions['total_mentions'][user_name])
        df['m4'] = df['USER'].apply(lambda user_name: self.basic_measures.mentions['user_mentions'][user_name])
        df['mention_impact'] = df['USER'].apply(lambda user_name: dict_of_users_dicts[user_name]['mention_impact'])
        activity_measures = [item for item in dict_of_users_dicts.values()[0].keys() if item not in list(df.columns)]
        for measure in activity_measures:
            df[measure] = df['USER'].apply(lambda user_name: dict_of_users_dicts[user_name][measure])

    def set_gui_status(self, screen_name, count_users, ):
        self.current_user_label.config(text='Current User: ' + screen_name)
        self.out_of_label.config(text="Calculated: " + str(count_users) + " / " + str(len(self.users)))
        # every 14 users more or less the system wait for 15 min.
        # each user takes 10 sec
        self.remain_time = datetime.datetime.strptime('00:00', '%H:%M')
        remain_users = len(self.users) - count_users
        self.remain_time = self.remain_time + datetime.timedelta(minutes=int(15 * (remain_users / 14.0)))
        self.remain_time = self.remain_time + datetime.timedelta(seconds=remain_users * 5)
        self.estimated_label.config(text="Estimated Time Remaining: " + str(self.remain_time.time()))
        self.root.update()

    def run_basic_calculation(self):
        dict_of_users_dicts = {}
        count_users = 0
        results_df = pd.DataFrame()
        for user in self.users:
            screen_name = user[0]['screen_name']
            self.set_gui_status(screen_name, count_users)
            try:
                results_df = self.calculate_basic_measures(user, dict_of_users_dicts, results_df, count_users)
                results_df.to_excel(EXCEL_FILE, index=False)
                count_users += 1
            except Exception as e:
                exception_case = handle_exception(e, screen_name, count_users)
                try:
                    if exception_case == 429:
                        sleep_15_min(self)
                        results_df = self.calculate_basic_measures(user, dict_of_users_dicts, results_df, count_users)
                    elif exception_case == 401:
                        self.prob_users['protected'].append(screen_name)
                    else:
                        self.prob_users['unknown_prob'].append(screen_name)
                except Exception as e:
                    print screen_name + ' --- Failed after failure - e: ' + e.message
        return results_df, dict_of_users_dicts

    def run_advanced_calculation(self, results_df, dict_of_users_dicts):
        self.users = remove_prob_users(self.prob_users, self.users)
        self.basic_measures.calculate_user_based_measures(dict_of_users_dicts)
        for user in self.users:
            self.calculate_activity_measures(user, dict_of_users_dicts)
        self.add_user_based_measures_to_dataframe(results_df, dict_of_users_dicts)
        return results_df

    def ready_for_calculation(self):
        try:
            excel_file = open(EXCEL_FILE, "r+")
        except IOError:
            tkMessageBox.showinfo("Permission problem", "Please close excel '"+EXCEL_FILE+"' File")
            return False
        if not self.users:
            tkMessageBox.showinfo("No users", "Please add users first")
            return False
        return True

    def basic_measure_frame_on_click(self):
        if self.ready_for_calculation():
            print 'calculation started: ' + get_current_time()
            self.clear_root_frame()
            self.calculation_title_label = Label(self.root, text="CALCULATING", font=("-weight bold", 20))
            self.current_user_label = Label(self.root, text="Current User:", font=20)
            self.out_of_label = Label(self.root, text="Calculated: 0 / " + str(len(self.users)), font=20)
            self.estimated_label = Label(self.root, text="Estimated Time Remaining: ", font=20)
            pad = 20
            self.calculation_title_label.pack(side=TOP, padx=pad, pady=pad)
            self.current_user_label.pack(side=TOP, padx=pad, pady=pad)
            self.out_of_label.pack(side=TOP, padx=pad, pady=pad)
            self.estimated_label.pack(side=TOP, padx=pad, pady=pad)
            results_df, dict_of_users_dicts = self.run_basic_calculation()
            results_df = self.run_advanced_calculation(results_df, dict_of_users_dicts)
            write_files(self, results_df)
            finish_calculation()
            self.back_on_click()

    def add_users_from_file(self):
        Tk().withdraw()
        file_name = askopenfilename()
        with open(file_name) as f:
            users_from_file = f.readlines()
        users_from_file = [x.strip() for x in users_from_file if x != '' and x != '\n']
        user_count = 1
        authrized_users = self.basic_measures.check_all_users(users_from_file)
        for user_name in users_from_file:
            if user_name in authrized_users['screen_name'].tolist():
                user = authrized_users[authrized_users['screen_name'] == user_name]
                self.users.append(user.to_dict(orient='records'))
                self.listbox.insert(0, user.to_dict(orient='records')[0]['screen_name'])
                print str(user_count) + '. ' + user.screen_name
                user_count += 1
            else:
                self.prob_users['not_active'].append(user_name)
        if self.prob_users['not_active']:
            failed_users = ''
            for failed_user in self.prob_users['not_active']:
                failed_users += failed_user + '\n'
            tkMessageBox.showinfo("Add user", "Failed users:\n" + failed_users)
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
                self.add_user_root.destroy()
        except:
            tkMessageBox.showinfo("Wrong Input", "No User Found")
        self.entry_user.delete(0, 'end')
