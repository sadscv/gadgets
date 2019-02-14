import subprocess
import sys


def mdb2sqlite(file, dest):
    subprocess.call(["mdb-schema", file, "mysql"])
    table_names = subprocess.Popen(["mdb-tables", "-1", file],
                                   stdout=subprocess.PIPE).communicate()[0]
    sys.stdout.flush()




if __name__ == '__main__':
    mdb2sqlite(file, dest)
