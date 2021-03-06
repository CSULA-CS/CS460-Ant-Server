# A service that starts everything else, and make connection between server and
# worker easier instead of relying on the socket connection

import tournament_manager
import web_server
import threading
import mananger

import sys


class WebThread(threading.Thread):
    def __init__(self, manangerThread):
        threading.Thread.__init__(self)
        self.manangerThread = manangerThread

    def run(self):
        web_server.main(2080, self.manangerThread)


class TCPThread(threading.Thread):
    def __init__(self, manangerThread):
        threading.Thread.__init__(self)
        self.manangerThread = manangerThread

    def run(self):
        tournament_manager.main(manangerThread)


class ManangerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        mananger.main()

    def addBot(self, cmd, botname):
        mananger.addBot(cmd, botname)


if __name__ == '__main__':

    try:
        manangerThread = ManangerThread()
        manangerThread.daemon = True
        tcpthread = TCPThread(manangerThread)
        tcpthread.daemon = True
        webthread = WebThread(manangerThread)
        webthread.daemon = True

        tcpthread.start()
        webthread.start()
        manangerThread.start()

        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        sys.exit()