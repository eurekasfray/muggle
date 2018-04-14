import json

from pathlib import Path

class Config:

    REPO_DIR_NAME = ".muggle"

    def __init__(self, filename, working_dir):
        self.working_dir = Path(working_dir)
        self.repo_dir = self.working_dir.joinpath(self.REPO_DIR_NAME)
        self.file = self.repo_dir.joinpath(filename)
        self.json = None
        self._load()

    def _load(self):
        if (not self.file.is_dir() and self.file.exists()):
            with open(self.file) as json_data:
                self.json = json.load(json_data)
        else:
            sys.exit("Could not find config file. Please provide a config file.")

    def wd(self):
        return self.working_dir

    def rd(self):
        return self.repo_dir

    def path(self):
        return self.file

    """
    host and port used in this program. host is localhost.
    In this way, you can visit the service (when it is running)
    in a browser at localhost:8888
    Or you can visit it manually for example through
    telnet localhost 8888

    returns tuple of (HOST, PORT)
    """
    def server_address(self):
        return (self.json['server']['host'], self.json['server']['port'])

    def server_host(self):
        return self.json['server']['host']

    def server_port(self):
        return int(self.json['server']['port'])

    def template_directory(self):
        return self.json['server']['template-directory']

    def template_file_name(self):
        return self.json['server']['template-filename']

    def template_file_path(self):
        return self.rd().joinpath(self.json['server']['template-directory'], self.json['server']['template-filename'])

    def notfound_file_path(self):
        return self.rd().joinpath(self.json['server']['template-directory'], self.json['server']['404-filename'])

    def index_file_name(self):
        return self.json['server']['directory-index']

    def dump(self):
        print(self.json)
