from besiktas.screen import Application, Footballers
import argparse


def main():
    parser = argparse.ArgumentParser(description='Besiktas ClI')
    parser.add_argument('kadro', nargs='?', const='foo')
    args = parser.parse_args()
    if args.kadro is None:
        try:
            screen = Application()
            screen.setup()
            screen.run()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print(ex)

    else:
        try:
            screen = Footballers()
            screen.setup()
            screen.run()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print(ex)



main()
