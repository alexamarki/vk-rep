import vk_api


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
    photos = vk_sess.photos.get(album_id=album_id, owner_id='-' + group_id)
    for photo in photos['items']:
        print('URL:', photo['sizes'][-1]['url'])
        print('Размеры:', photo['sizes'][-1]['width'], 'x', photo['sizes'][-1]['height'])


if __name__ == '__main__':
    main()
