import time
import multiprocessing
import subprocess
from infi.systray import SysTrayIcon
from pyuac import main_requires_admin
from codeopener.loop import loop
from codeopener.windows_native_notification import windows_native_notification
from codeopener.logger import log_file


def _loop():
        while True:
            windows_native_notification(loop())
            time.sleep(10)


def open_logs(_):
    subprocess.run(["PowerShell", "Get-Content", "-Path", log_file, "-Wait"])

menu_options = (("Logs", None, open_logs),)


@main_requires_admin
def main():
    loop_process = multiprocessing.Process(target=_loop)
    loop_process.start()

    def on_quit(_):
        loop_process.terminate()

    systray = SysTrayIcon("icon.ico", "Code Opener", menu_options, on_quit=on_quit)
    systray.start()


if __name__ == '__main__':
    main()
