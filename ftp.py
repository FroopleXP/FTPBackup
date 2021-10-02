import ftplib
from os import error, path

MAX_RETRIES = 10


class FTP:

    def __init__(self, host, user, password, port=21) -> None:
        self._host = host
        self._user = user
        self._password = password
        self._port = port
        self._client = ftplib.FTP(host=self._host)
        self._retries = 0

    def connect(self) -> None:
        try:
            self._client.connect(port=self._port)
            self._client.login(self._user, self._password)

        except ftplib.error_perm:
            raise error("Failed to login")

        except OSError:
            raise error("Failed to connect to %s" % self._host)

    # Test is the connection is stable, if not retry
    def _isstableconn(self) -> bool:
        try:
            self._client.voidcmd("NOOP")
            return True

        except IOError:
            if self._retries < MAX_RETRIES:
                self._retries += 1
                self.connect()
                return self._isstableconn()
            self._retries = 0
            return False

    # Send single file
    def sendfile(self, dir, to):
        if not self._isstableconn():
            raise error("Failed to send file, connection not stable")

        try:
            # Open file
            file = open(dir, "rb")
            filename = path.basename(file.name)

            self._client.cwd(to)
            self._client.storbinary("STOR %s" % filename, file)

        except ftplib.error_perm as e:
            raise error("FTP permission issue: %s" % e)

        except OSError:
            raise FileNotFoundError("Failed to open '%s'" % dir)

        finally:
            file.close()
            self._client.close()
