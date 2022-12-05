from time import sleep

import vk_api
from config import token, id_app
import datetime

# for friend in session.method('friends.get', {'user_id': self.user_id})['items']:
#     person = session.method('users.get', {'user_id': friend})
#     for check in self.check_friends:
#         if f"{person[0]['first_name']} {person[0]['last_name']}" == check:
#             online_self = session.method('messages.getLastActivity', {'user_id': self.user_id})
#
#             if online_self['online'] == 0:
#                 timestamp_self = online_self['time']
#                 time_online_self = datetime.datetime.fromtimestamp(timestamp_self)
#                 online_self = time_online_self.strftime("%Y-%m-%d %H:%M:%S")
#             else:
#                 timestamp_self = online_self['time']
#                 time_online_self = datetime.datetime.fromtimestamp(timestamp_self)
#                 online_self = time_online_self.strftime("%Y-%m-%d %H:%M:%S")
#             online_friend = session.method('messages.getLastActivity', {'user_id': person[0]['id']})
#
#             if online_friend['online'] == 0:
#                 timestamp_friend = online_friend['time']
#                 time_online_friend = datetime.datetime.fromtimestamp(timestamp_friend)
#                 online_friend = time_online_friend.strftime("%Y-%m-%d %H:%M:%S")
#             else:
#                 timestamp_friend = online_friend['time']
#                 time_online_friend = datetime.datetime.fromtimestamp(timestamp_friend)
#                 online_friend = time_online_friend.strftime("%Y-%m-%d %H:%M:%S")


session = vk_api.VkApi(token=token)
vk = session.get_api()


class Persons:
    def __init__(self, user_id, package):
        self.user_id = user_id
        self.package = package

        self.check_friends = {}
        self.intermediate_check_online = {}
        self.not_friends = []
        self.active_friends = []
        sex = session.method('users.get', {'user_id': self.user_id, 'fields': 'sex'})
        self.user_sex = sex[0]['sex']

    def defining_friends(self):
        now_date = datetime.datetime.now()

        friends = session.method('friends.get', {'user_id': self.user_id, 'fields': 'sex'})
        for friend in friends['items']:
            friend_active = session.method('messages.getLastActivity', {'user_id': friend['id']})
            if friend_active['online'] == 0:
                timestamp = friend_active['time']
                time_online = datetime.datetime.fromtimestamp(timestamp)
                count_month = int(str(now_date)[5] + str(now_date)[6])
                count_month_activity = int(
                    str(time_online.strftime("%Y-%m-%d %H:%M:%S"))[5] + str(time_online.strftime("%Y-%m-%d %H:%M:%S"))[
                        6])
                if count_month - count_month_activity > 2:
                    self.not_friends.append(f"{friend['first_name']} {friend['last_name']}")

        for friend in friends['items']:
            if 'is_closed' in friend:
                if self.user_sex != friend['sex'] and f"{friend['first_name']} {friend['last_name']}" not in self.not_friends:
                    if not friend['is_closed']:
                        self.check_friends[f'{friend["first_name"]} {friend["last_name"]}'] = [{'overall_rating': 0},
                                                                                               {'private': False},
                                                                                               {'number_of_likes': 0},
                                                                                               {'number of comments': 0},
                                                                                               {'online': [0, 0]}]
                    else:
                        self.check_friends[f'{friend["first_name"]} {friend["last_name"]}'] = [{'overall_rating': 0},
                                                                                               {'private': True},
                                                                                               {'number_of_likes': 0},
                                                                                               {'number of comments': 0},
                                                                                               {'online': [0, 0]}]

    def check_online_friend(self):
        main_online = session.method('messages.getLastActivity', {'user_id': self.user_id})
        if main_online['online'] == 1:
            for friend in session.method('friends.get', {'user_id': self.user_id})['items']:
                person = session.method('users.get', {'user_id': friend})
                for check in self.check_friends:
                    if f"{person[0]['first_name']} {person[0]['last_name']}" == check:
                        online_self = session.method('messages.getLastActivity', {'user_id': self.user_id})

                        if online_self['online'] == 1:
                            timestamp_self = online_self['time']
                            time_online_self = datetime.datetime.fromtimestamp(timestamp_self)
                            online_self = time_online_self.strftime("%Y-%m-%d %H:%M:%S")

                        online_friend = session.method('messages.getLastActivity', {'user_id': person[0]['id']})
                        if online_friend['online'] == 1:
                            if main_online['online'] == 1:
                                timestamp_friend = online_friend['time']
                                time_online_friend = datetime.datetime.fromtimestamp(timestamp_friend)
                                online_friend = time_online_friend.strftime("%Y-%m-%d %H:%M:%S")
                                if check not in self.intermediate_check_online:
                                    self.intermediate_check_online[check] = 1
                                else:
                                    self.intermediate_check_online[check] += 1
                                print(f'Мой онлайн: {online_self}  Онлайн {check}: {online_friend}')
                            else:
                                break

        else:
            if len(self.intermediate_check_online) != 0:
                for friend_check in self.check_friends:
                    for friend_online in self.intermediate_check_online:
                        if friend_online == friend_check:
                            self.check_friends[friend_check][4]['online'][1] += self.intermediate_check_online[friend_online]

            self.intermediate_check_online = {}
            for check_friend in self.check_friends:
                print(f'{check_friend}: {self.check_friends[check_friend][4]["online"][1]} общее время в минутах')
            print('Не в сети!')

    def check_photos(self):
        test_likes = session.method('likes.getList', {'user_id': self.user_id, 'type': 'photo', 'item_id': id_app})
        print(test_likes)
        # for friend_id in session.method('friends.get', {'user_id': self.user_id})['items']:
        #     friend = session.method('users.get', {'user_id': friend_id})
        #     for check_friend in self.check_friends:
        #         if f"{friend[0]['first_name']} {friend[0]['last_name']}" == check_friend:
        #             photos_friend = session.method('likes.getList', {'user_id': self.user_id})
        #             print(photos_friend)


chel = Persons(user_id=448795909, package=1)
# 456035379
chel.defining_friends()
print(chel.check_friends)
count_time = 0
while True:
    count_time += 1
    chel.check_online_friend()
    sleep(60)
    if count_time == 100:
        for check_friend in chel.check_friends:
            if chel.check_friends[check_friend][4]["online"][1] != 0:
                print(f'{check_friend}: {chel.check_friends[check_friend][4]["online"][1]} минут || общее время онлайна')


