import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
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
