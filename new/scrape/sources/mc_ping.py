
import json

from twisted.internet import reactor, task
from twisted.internet.protocol import ClientFactory, Protocol

from scrape.sources import Source

class MinecraftPingProtocol(Protocol):
    buf = ""
    def connectionMade(self):
        self.transport.write("\x06\x00\x05\x00\x00\x00\x01\x01\x00")

    def connectionLost(self, reason=None):
        self.factory.stopFactory()

    def dataReceived(self, data):
        self.buf += data

        b = self.buf

        try:
            _, b = self.unpackVarint(b) # packet length
            _, b = self.unpackVarint(b) # packet id
            l, b = self.unpackVarint(b)
            if l != len(b):
                raise IndexError()

            data = json.loads(b)
            self.factory.got_data(data)
            self.transport.loseConnection()

        except IndexError:
            pass

    def unpackVarint(self, data):
        o = 0
        for i in range(5):
            d = data[i]
            o |= (d & 0x7F) << 7*i
            if not d & 0x80:
                return o, data[i+1:]


class MinecraftPingFactory(ClientFactory):
    protocol = MinecraftPingProtocol


class IRCSource(Source):
    def start(self):
        task.LoopingCall(self.update).start(10*60)
    def update(self):
        factory = IRCFactory()
        factory.got_users = self.got_users
        reactor.connectTCP("irc.gamesurge.net", 6667, factory)

    def got_users(self, count):
        self.api_call("update_cache",
            key="IRC_USERS_CURRENT",
            value=count)

source = IRCSource