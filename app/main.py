from controllers.telegram2anki import Telegram2AnkiController
import utils.logger


def run():
    Telegram2AnkiController().start_server()


if __name__ == '__main__':
    run()
