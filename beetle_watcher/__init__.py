from sys import stdout
import time

from watchdog.observers import Observer


class Watcher(object):
    last_render = 0

    def __init__(self, context, config):
        self.context = context
        self.config = config
        self.folders = context.config.folders

    def _start_observer(self):
        self.observer = Observer()
        self.observer.schedule(self, self.folders['content'], recursive=True)
        self.observer.schedule(self, self.folders['templates'], recursive=True)
        self.observer.schedule(self, self.folders['include'], recursive=True)
        self.observer.start()

    def _stop_observer(self):
        self.observer.stop()
        self.observer.join()

    def watch(self):
        self.dispatch(None)
        self._start_observer()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._stop_observer

    def dispatch(self, _):
        # Guard against multiple renders triggered by the same event
        if self.last_render + 0.1 > time.time():
            return

        stdout.write('Rendering site... ')
        stdout.flush()

        try:
            self.context.commander.run('render')
            print('Done')
        except Exception as error:
            print('\nError occured during rendering: {}'.format(error))

        self.last_render = time.time()


def register(context, plugin_config):
    watcher = Watcher(context, plugin_config)
    context.commander.add('watcher', watcher.watch, 'Watch input files and do a render on changes')
