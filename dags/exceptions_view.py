from store import Store
from avito_data import ParseException

if __name__ == "__main__":
    exceptions = Store().get_exceptions()
    print("\n".join(["{}) {}".format(i, ex.msg) for i, ex in enumerate(exceptions)]))
    print()
    print("\n\n".join(["{}) {}\n{}".format(i, ex.msg, str(ex.context)) for i, ex in enumerate(exceptions)]))