# Python ↔ Go Communication

This project demonstrates how to use Go's performance from Python by calling Go executables and exchanging data through standard input and output.

This approach does not use Python bindings or `cgo`. Instead, it treats Go as a separate CLI program that can be called from Python.

## Goal

- Build Go logic into a standalone binary.
- Pass data from Python to Go using stdin.
- Read data from Go using stdout.
- Keep both sides decoupled and language-agnostic.

## Project Structure

 - go-binaries/`architecture`/cli-app.exe
 - go-binaries/`architecture`/cli-app
 - main.go -> go code
 - main.py -> python code


### General Idea
 - you need a list of constants to define architecture (these constants need to exist in both codebases. we are going to use these for the calling the correct binary for the platform we currenly work with)
 - a common way to communicate:
    - since we are using args to communicate, we can pass a json string and expect back, you guessed right, another json string

### Use Cases
 - say we got a large dataset of structured data, either stored in a database or file
 - we want to leverage go's concurrency and parallelism to perform full-text search or maybe analyze something

### Usage Example
```python
from PyGo import PyGo, detect_go_platform

# you can set this manually
binary_path : str = f'go-binaries/{detect_go_platform()}/cli-app'

# the data you want to send to your go binary
go_data : dict = {
    "name": "Alex",
    "age": 29
}

# call the class
pygo : PyGo = PyGo(executable_file_path=binary_path)

# send your data
pygo.send(go_data)

# receive your data
result = pygo.receive()
if result is None:
    print("Error:", pygo.get_error())
else:
    print("Output from Go executable:", result)
```