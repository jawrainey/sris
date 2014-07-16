import config


class Databases(object):
    """
    Used to make interaction with several databases easier.
    """
    def __init__(self):
        """
        Imports & assigns each module specified in the config to an attribute.
        This allows for access to the submodule, e.g. Databases.{name}.{method}
        """
        for name in config.DATABASE_NAMES:
            setattr(self, name, __import__(name, globals=globals()))
