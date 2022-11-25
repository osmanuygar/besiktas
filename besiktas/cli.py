from .screen import Application, Footballers, Stats
import argparse

def main():
    parser = argparse.ArgumentParser(description='Besiktas ClI')
    parser.add_argument('-kadro', action='store_true', help='Besiktas Squad')
    parser.add_argument('-stats', action='store_true', help='Top Scorers')
    args = parser.parse_args()
    if args.kadro is False and args.stats is False:
        try:
            screen = Application()
            screen.setup()
            screen.run()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print(ex)

    if args.kadro:
        try:
            screen = Footballers()
            screen.setup()
            screen.run()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print(ex)

    if args.stats:
        try:
            screen = Stats()
            screen.setup()
            screen.run()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print(ex)
