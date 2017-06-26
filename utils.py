from time import strftime, gmtime
import time
import datetime
import copy

from conf import SUMMARY_FILE, REORDER, EXCEL_FILE


def get_current_time():
    return str(strftime("%H:%M:%S", gmtime()))


def write_summary_to_file(model, results_df):
    all_users = list(results_df['USER'].values) + model.prob_users['not_active'] + model.prob_users['protected'] + \
                model.prob_users['unknown_prob']
    flag = '****************'
    f = open(SUMMARY_FILE, 'w')
    f.write(flag + '   Dates   ' + flag + '\n')
    f.write('From Date: ' + str(model.basic_measures.dates['from']) + '\n')
    f.write('To Date: ' + str(model.basic_measures.dates['to']) + '\n')
    f.write(flag + '   Users   ' + flag + '\n')
    f.write('Total users: ' + str(len(all_users)) + '\n')
    f.write('Calculated users: ' + str(len(results_df['USER'].values)) + '\n')
    f.write('Non-Active users: ' + str(len(model.prob_users['not_active'])) + '\n')
    f.write('Protected users: ' + str(len(model.prob_users['protected'])) + '\n')
    f.write('Unknown Problem users: ' + str(len(model.prob_users['unknown_prob'])) + '\n')
    f.write(flag + '   HashTags   ' + flag + '\n')
    f.write('HashTags: ' + str(model.hashtags) + '\n')
    for hashtag in model.hashtags:
        f.write('\t' + hashtag + '\n')
    f.write(flag + '   Users Detailed   ' + flag + '\n')
    f.write('Total users: ' + '\n')
    for user in all_users:
        f.write('\t' + user + '\n')
    f.write('Calculated Users:\n')
    for user in results_df['USER'].values:
        f.write('\t' + user + '\n')
    f.write('Non-Active Users:\n')
    for user in model.prob_users['not_active']:
        f.write('\t' + user + '\n')
    f.write('Protected Users:\n')
    for user in model.prob_users['protected']:
        f.write('\t' + user + '\n')
    f.write('Unknown Problem Users:\n')
    for user in model.prob_users['unknown_prob']:
        f.write('\t' + user + '\n')

    f.close()

def update_sleep_timer(gui, time_passed):
    gui.current_user_label.config(text='TWITTER rate limiting has been reached.\nThe system is in Sleep-Mode for 15 minutes,\n'+str(time_passed)+' minutes passed.')
    gui.estimated_label.config(text="Last Estimated Time Remaining: " + str(gui.remain_time.time()))
    gui.root.update()

def sleep_15_min(gui):
    i = 0
    while i <= 16:
        update_sleep_timer(gui, i)
        time.sleep(60)
        i += 1
        print str(i) + ' min passed'


def get_dates(from_d, from_m, from_y, to_d, to_m, to_y):
    try:
        from_date = datetime.datetime.strptime(from_d + from_m + from_y, '%d%m%Y')
        to_date = datetime.datetime.strptime(to_d + to_m + to_y, '%d%m%Y')
        dates = {'from': from_date, 'to': to_date}
        if from_date >= to_date:
            return None
        return dates
    except:
        return None


def get_default_date():
    curr_date = datetime.datetime.now()
    return curr_date.day, curr_date.month, curr_date.year


def remove_prob_users(prob_users_dict, all_users):
    all_users_without_prob = copy.deepcopy(all_users)
    for user in all_users:
        if user[0]['screen_name'] in prob_users_dict['protected'] + prob_users_dict['unknown_prob']:
            all_users_without_prob.remove(user)
    return all_users_without_prob


def handle_exception(e, screen_name, count_users):
    print e
    if e.__class__.__name__ is 'TweepError':
        print 'Reason: ' + e.response.reason + '\nStatus Code: ' + str(e.response.status_code)
        return e.response.status_code
    else:
        print 'EXCEPTION!!!!! - User: ' + screen_name + ' - User Number:' + str(count_users)


def write_files(model, results_df):
    results_df = results_df[REORDER]
    results_df.to_excel(EXCEL_FILE, index=False)
    write_summary_to_file(model, results_df)
