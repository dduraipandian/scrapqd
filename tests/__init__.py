import sys
import subprocess


class MockServer:
    def __init__(self):
        self.process = subprocess.Popen([sys.executable, '-m', "scrapqd"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)
        count = 0
        for line in iter(self.process.stdout.readline, ''):
            if "* debug mode: off" in line.decode().lower() or count == 10:
                break
            count += 1

    def __del__(self):
        self.process.terminate()
        self.process.communicate()
