import signal


class SignalHandler:
    exit_now = False

    def __init__(self):
        """
        Add callbacks for signals
        """
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        """
        Callbacks should cause main process to stop
        """
        self.exit_now = True
