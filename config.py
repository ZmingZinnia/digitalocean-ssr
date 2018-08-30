import settings

class Config(object):
    def __init__(self):
        pass

    def set(self, key, value):
        self.key = value

    def get(self, key):
        if hasattr(self, key):
            return self.__dict__[key]
        else:
            raise RuntimeError('do not find this property')


config = Config()

def load_config():
    attrs = dir(settings)
    for attr in attrs:
        if attr.startswith('__'):
            pass
        config.__dict__[attr] = settings.__dict__[attr]
    with open(config.public_key_file_path) as f:
        config.__dict__['public_key'] = f.read().strip('\n').strip('')
