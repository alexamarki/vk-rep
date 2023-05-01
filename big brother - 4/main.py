import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN) #не знаю, нужно здесь прикладывать токен и id сообщества или нет (могу прислать, если необходимо)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_sess = vk_session.get_api()
            user_data = vk_sess.users.get(user_id=event.obj.message['from_id'], fields="city")[0]
            reply = f"Привет, {user_data['first_name']}!\n"
            if "city" in user_data:
                reply += f'Как поживает {user_data["city"]["title"]}?'
            vk_sess.messages.send(user_id=event.obj.message['from_id'],
                             message=reply,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
