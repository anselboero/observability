import json
import hashlib
import os
import git
import logging
from functools import reduce

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = json.JSONEncoder().default
json.JSONEncoder.default = _default

class Application:
    def __init__(self, name: str):
        self.name = name
        self.id = hashlib.md5(name.encode("utf-8")).hexdigest()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    # add a static method to fetch the name as the file name of the current script
    @staticmethod
    def fetch_file_name():
        return os.path.basename(os.path.realpath(__file__))

class ApplicationRepository:
    # primary key
    def __init__(self, location: str, application: Application):
        # Pk
        self.location = location
        # Pk
        self.application = application
        self.id = hashlib.md5(",".join([self.location, self.application.id]).encode("utf-8")).hexdigest()
    
    def to_json(self):
        return {
            "id": self.id,
            "location": self.location,
            "application": self.application.id
        }
    
    @staticmethod
    def fetch_git_location():
        code_repo = git.Repo(search_parent_directories=True).working_tree_dir.split("/")[-1]
        return code_repo
    
class DataSource:
    def __init__(self, location: str, server: str, format: str = None):
        self.location = location
        self.server = server
        self.id = hashlib.md5(",".join([self.location, self.server]).encode("utf-8")).hexdigest()

    # More helper methods should be added as the number of different data sources increases

class Schema:
    def __init__(self, fields: list, data_source: DataSource):
        """fields is a list of tuples list[tuple(name, type)]"""
        self.fields = fields
        self.data_source = data_source
        linearized_fields = ",".join(list(map(lambda x: f"{x[0]} - {x[1]}", sorted(self.fields) )))
        self.id = hashlib.md5(
            ",".join([linearized_fields, self.data_source.id]).encode("utf-8")
        ).hexdigest()

    def to_json(self):
        jfields = reduce(lambda x,y: dict (**x, **y), map(lambda f: {
            f[0]: f[1], self
        }))



# Instantiating and reporting
app = Application(Application.fetch_file_name())
logger.info(json.dumps(app))

app_repo = ApplicationRepository(ApplicationRepository.fetch_git_location(), app)
logger.info(json.dumps(app_repo))