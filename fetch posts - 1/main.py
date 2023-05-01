import vk_api
import datetime


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
    posts = vk_sess.wall.get(count=5)
    if posts['items']:
        for i in posts['items']:
            dt_stamp = datetime.datetime.fromtimestamp(i['date'])
            dt_date = dt_stamp.strftime('%Y-%m-%d')
            dt_time = dt_stamp.strftime('%H:%M:%S')
            print(f"{i['text']};\ndate: {dt_date}, time: {dt_time}")


if __name__ == '__main__':
    main()
