from datetime import datetime


class NameGenerator:
    @classmethod
    def generate_name(cls, extension, prefix=None, root=None, suffix=None):
        """
        Generates filename based on arguments:
        prefix + root + current_time + suffix + "." + extension
        :return: generated filename
        """
        to_ret = ""
        curr_date = str(datetime.now()).replace(":", "-") \
            .replace(" ", "-").split(".")[0]
        if prefix:
            to_ret += prefix
        if root:
            to_ret += root
        to_ret += curr_date
        if suffix:
            to_ret += suffix
        to_ret += "." + extension
        return to_ret

    @classmethod
    def extract_filename_from_path(cls, string):
        return string.split("/")[-1].split(".")[0]
