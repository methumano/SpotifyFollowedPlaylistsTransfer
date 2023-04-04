import urllib.parse
import base64
import requests
import json
import webbrowser

from secrets_manager import secrets_manager


def introduction():
    """Brief description of script and its functions"""
    print(
        'This script allows you to migrate the playlists that you follow from one account to another.\n'
        'During the process, your browser will automatically open and you will be asked to agree to allow '
        'this script to access your profile.\n''This is required in order to carry out actions.\n')
    input("Press Enter to continue...")


def get_token(scope):
    """Obtain access token"""
    secrets = secrets_manager()
    encoded_redirect_uri = urllib.parse.quote(secrets.redirect_uri, safe='')

    webbrowser.open(
        f'https://accounts.spotify.com/authorize?client_id={secrets.client_id}&response_type=code&redirect_uri={encoded_redirect_uri}&scope={scope}'
    )

    user_response = input(
        '\nPlease allow the web app the necessary permissions to function...'
        f'\nOnce you have done this, you will be automatically redirected to a new webpage.'
        '\nPlease copy the URL and paste below...\n')

    authorisation_code = user_response.split('code=')[1]
    b64_encoded_credentials = base64.urlsafe_b64encode(f'{secrets.client_id}:{secrets.client_secret}'.encode()).decode()
    headers = {'Authorization': f'Basic {b64_encoded_credentials}'}
    data = {'grant_type': 'authorization_code', 'code': authorisation_code, 'redirect_uri': secrets.redirect_uri}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return json.loads(response.text).get('access_token')

def get_playlists():
    """Gathers list of all playlist ids and respective owner ids from source account"""
    id_list = []
    scope_list = ['playlist-read-private', 'playlist-read-collaborative']
    input('\nPlease open a browser window and login to the source Spotify account.\n'
          'Press Enter once you are logged in and ready to continue...\n')
    for scope in scope_list:
        token = get_token(scope)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        for offset in range(0, 1000, 50):
            results = requests.get(f'https://api.spotify.com/v1/me/playlists?limit=50&offset={offset}', headers=headers)
            print(results)
            x = json.loads(results.text).get('items')
            for item in x:
                a = list(item['external_urls'].values())
                playlist_id = [element.split("/playlist/", 1)[1] for element in a]
                b = list(item['owner']['external_urls'].values())
                owner_id = [element.split("/user/", 1)[1] for element in b]
                playlist_name = [item['name']]
                combined = playlist_id + owner_id + playlist_name
                id_list.append(combined)
            if len(x) != 50:
                print(f'Offset limit: {offset}')
                break
    print(id_list)
    return id_list


def add_playlists(id_list):
    """Adds playlists from list into target account"""
    scope = 'playlist-modify-public'
    input('\nPlease open a browser window and login to the target Spotify account.\n'
          'Press Enter once you are logged in and ready to continue...\n')
    token = get_token(scope)
    count = 0
    for item in id_list:
        playlist_id = item[0]
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        data = {'public': 'false'}
        requests.put(f'https://api.spotify.com/v1/playlists/{playlist_id}/followers', headers=headers, data=data)
        print('Adding playlist: ', item[2])
        count += 1
    print('\nA total of', str(count),
          'playlists have been transferred successfully!')


if __name__ == "__main__":
    introduction()
    add_playlists(get_playlists())
