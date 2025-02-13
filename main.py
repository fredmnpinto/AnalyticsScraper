from data_models import *

if __name__ == "__main__":
    new_database_session = setup_database()
    DataModel.load_all(new_database_session)
