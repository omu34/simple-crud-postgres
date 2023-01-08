from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    if not parser.has_section(section):
        raise Exception(
            f'Section{section} is not found in {filename} file')
    params = parser.items(section)
    return {param[0]: param[1] for param in params}


config()
