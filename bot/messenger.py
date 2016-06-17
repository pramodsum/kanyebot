import logging
import random
import requests
import soundcloud
from ghost import Ghost

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

        # log into soundcloud account
        self.scClient = soundcloud.Client(client_id='37aa5b54501a7ab82d4c207816619f99',
                           client_secret='94c8f5abf9cd7724675eea56c0125c91',
                           username='sumu@cookinginpjs.com',
                           password='kanyebot123',
                           scope='non-expiring')

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)

    def test_gif_response(self, channel_id):
        attachment = {
            "pretext": "HAAANH?!?!?",
            "image_url": "http://s3.amazonaws.com/rapgenius/tumblr_me2bakjLPb1qlsrn9o1_500.gif",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, '', attachments=[attachment], as_user='true')

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def serenade(self, channel_id):
        ghost = Ghost()
        page, resources = ghost.open("http://www.kanyerest.xyz/serenade/")
        self.send_message(channel_id, ghost.content)

    def add_to_soundcloud(self, channel_id, user_id, msg):
        # Cleanup link 
        link = msg['text']
        link = link[1:len(link) - 1]

        # Get soundcloud playlist
        playlist = self.scClient.get('/playlists/234288095')

        # Get all tracks currently in playlist
        tracks = []
        for track in playlist.tracks:
            tracks += [{'id': track['id']}]

        # Adding new track to end of playlist
        new_track = self.scClient.get('/resolve', url=link)

        username = self.scClient.get('/me').username

        # make sure track isn't already in playlist
        if any(track['id'] == new_track.id for track in tracks):
            txt = "\"" + new_track.title + "\" wasn't added because it already exists in Boxer Tunes."
            self.send_message(channel_id, txt)
        else:
            tracks = [{'id': new_track.id}] + tracks

            # Updating playlist
            self.scClient.put(playlist.uri, playlist={
                'tracks': tracks
            })

            txt = username + "added \"" + new_track.title + "\" to the Boxer Tunes soundcloud playlist"
            self.send_message(channel_id, txt)

    def add_to_spotify(self, channel_id, user_id, msg):
        txt = '{} posted a spotify link to {}'.format(user_id, msg)
        self.send_message(channel_id, txt)

