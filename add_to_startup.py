import getpass
import os

USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

    with open("student-city-run.bat", "w") as start, open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'cd "" %s' % file_path)
        bat_file.write(r'start "" %s' % file_path)
