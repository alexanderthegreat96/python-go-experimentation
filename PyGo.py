import json
import base64
import subprocess
from typing import Union, Optional
from pathlib import Path
import platform

# Mapping of (OS, architecture) to GOOS/GOARCH strings.
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

def detect_go_platform() -> str:
    """
    Detect the current platform in GOOS/GOARCH format.

    Returns:
        A string representing the platform, e.g., "linux/amd64",
        or "unsupported" if the platform is not recognized.
    """
    key = (platform.system().lower(), platform.machine().lower())
    return PLATFORM_ARCH_MAP.get(key, "unsupported")


class PyGo:
    """
    A class to handle communication with a Go executable.

    This class sends input to the Go binary (optionally encoded in Base64)
    and decodes the output (if it was Base64 encoded) received via stdout.
    """
    def __init__(self, executable_file_path: Optional[str] = None, use_encoding: bool = False) -> None:
        """
        Initialize PyGo with an optional path to the Go executable.

        Args:
            executable_file_path: Path to the Go executable.
            use_encoding: Whether to encode input/output using Base64.
        """
        self.__executable_file_path: Optional[str] = None
        self.__input_data: Optional[bytes] = None
        self.__output_data: Optional[bytes] = None
        self.__error: Optional[str] = None
        self.__use_encoding: bool = use_encoding

        if executable_file_path:
            self.set_executable_path(executable_file_path)

    def set_executable_path(self, path: str) -> None:
        """
        Set the path to the Go executable.

        Args:
            path: Path to the executable file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        exec_path = Path(path)
        if not exec_path.is_file():
            self.__error = f"Executable not found: {exec_path}"
        self.__executable_file_path = str(exec_path)

    def get_executable_path(self) -> Optional[str]:
        """
        Get the current executable path.

        Returns:
            The path to the executable if set, otherwise None.
        """
        return self.__executable_file_path

    def get_error(self) -> Optional[str]:
        """
        Retrieve the last error message.

        Returns:
            The error message as a string, or None if no error.
        """
        return self.__error

    def get_raw_output(self) -> Optional[bytes]:
        """
        Get the raw output bytes from the Go process.

        Returns:
            The raw output, or None if not set.
        """
        return self.__output_data

    def __encode_input(self, data: Union[str, dict]) -> bytes:
        """
        Encode input data into bytes, optionally using Base64.

        Args:
            data: A string or dictionary to encode.

        Returns:
            Encoded bytes.
        """
        if isinstance(data, dict):
            # Convert dict to JSON string.
            data = json.dumps(data)
        raw_bytes = data.encode("utf-8")
        if self.__use_encoding:
            return base64.b64encode(raw_bytes)
        return raw_bytes

    def __decode_output(self, data: bytes) -> Union[str, dict]:
        """
        Decode output data from bytes, optionally decoding Base64.

        Args:
            data: Raw output bytes from the process.

        Returns:
            The decoded output as a dictionary (if valid JSON) or a string.
        """
        if self.__use_encoding:
            try:
                # Decode Base64 first.
                decoded = base64.b64decode(data).decode("utf-8")
                return json.loads(decoded)
            except (json.JSONDecodeError, UnicodeDecodeError, base64.binascii.Error):
                return data.decode("utf-8", errors="ignore")
        else:
            raw_string = data.decode("utf-8", errors="ignore")
            try:
                return json.loads(raw_string)
            except json.JSONDecodeError:
                return raw_string

    def send(self, input_buffer: Union[str, dict]) -> None:
        """
        Encode and store the input data to send to the Go executable.

        Args:
            input_buffer: Input data as a string or dictionary.
        """
        self.__input_data = self.__encode_input(input_buffer)

    def receive(self) -> Union[str, dict, None]:
        """
        Run the Go binary, pass the input data via stdin, and decode the stdout output.

        Returns:
            The decoded output, or None if an error occurred.
        """
        self.__error = None
        self.__output_data = None

        if not self.__executable_file_path:
            self.__error = "Executable path not set"
            return None

        exec_path = Path(self.__executable_file_path)
        if not exec_path.is_file():
            self.__error = f"Executable not found: {exec_path}"
            return None

        try:
            proc = subprocess.Popen(
                [str(exec_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate(input=self.__input_data)

            if proc.returncode != 0:
                self.__error = stderr.decode("utf-8")
                return None

            self.__output_data = stdout
            return self.__decode_output(stdout)
        except Exception as e:
            self.__error = str(e)
            return None
