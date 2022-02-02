import json
from pathlib import Path
from typing import TypeVar, Any, cast


TFallback = TypeVar('TFallback')

NO_FALLBACK = object()


class JSONDatabase:
    """
    A very simple JSON file-based database.
    """
    def __init__(self, filename: str):
        self.filename: str = filename
        self.data: dict[str, dict[str, Any]] = self._load()
        self.dirty: bool = False


    def _load(self) -> dict[str, dict[str, Any]]:
        """
        Load the database from the file.
        """
        with open(self.filename, 'rt', encoding='utf-8') as f:
            data = json.load(f)

        return data


    def save(self):
        """
        Save the database to the file.
        """
        if self.data is None:
            raise Exception("No data to save.")

        if not self.dirty:
            return

        # Convert to JSON first before we touch the file (safer if there are errors)
        data = json.dumps(self.data, indent=4, separators=(',', ': '), sort_keys=True)

        # Write the data
        Path(self.filename).write_text(data, encoding='utf-8')

        self.dirty = False


    def mark_dirty(self):
        """
        Mark the database as dirty, so it will be saved in future.
        """
        self.dirty = True


    def __getitem__(self, id: str) -> dict[str, Any]:
        return self.data[str(id)]


    def get(self, id: str, fallback:TFallback=NO_FALLBACK) -> dict[str, Any]|TFallback:
        """
        Get the value of an item, or return a fallback value if it doesn't exist.
        """
        try:
            return self.data[str(id)]
        except KeyError:
            if fallback is NO_FALLBACK:
                raise
            return fallback


    def __setitem__(self, id: str, value: dict[str, Any]) -> dict[str, Any]:
        self.data[str(id)] = value
        self.mark_dirty()
        return value


    def update(self, id: str, update_values: dict[str, Any]) -> dict[str, Any]:
        """
        Update the value of an item.
        """
        old_values = self.data[str(id)]
        new_values = {**old_values, **update_values}
        self.data[str(id)] = new_values
        self.mark_dirty()
        return update_values


if __name__ == '__main__':
    from typing import Any

    db = JSONDatabase('database.json')
    db['1234'] = dict(name='Dirty John', age=42)
    db.save()


    db = JSONDatabase('database.json')
    print(db['1234'])


    db = JSONDatabase('database.json')
    db.update('1234', dict(age=43))
    db.update('1234', dict(gender='m'))
    db.save()
