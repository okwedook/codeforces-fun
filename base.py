import requests
import time
import random
import hashlib
import subprocess

CODEFORCES_API = "https://codeforces.com/api/"

def fill_tilde(file_name):
    return subprocess.check_output(f"echo {file_name}", shell=True)[:-1]

class Requester:
    def __init__(self, key_file_name = "~/.codeforces/key", secret_file_name = "~/.codeforces/secret"):
        key_file_name = fill_tilde(key_file_name)
        secret_file_name = fill_tilde(secret_file_name)
        self.key = open(key_file_name, "r").read()
        self.secret = open(secret_file_name, "r").read()

    def getSig(self, handler, params):
        rand = str(random.randint(100000, 999999))
        joined_params = "&".join(
            f"{key}={value}"
            for key, value in sorted(params.items())
        )
        return hashlib.sha512(
            bytes(
                f"{rand}/{handler}?{joined_params}#{self.secret}",
                encoding="utf-8"
            )
        )

    def make_api_query(self, handler, params):
        params = {
            "time": int(time.time()),
            "key": self.key,
            **params
        }

        params["apiSig"] = self.getSig(handler, params)

        try:
            response = requests.get(f"{CODEFORCES_API}{handler}", params=params)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return response.json()