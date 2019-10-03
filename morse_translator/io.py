def write_to_file(string, file_path):
    """Writes a string into a file, replacing existing file if it exists"""
    with open(file_path, "w") as file:
        file.write(string)


def read_from_file(file_path):
    """Reads the contents of a file and returns it as a string"""
    with open(file_path, "r") as file:
        return file.read()
