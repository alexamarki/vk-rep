import vk_api
import calendar


def auth_handler():
    key = input("Enter 2FA code: ")
    remember_device = True
    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_sess = vk_session.get_api()
    friends = vk_sess.friends.get(fields="bdate")
    friend_list = []
    if friends['items']:
        for i in friends['items']:
            friend_profile = {}
            friend_profile["name"] = i["first_name"]
            friend_profile["surname"] = i["last_name"]
            if "bdate" in i:
                date = i["bdate"].split(".")
                month_day = " ".join((calendar.month_name[int(date[1])], date[0]))
                if len(date) < 3:
                    friend_profile["bdate"] = month_day
                else:
                    friend_profile["bdate"] = ", ".join((month_day, date[2]))

            else:
                friend_profile["bdate"] = "Date unavailable"
            friend_list.append(friend_profile)
        friends_sorted = sorted(friend_list, key=lambda x: x["surname"])
        for j in friends_sorted:
            name_full = ' '.join((j["surname"], j["name"])) #Для красивого отображения
            print(f'{name_full:<30}{j["bdate"]:>30}')
    else:
        print('No friends :(')


if __name__ == '__main__':
    main()
