# SpotifyFollowedPlaylistsTransfer
Move across playlists that you follow from one Spotify account to another.   
There are many applications such as SpotMyBackup that allow you to import/export songs within playlists. This is great for playlists that are created by you, but what about playlists that you would like to follow rather than recreate?   
That is where this script comes to play! This script will gather all followed playlists from one account, and then follow those playlists in another account.

## Prerequisites:
1. Login to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) and create a new application. You should then be able to view the Client ID and Client Secret in the top left corner of the webpage. In order to create a new Redirect URI, click edit settings in the top right corner in the dashboard and add a new Redirect URI *`e.g. http://localhost:0000/callback`*. Add these to values to the respective functions in the `secrets_manager.py` file.

2. [Spotipy](https://spotipy.readthedocs.io/en/2.9.0/) : Spotipy is a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform.
    - For Python 2.7 users: `python pip install spotipy`
    - For Python 3.6 usersL `python3 -m pip install spotipy --user spotipy`

## Steps:
1. Update necessary parameters in `secrets_manager.py` and then run the script.
2. Login to the **source** Spotify account i.e. the account which holds the playlists you want to transfer over.
3. The script should automatically open a browser window and request acceptance to progress further. Once accepted, the browser will then redirect. Copy the URL and paste into the terminal. 
Note that this occurs twice due to limitations with Spotify's API which requires two different scopes to obtain collaborative and private playlists.
4. Login to the **target** Spotify account i.e. the account which you want to add the playlists to.
5. Once again, the script should automatically open a browser window and request acceptance to progress further. Once accepted, the browser will then redirect. Copy the URL and paste into the terminal.
6. All playlists should now be transferred over!

## Screenshots
![Image of script introduction message](https://github.com/methumano/SpotifyFollowedPlaylistsTransfer/blob/master/screenshots/Img1.png)
![Image of results after running script](https://github.com/methumano/SpotifyFollowedPlaylistsTransfer/blob/master/screenshots/Img2.png)
