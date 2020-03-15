import sys
import spotipy
import spotipy.util as util
from secrets_manager import secrets_manager


def introduction():
    """Brief description of script and its functions"""
    print(
        'This script allows you to migrate the playlists that you follow from one account to another.\n'
        'During the process, your browser will automatically open and you will be asked to agree to allow '
        'this script to access your profile.\n''This is required in order to carry out actions.\n')
    input("Press Enter to continue...")


def get_client(scope, username):
    """Creates Spotify client"""
    secrets = secrets_manager()
    try:
        token = util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=secrets.client_id,
                                           client_secret=secrets.client_secret,
                                           redirect_uri=secrets.redirect_uri)
        client = spotipy.Spotify(auth=token)
        return client
    except:
        sys.exit(
            '\nCould not create client. Please ensure details entered are correct.\n')


def get_playlists():
    """Gathers list of all playlist ids and respective owner ids from source account"""
    id_list = []
    scope_list = ['playlist-read-private', 'playlist-read-collaborative']
    username = input('\nPlease enter the username ID of the source account\n')
    input('\nPlease open a browser window and login to the source Spotify account.\n'
          'Press enter to continue...\n')
    for scope in scope_list:
        client = get_client(scope, username)
        results = client.current_user_playlists()
        x = results['items']
        for item in x:
            a = list(item['external_urls'].values())
            playlist_id = [element.split("/playlist/", 1)[1] for element in a]
            b = list(item['owner']['external_urls'].values())
            owner_id = [element.split("/user/", 1)[1] for element in b]
            playlist_name = [item['name']]
            combined = playlist_id + owner_id + playlist_name
            id_list.append(combined)
    return id_list


def add_playlists(id_list):
    """Adds playlists from list into target account"""
    scope = 'playlist-modify-public'
    username = input('\nPlease enter the username ID of the target account\n')
    input('\nNow log out of the source Spotify account and login to the target Spotify account.\n'
          'Press enter to continue...')
    client = get_client(scope, username)
    count = 0
    for item in id_list:
        playlist_id = item[0]
        owner_id = item[1]
        client.user_playlist_follow_playlist(
            playlist_id=playlist_id, playlist_owner_id=owner_id)
        print('Adding playlist: ', item[2])
        count += 1
    print('\nA total of', str(count),
          'playlists have been transferred successfully!')


if __name__ == "__main__":
    introduction()
    add_playlists(get_playlists())
