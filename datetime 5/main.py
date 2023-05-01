import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.fVda2xRs1I8GZZ7sNo8cpH2NADunCf5qPcDaKuJz6AKAWjsfXj6MIlxa74FI8XyH1av7T6aZUy9XOTAMY_XfK-Gx5YkVa9JOuAWp8DjbCTnZfkCGfJ8P--Yz2O2Flsld6NdxQm7JMA2XymPLqoj8hWF1ZYeX1BZE3ziqXR3RyzL9z_MT8wYApvjP3C91tC8R55tfoUykTsapIlc6_FRZeA')
    longpoll = VkBotLongPoll(vk_session, 220256793)
    moscow_delta = datetime.timedelta(hours=3)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_sess = vk_session.get_api()
            msg = event.obj.message['text']
            reply = ''
            if any(word in msg.lower() for word in ["время", "дата", "число", "день"]):
                dt_obj = datetime.datetime.utcnow() + moscow_delta
                reply = f'Сегодня {dt_obj.strftime("%A")}, {dt_obj.strftime("%d %B, %Y")}. В Москве сейчас {dt_obj.strftime("%H час(а/ов), %M минут(а/ы), %S секунд(а/ы)")}'
            else:
                reply = f'Спросите меня о времени, дне, дате или числе и я скажу вам их.'
            vk_sess.messages.send(user_id=event.obj.message['from_id'],
                             message=reply,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
