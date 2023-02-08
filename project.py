"""
Name: Chris Braley
Netid:braleych
PID: A60088768
How long did this project take you?


Sources:

"""
import string

import setuptools

_ALL_DATABASES = {}

correct_tokens = [
    "INSERT",
    "INTO",
    "instructors",
    "VALUES",
    "(",
    "James",
    ",",
    29,
    ",",
    17.5,
    ",",
    None,
    ")",
    ";"
]

class Database(object): #Only need 1 database for project 1 so far.
    def __init__(self):
        """
        """
        self.tables = []
        self.name = ""

    def add_table(self, tbl):
        self.tables.append(tbl)

    def get_table(self, name):
        for tbl in self.tables:
            if name == tbl.name:
                return tbl

class Table(object):
    def __init__(self, name):
        self.name = name
        self.types = []
        self.rows = []
        self.colnames = []

    def set_types(self, data):
        for elem in data:
            if elem == "INTEGER" or elem == "TEXT" or elem == "REAL": # Store table types, in order with a list
                self.types.append(elem)
            else:
                self.colnames.append(elem)  # Also store column names

    def add_row(self, data):            # Should be called during INSERT
        lst = []
        for i in range(len(data)):          #Conversions of data eg ('James', 29, 3.5)
            if data[i] is None:
                lst.append(None)
                continue
            if self.types[i] == "INTEGER":
                lst.append(int(data[i]))
            if self.types[i] == "TEXT":
                lst.append(str(data[i]))
            if self.types[i] == "REAL":
                lst.append(float(data[i]))
        row = Row(lst)
        self.rows.append(row)

    def get_rows(self, keys):
        lst = []
        for row in self.rows:



        #
        print(lst)
class Row(object):
    def __init__(self):
        self.data = ()

    def __init__(self, lst):
        self.data = tuple(lst)

    def __repr__(self):
        s = ''
        for i in range(len(self.data)):
            s += self.data[i] + " "
        return s

db = Database()

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

        def collect_characters(query, allowed_characters):
            letters = []
            for letter in query:
                if letter not in allowed_characters:
                    break
                letters.append(letter)
            return "".join(letters)

        def remove_leading_whitespace(query, tokens):
            whitespace = collect_characters(query, string.whitespace)
            return query[len(whitespace):]

        def remove_word(query, tokens):
            word = collect_characters(query,
                                      string.ascii_letters + "_" + string.digits + ".")
            if word == "NULL":
                tokens.append(None)
            elif "." in word:
                tokens.append(float(word))
            elif word.isdigit():
                tokens.append(int(word))
            else:
                tokens.append(word)
            return query[len(word):]

        def remove_text(query, tokens):
            assert query[0] == "'"
            query = query[1:]
            end_quote_index = query.find("'")
            text = query[:end_quote_index]
            tokens.append(text)
            query = query[end_quote_index + 1:]
            return query

        def tokenize(query):
            tokens = []
            while query:
                #print("Query:{}".format(query))
                #print("Tokens: ", tokens)
                old_query = query

                if query[0] in string.whitespace:
                    query = remove_leading_whitespace(query, tokens)
                    continue

                if query[0] in (string.ascii_letters + "_"):
                    query = remove_word(query, tokens)
                    continue

                if query[0] in "(),;":
                    tokens.append(query[0])
                    query = query[1:]
                    continue

                if query[0] == "'":
                    query = remove_text(query, tokens)
                    continue

                # xtodo integers, floats, misc. query stuff (select * for example)
                if query[0] in (string.digits):
                    query = remove_word(query, tokens)
                    continue

                if query[0] == "*":
                    tokens.append(query[0])
                    query = query[1:]
                    continue

                if len(query) == len(old_query):
                    raise AssertionError("Query didn't get shorter.")

            return tokens

        tokens = tokenize(statement)

        if tokens[0] == "CREATE":
            #db = Database()  # Instantiate DB
            #_ALL_DATABASES[1] = db      # CREATING A DB
            tbl = Table(tokens[2])      # Create a table with name (tokens[2] should always be name)
            data = []                   # Retreive data from query
            for i in range(4, tokens.index(')')):       # Should add a row to table
                if tokens[i] == ',':
                    continue
                data.append(tokens[i])
            tbl.set_types(data)
            db.add_table(tbl)  # Add table to DB

        if tokens[0] == "INSERT":
            tbl = db.get_table(tokens[2])  # ??? Maybe? Would create a new table after every insert is called
            data = []
            for i in range(5, tokens.index(')')):
                if tokens[i] == ',':
                    continue
                data.append(tokens[i])
            tbl.add_row(data)

        if tokens[0] == "SELECT":
            lst = []
            if tokens[1] == "*":
                tbl = db.get_table(tokens[3])
                for row in tbl.rows:
                    lst.append(row.data)
            else:
                cols = []
                tbl = db.get_table(tokens[tokens.index("FROM") + 1])
                for i in range(1, tokens.index("FROM")):
                    if tokens[i] == ',':
                        continue
                    cols.append(tokens[i])

                tbl.get_rows(cols)
                tmp = []
                # for i in range(len(cols)):
                #     for x in range(len(tbl.colnames)):
                #         if cols[i] == tbl.colnames[x]:
                #             for row in tbl.rows:
                #                 tmp.append(row.data[x])





            return lst


        return []

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


conn = Connection("test.db")
query = "CREATE TABLE student (name TEXT, grade REAL);"
conn.execute(query)
query = "INSERT INTO student VALUES ('James', 1.5);"
conn.execute(query)
query = "INSERT INTO student VALUES ('Yaxin', 4.0);"
conn.execute(query)
query = "INSERT INTO student VALUES ('Li', 3.2);"
conn.execute(query)
query = "SELECT grade, name FROM student ORDER BY name;"
conn.execute(query)
print("Completed")