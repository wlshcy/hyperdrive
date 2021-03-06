import os
import signal

import eventlet

from hyperdrive import wsgi
from hyperdrive.common import log as logging
from hyperdrive.common import cfg
from hyperdrive.common.cfg import Int
from hyperdrive.common import importutils

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class WSGIService(object):
    def __init__(self, name):
        self.name = name
        self.loader = wsgi.Loader()
        self.app = self.loader.load_app(self.name)
        self.host = getattr(CONF, "%s_bind_host" % self.name)
        self.port = Int(getattr(CONF, "%s_bind_port" % self.name))
        self.workers = Int(CONF.workers)
        self.server = wsgi.Server(self.name,
                                  self.app,
                                  self.host,
                                  self.port)

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def wait(self):
        self.server.wait()


class ServerWrapper(object):
    def __init__(self, server, workers):
        self.server = server
        self.workers = workers
        self.children = set()


class Launcher(object):
    @staticmethod
    def run_service(service):
        service.start()
        service.wait()


class ProcessLauncher(object):
    def __init__(self, wait_interval=0.01):
        self.children = {}
        rfd, self.writepipe = os.pipe()
        self.running = True
        self.wait_interval = wait_interval

        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        # SIGKILL can not be catch
        # signal.signal(signal.SIGKILL,self._handle_signal)

    def _handle_signal(self, signo, frame):
        LOG.debug("master received SIGTERM or SIGINT...")
        self.running = False

    def _child_process(self, server):
        eventlet.hubs.use_hub()

        os.close(self.writepipe)

        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        launcher = Launcher()
        launcher.run_service(server)

    def _start_child(self, wrap):
        pid = os.fork()
        if pid == 0:
            try:
                self._child_process(wrap.server)
            finally:
                wrap.server.stop()
            os._exit(0)
        wrap.children.add(pid)
        self.children[pid] = wrap

    def _wait_child(self):
        pid, status = os.waitpid(0, os.WNOHANG)
        if pid not in self.children:
            return None
        wrap = self.children.pop(pid)
        wrap.children.remove(pid)
        return wrap

    def launch_server(self, server, workers=1):
        wrap = ServerWrapper(server, workers)
        while len(wrap.children) < wrap.workers:
            self._start_child(wrap)

    def wait(self):
        while self.running:
            wrap = self._wait_child()
            if not wrap:
                eventlet.greenthread.sleep(self.wait_interval)
                continue
            while len(wrap.children) < wrap.workers:
                self._start_child(wrap)

        LOG.debug("master is going to die,kill workers first...")
        for pid in self.children:
            os.kill(pid, signal.SIGTERM)

        while self.children:
            self._wait_child()
