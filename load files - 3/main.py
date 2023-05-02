import vk_api
import requests
import os


def auth_handler():
    key = input("Enter 2FA code: ")
    remember_device = True
    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    group_id = GROUP_ID
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_sess = vk_session.get_api()
    album_id = vk_sess.photos.getAlbums(owner_id='-' + group_id, need_system=1)['items'][0]['id']
    for file in os.listdir('./static/img'):
        filepath = os.path.join('./static/img', file)
        if os.path.isfile(filepath):
            upload_url = vk_sess.photos.getUploadServer(album_id=album_id, group_id=group_id)['upload_url']
            with open(filepath, 'rb') as file:
                response = requests.post(upload_url, files={'photo': file}).json()
            vk_sess.photos.save(album_id=album_id, group_id=group_id, **response)[0]


if __name__ == '__main__':
    main()
