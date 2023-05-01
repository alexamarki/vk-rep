import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.fVda2xRs1I8GZZ7sNo8cpH2NADunCf5qPcDaKuJz6AKAWjsfXj6MIlxa74FI8XyH1av7T6aZUy9XOTAMY_XfK-Gx5YkVa9JOuAWp8DjbCTnZfkCGfJ8P--Yz2O2Flsld6NdxQm7JMA2XymPLqoj8hWF1ZYeX1BZE3ziqXR3RyzL9z_MT8wYApvjP3C91tC8R55tfoUykTsapIlc6_FRZeA')
    longpoll = VkBotLongPoll(vk_session, 220256793)
    wikipedia.set_lang("ru")
    question_resolved = True
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_sess = vk_session.get_api()
            if question_resolved:
                reply = "Здравствуйте! Введите запрос для того, чтобы получить краткое содержание " \
                        "соответствующей страницы на Википедии"
                question_resolved = False
            else:
                try:
                    reply = wikipedia.summary(event.obj.message['text'])
                    question_resolved = True
                except wikipedia.exceptions.DisambiguationError:
                    reply = 'Ваш запрос слишком обширен. Пожалуйста, уточните'
                except wikipedia.exceptions.PageError:
                    reply = 'Страниц, соответствующих данному запросу, нет. Попробуйте еще раз'
            vk_sess.messages.send(user_id=event.obj.message['from_id'],
                                  message=reply,
                                  random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
