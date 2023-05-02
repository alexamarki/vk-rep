import vk_api
from flask import Flask, render_template

app = Flask(__name__)


def auth_handler():
    key = input("Enter 2FA code: ")
    remember_device = True
    return key, remember_device


def check_records(word, source_dict, dest_dict):
    if word in source_dict:
        dest_dict[word] += source_dict[word]


def vk_stat_agent(group_id):
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_sess = vk_session.get_api()
    try:
        all_stats = vk_sess.stats.get(group_id=group_id, intervals_count=10, fields=['activity', 'reach'])
    except Exception:
        return (), (), (), ()
    activities = {'likes': 0, 'comments': 0, 'copies': 0, 'subscribed': 0}
    cities = set()
    age = {'12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0, '27-30': 0, '30-35': 0, '35-45': 0, '45-100': 0}
    sex = {'female': 0, 'male': 0}
    for rec in all_stats:
        if 'activity' in rec:
            activity = rec['activity']
            check_records('likes', activity, activities)
            check_records('comments', activity, activities)
            check_records('copies', activity, activities)
            check_records('subscribed', activity, activities)
        reach_data = rec['reach']
        if 'cities' in reach_data and reach_data['cities']:
            if 'name' in reach_data['cities'][0]:
                for city in reach_data['cities']:
                    cities.add(city['name'])
        if 'sex' in reach_data and reach_data['sex']:
            if 'count' in reach_data['sex'][0]:
                sex['female'] += reach_data['sex'][0]['count']
                sex['male'] += reach_data['sex'][1]['count']
        if 'age' in reach_data:
            for age_group in range(len(age)):
                reach_age = reach_data['age'][age_group]
                age[reach_age['value']] += reach_age['count']
    return age, sex, activities, cities


@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    age, sex, activities, cities = vk_stat_agent(str(group_id))
    if not age:
        return render_template('stat.html', found=False)
    return render_template('stat.html', found=True, listed=(activities, sex, age), cities=cities,
                           list_of_headers=['Activities', 'Sexes', 'Ages'], title=f'Статистика ВК (club{group_id})')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
