"""
Name: Chris Braley
Netid:braleych
PID: A60088768
How long did this project take you?


Sources:

"""

_ALL_DATABASES = {}


class Connection(object):
    def __init__(self, filename):
        """
        Takes a filename, but doesn't do anything with it.
        (The filename will be used in a future project).
        """
        pass

    def execute(self, statement):
        """
        Takes a SQL statement.
        Returns a list of tuples (empty unless select statement
        with rows to return).
        """
        raise NotImplementedError("To Be Done")

    def close(self):
        """
        Empty method that will be used in future projects
        """
        pass


def connect(filename):
    """
    Creates a Connection object with the given filename
    """
    return Connection(filename)


class Database(object):
    pass


class Table(object):
    pass


class Row(object):
    pass
