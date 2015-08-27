"""
This file provide class to spawn a SpeedRunsLive IRC bot.
"""
from irc.bot import SingleServerIRCBot

from .commands import SRLCommands


class SRLBot(SingleServerIRCBot):
    """
    Class to implement a SpeedRunsLive bot.
    """
    def __init__(self, server="irc.speedrunslive.com",
                 port=6667, channel="#speedrunslive",
                 nickname="Bot"):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.commands = SRLCommands()

    def on_nicknameinuse(self, connection, _):
        """
        Handle already used nickname.
        """
        print 'Nickname already used'
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, _):
        """
        Handle connection and Join channel.
        """
        print 'Connected to %s:%d' % (
            connection.server, connection.port
        )
        connection.join(self.channel)
        print 'Joined %s' % self.channel

    def on_pubmsg(self, _, event):
        """
        Handle message from public chat.
        """
        words = event.arguments[0].split(" ", 1)
        command = words[0]
        if command.startswith('.startrace') is True and len(words) >= 2:
            self.commands.do_startrace(words)