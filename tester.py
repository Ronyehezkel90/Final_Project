import datetime

from basic_measures import BasicMeasures
import unittest
from activity_measures import ActivityMeasures
from connector import Connector
import pandas as pd

from utils import get_current_time


class MyTestCase(unittest.TestCase):
    def test_activity_measures(self):
        activity_measures = ActivityMeasures()
        print activity_measures.tweet_count_score()
        ron = 2

    def test_all_basics(self):
        basic_measures = BasicMeasures()
        user = basic_measures.api.get_user('@' + 'djalbo')
        basics = basic_measures.get_all_basic_measures(user)
        ron = 2

    def test_get_followers(self):
        connector = Connector()
        connector.application_authorization()
        basic_measures = BasicMeasures(connector)
        followers = basic_measures.get_all_followers()
        ron = 2

    def test_sample_run(self):
        dict_of_users_dicts = {}
        connector = Connector()
        connector.application_authorization()
        basic_measures = BasicMeasures(connector)
        activity_measures = ActivityMeasures()
        users_names = ['ronyehezkel90']
        authrized_users = basic_measures.check_all_users(users_names)
        users = []
        count_users = 0
        results_df = pd.DataFrame()
        user = authrized_users[authrized_users['screen_name'] == users_names[0]]
        users.append(user.to_dict(orient='records'))
        # self.users.append(user.to_dict(orient='records'))
        for user in users:
            screen_name = user[0]['screen_name']
            dict_of_users_dicts[screen_name] = basic_measures.get_all_basic_measures(user)
            dict_of_users_dicts[screen_name].update(
                activity_measures.get_all_activity_measures(dict_of_users_dicts[screen_name]))
            df = pd.DataFrame([dict_of_users_dicts[screen_name]])
            df['USER'] = screen_name
            results_df = results_df.append(df)
            results_df.to_excel('test.xlsx', index=False)
            print str(count_users) + '. ' + screen_name + ' ::: ' + get_current_time()

            count_users += 1
        print 'Measures file is ready!'

    def check_user_mean_time(self):
        time = datetime.datetime.strptime('03:55', '%H:%M').time()
        print time
        times=[]
        with open('log') as f:
            content = f.readlines()
        for line in content:
            if ':::' in line:
                times.append(line[line.find('::: ')+4:-1])
        ron=2


