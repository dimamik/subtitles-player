import inspect
import logging


class CssManager:
    @staticmethod
    def get_css_as_string(cls):
        path = inspect.getfile(cls.__class__).replace(".py", ".css")
        css_to_return = ""
        try:
            with open(path) as file:
                css_to_return = file.read()
        except FileNotFoundError:
            logging.error("File not found")
            exit(-1)
        except IOError:
            logging.error("IOError")
            exit(-1)
        return css_to_return
