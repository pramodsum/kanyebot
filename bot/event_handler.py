import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # If message has an attachment
        # if 'previous_message' in event:
        #     msg = event['previous_message']
        #     print(msg)
        #     song = msg['title']
        #     link = msg['from_url']
        #     service = msg['service_name']

        #     # If message contains soundcloud link
        #     if 'Soundcloud' in service: 
        #         self.msg_writer.add_to_soundcloud(event['channel'], song, link, event)
        #     if 'Spotify' in service:
        #         self.msg_writer.add_to_spotify(event['channel'], song, link, event)

        # Filter out messages from the bot itself
        if 'user' in event: 
            if not self.clients.is_message_from_me(event['user']):

                msg_txt = event['text']

                # If message contains soundcloud link
                if 'https://soundcloud.com' in msg_txt: 
                    self.msg_writer.add_to_soundcloud(event['channel'], event['user'], event)
                if 'https://open.spotify.com' in msg_txt:
                    self.msg_writer.add_to_spotify(event['channel'], event['user'], event)

                if self.clients.is_bot_mention(msg_txt):
                    # e.g. user typed: "@pybot tell me a joke!"
                    if 'help' in msg_txt:
                        self.msg_writer.write_help_message(event['channel'])
                    elif re.search('hi|hey|hello|howdy|sup|yo', msg_txt):
                        self.msg_writer.write_greeting(event['channel'], event['user'])
                    elif 'joke' in msg_txt:
                        self.msg_writer.write_joke(event['channel'])
                    elif 'attachment' in msg_txt:
                        self.msg_writer.demo_attachment(event['channel'])
                    elif 'serenade' in msg_txt:
                        self.msg_writer.serenade(event['channel'])
                    else:
                        self.msg_writer.test_gif_response(event['channel'])
