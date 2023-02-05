"""
Name: Chris Braley
Netid:braleych
PID: A60088768
How long did this project take you?


Sources:

"""
import string

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
        table = [()]

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
                print("Query:{}".format(query))
                print("Tokens: ", tokens)
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

                # todo integers, floats, misc. query stuff (select * for example)
                if query[0] in (string.digits):
                    query = remove_word(query, tokens)
                    continue

                if query[0] == "*":
                    continue

                if len(query) == len(old_query):
                    raise AssertionError("Query didn't get shorter.")

            return tokens

        tokens = tokenize(statement)
        if tokens[0] == "CREATE":       # CREATING A DB
            db = Database()             # Instantiate DB
            tbl = Table(tokens[2])      # Create a table with name (tokens[2] should always be name)
            db.add_table(tbl)           # Add table to DB
            data = []                   # Retreive data from query
            for i in range(4, tokens.index(')')):       # Should add a row to table, or column (still deciding)
                if tokens[i] == ',':
                    continue
                data.append(tokens[i])



        print("My toks:" ,tokens)

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


class Database(object): #Only need 1 database for project 1 so far.
    def __init__(self):
        """
        """
        self.tables = []
        self.name = ""

    def add_table(self, tbl):
        self.tables.append(tbl)


class Table(object):
    def __init__(self, name):
        self.name = name
        self.rows = [Row]


class Row(object):
    def __init__(self, name):
        self.name = name
        self.data = ()

#query = " INSERT   INTO instructors VALUES('James', 29, 17.5, NULL);"
query = "CREATE TABLE students (col1 INTEGER, col2 TEXT, col3 REAL);"
conn = Connection("test.db")
conn.execute(query)

print("Correct:" ,correct_tokens)