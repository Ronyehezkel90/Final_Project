from tkinter import *
import first
import connector
import basic_measures


class Application(Frame):
    """ GUI """

    def __init__(self, master):
        """initialize the frame"""
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.button = Button(self, text="Get User's Tweets", command=self.build_list)
        self.button1 = Button(self, text="Get Statuses", command=first.get_ten_statuses)
        self.button2 = Button(self, text="Tweet Rank", command=self.tweet_rank)
        self.button3 = Button(self, text="Tweet Count Score", command=self.tweet_count_score)
        self.button4 = Button(self, text="General Activity", command=self.general_activity)
        self.button5 = Button(self, text="Signal Strength", command=self.signal_strength)
        self.label2 = Label(self, text="Result: ")
        self.text_box_2 = Entry(self)

        self.button.pack()
        self.button1.pack()
        self.text_box_2.pack(side=LEFT)
        self.label2.pack(side=LEFT)
        self.text_box_2.insert(0, "@JohnAlexanderMP")

    def build_list(self):
        self.get_tweets()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()

    def tweet_rank(self):
        count = first.count_by_measure('TweetRank')
        self.label2['text'] = "Result: ", count

    def tweet_count_score(self):
        count = first.count_by_measure('TweetCountScore')
        self.label2['text'] = "Result: ", count

    def general_activity(self):
        count = first.general_activity()
        self.label2['text'] = "Result: ", count

    def signal_strength(self):
        count = first.signal_strength()
        self.label2['text'] = "Result: ", count

    def get_tweets(self):
        user_name = self.text_box_2.get()
        print(user_name)
        connector.get_tweets(user_name)


root = Tk()
root.title("Twitter")
root.geometry("400x500")

app = Application(root)
root.mainloop()
