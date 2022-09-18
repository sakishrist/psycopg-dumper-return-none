from psycopg.types.datetime import DateDumper
import psycopg

# ---------------------------------------------------------------------------- #
#                                    HELPERS                                   #
# ---------------------------------------------------------------------------- #

# Custom type because python's type doesn't like negative dates
class SQLDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self):
        return f'SQLDate({self.year:04}-{self.month:02}-{self.day:02})'

    def __nonzero__(self):
        if self.year is None and self.month is None and self.day is None:
            return False
        else:
            return True


class ExceptionDateDumper(DateDumper): # From Python to DB
    def dump(self, obj):

        year = obj.year
        month = obj.month
        day = obj.day

        if year is None and month is None and day is None:
            return None

        if year < 0:
            bc = " BC"
            year*=-1
        else:
            bc = ""

        day = 1 if day is None else day
        month = 1 if month is None else month

        return bytes(f'{year:04}-{month:02}-{day:02}{bc}', encoding='utf-8')

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

with psycopg.connect("postgres://postgres@localhost:5432/postgres") as conn:

    cur = conn.cursor()

    cur.adapters.register_dumper(SQLDate, ExceptionDateDumper)

    reinitSql = '''
    DROP TABLE IF EXISTS test_dumper_return_none;
    CREATE TABLE IF NOT EXISTS test_dumper_return_none (
        id INT,
        col DATE
    );
    '''

    copySql = '''
    COPY test_dumper_return_none (id, col) FROM STDIN;
    '''

    cur.execute(reinitSql)

    with cur.copy(copySql) as copy:
        copy.write_row(   (0, SQLDate(1990, 5, 28))   )
        copy.write_row(   (0, SQLDate(None, None, None))   )
