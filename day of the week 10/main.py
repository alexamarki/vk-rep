import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import locale
import datetime
import re

locale.setlocale(locale.LC_ALL, 'ru_RU')


def reply_msg(session, event, text):
    session.messages.send(user_id=event.obj.message['from_id'],
                          message=text,
                          random_id=random.randint(0, 2 ** 64))


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    base_reply = 'Я могу сказать, какой день недели был в ту или иную дату!\nПросто назови мне дату ' \
                 'в формате ГГГГ-ММ-ДД в своем сообщении, а я скажу тебе день ' \
                 'недели.\nP.S.: На данный момент считывается только первая подходящая по формату дата в сообщении'
    initiated = False
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk_sess = vk_session.get_api()
            text = event.obj.message['text']
            if not initiated:
                reply_msg(vk_sess, event, base_reply)
                initiated = True
                continue
            match = re.findall('\d{4}-\d{2}-\d{2}', text)
            if match:
                date = match[0]
                try:
                    dt_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    reply_msg(vk_sess, event, dt_obj.strftime('%A').capitalize())
                except Exception:
                    reply_msg(vk_sess, event, "Ошибка с датой. Пожалуйста, попробуйте еще раз.")
                    continue

            else:
                reply_msg(vk_sess, event, 'В сообщении нет даты в необходимом формате. Попробуйте еще раз :)')
                continue



if __name__ == '__main__':
    main()
