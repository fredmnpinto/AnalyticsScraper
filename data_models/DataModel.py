from sqlalchemy import or_
from tqdm import tqdm


class DataModel:
    UNIQUE_COLUMNS = [] # To be overridden by child classes

    @classmethod
    def load_all(cls, database_session):
        if cls is DataModel:  # If called on Parent
            print("Loading data from all data sources")
            for _class in DataModel.__subclasses__():
                print("Loading data from " + _class.__name__)
                _class.load_all(database_session)
        else:
            raise NotImplementedError("Subclasses must override 'load_all()'")

    @classmethod
    def reset_database_to(cls, new_entries: list, database_session):
        old_size = database_session.query(cls).delete()
        print(f"Deleting {old_size} old entries")

        print("Processing new data...")
        database_session.add_all(new_entries)

        print(f'Writing {len(new_entries)} new entries to database...')
        database_session.commit()

    @classmethod
    def find_by(cls, filters: dict, db_session):
        conditions = [getattr(cls, col) == val for col, val in filters.items()]
        return db_session.query(cls).filter(or_(*conditions)).first()

