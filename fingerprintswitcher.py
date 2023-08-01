import subprocess
import os
import tempfile
import time
import json


class FingerprintSwitcher:
    def __init__(self, headless: bool = None, proxy: str = None):
        self.__temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.__process = None
        self.proxy = proxy
        self.headless = headless
        self.url = None

    def start(self):
        args = [
            "node",
            os.path.join(os.path.dirname(__file__), "index.js"),
            f"--user-data-dir={self.__temp_dir.name}"
        ]
        if self.headless:
            args.append("--headless")
        if self.proxy:
            args.append(f"--proxy={self.proxy}")
        self.__process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        while True:
            line = self.__process.stdout.readline().strip()
            if "this may take some time" in line:
                time.sleep(10)
                continue
            data = json.loads(line)
            if data["status"] == "error":
                raise Exception(data["message"])
            self.url = data["url"]
            break

    def stop(self):
        self.__process.terminate()
        self.__temp_dir.cleanup()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

fs = FingerprintSwitcher()
fs.start()
print(fs.url)
fs.stop()
