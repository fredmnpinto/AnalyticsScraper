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
    def write_to_database(cls, entries: list, database_session):
        new_unique_entries = 0

        print("Processing data...")
        for entry in entries:
            # Check if the entry already exists in the database
            filters = {}
            for column in cls.UNIQUE_COLUMNS:
                filters[column] = cls.getattr(column)
            existing_entry = cls.find_by(filters, database_session)

            if existing_entry:
                # If the entry already exists, we update it
                entry.id = existing_entry.id
                database_session.merge(entry)
            else:
                # If the entry does not exist, we add it to the session and track it as new
                database_session.add(entry)
                new_unique_entries += 1

        print(f'Writing {new_unique_entries} new entries to database...')
        database_session.commit()

    @classmethod
    def find_by(cls, filters: dict, db_session):
        conditions = [getattr(cls, col) == val for col, val in filters.items()]
        return db_session.query(cls).filter(or_(*conditions)).first()

