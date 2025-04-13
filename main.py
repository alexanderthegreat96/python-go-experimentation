from PyGo import PyGo, detect_go_platform
binary_path : str = f'go-binaries/{detect_go_platform()}/cli-app'

go_data : dict = {
    "name": "Alex",
    "age": 29
}

pygo : PyGo = PyGo(executable_file_path=binary_path)
pygo.send(go_data)
    
result = pygo.receive()
if result is None:
    print("Error:", pygo.get_error())
else:
    print("Output from Go executable:", result)