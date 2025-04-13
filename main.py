#!python

import platform
import json
import subprocess

# we're using what build.sh currenly has
# since the compiled binaries are going to be found under
# go-binaries/<PLATFORM_ARCH>

PLATFORM_ARCH_MAP = {
    ("linux", "x86_64"):     "linux/amd64",
    ("linux", "amd64"):      "linux/amd64",
    ("linux", "i386"):       "linux/386",
    ("linux", "i686"):       "linux/386",
    ("linux", "x86"):        "linux/386",
    ("linux", "arm64"):      "linux/arm64",
    ("linux", "aarch64"):    "linux/arm64",
    ("linux", "armv7l"):     "linux/arm",
    ("linux", "armv6l"):     "linux/arm",
    ("linux", "arm"):        "linux/arm",

    ("darwin", "x86_64"):    "darwin/amd64",
    ("darwin", "amd64"):     "darwin/amd64",
    ("darwin", "arm64"):     "darwin/arm64",

    ("freebsd", "x86_64"):   "freebsd/amd64",
    ("freebsd", "amd64"):    "freebsd/amd64",
    ("freebsd", "i386"):     "freebsd/386",
    ("freebsd", "i686"):     "freebsd/386",

    ("openbsd", "x86_64"):   "openbsd/amd64",
    ("openbsd", "amd64"):    "openbsd/amd64",
    ("openbsd", "i386"):     "openbsd/386",
    ("openbsd", "i686"):     "openbsd/386",
}

# this function simply tells us which platform we are on
# so we know which go binary we can call

def detect_go_platform():
    key = (platform.system().lower(), platform.machine().lower())
    return PLATFORM_ARCH_MAP.get(key, "unsupported")


go_query : dict = {
    "name": "Alex",
    "age": 29
}

binary_path : str = f'go-binaries/{detect_go_platform()}/cli-app'

proc = subprocess.Popen(
    [binary_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

input_data = json.dumps(go_query).encode("utf-8")
stdout, stderr = proc.communicate(input=input_data)

if proc.returncode != 0:
    print("Error:", stderr.decode())
else:
    response = json.loads(stdout.decode())
    print("Go says:", response["message"])