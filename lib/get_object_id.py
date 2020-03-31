import re
import os
filenameRegex = re.compile('R(\s|_).*(\s|_)N(\s|_).*(\s|_)')
def get_object_id(input):
    return filenameRegex.subn("", input)[0].replace(".fits", "")