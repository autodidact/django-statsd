import socket
from contextlib import closing

from statsd.client import StatsClient

class StatsClient(StatsClient):
    """A client for statsd."""

    def __init__(self, host='localhost', port=8125, prefix=None,
                 maxudpsize=512, ipv6=False):
        """Create a new client."""
        fam = socket.AF_INET6 if ipv6 else socket.AF_INET
        family, _, _, _, addr = socket.getaddrinfo(
            host, port, fam, socket.SOCK_DGRAM)[0]
        self._family = family
        self._addr = addr
        self._prefix = prefix
        self._maxudpsize = maxudpsize

    def _send(self, data):
        """Send data to statsd."""
        with closing(socket.socket(self._family, socket.SOCK_DGRAM)) as conn:
            try:
                conn.sendto(data.encode('ascii'), self._addr)
            except (socket.error, RuntimeError):
                # No time for love, Dr. Jones!
                pass
