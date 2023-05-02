import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def auth_handler():
    key = input("Enter 2FA code: ")
    remember_device = True
    return key, remember_device


def user_photo_agent(login, password, group_id):
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_sess = vk_session.get_api()
    album_id = vk_sess.photos.getAlbums(owner_id='-' + group_id, need_system=1)['items'][0]['id']
    photos = vk_sess.photos.get(album_id=album_id, owner_id='-' + group_id)
    photo = random.choice(photos['items'])
    photo_id = f"photo-{group_id}_{photo['id']}"
    return photo_id


def main():
    login, password = LOGIN, PASSWORD
    token = TOKEN
    group_id = GROUP_ID
    vk_session = vk_api.VkApi(
        token=token)
    longpoll = VkBotLongPoll(vk_session, group_id)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_sess = vk_session.get_api()
            name = vk_sess.users.get(user_id=event.obj.message['from_id'], fields="city")[0]['first_name']
            reply = f'Здравствуй, {name}!'
            photo = user_photo_agent(login, password, group_id)
            vk_sess.messages.send(user_id=event.obj.message['from_id'],
                                  message=reply,
                                  attachment=photo,
                                  random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
