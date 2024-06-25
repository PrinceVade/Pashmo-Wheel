
class Row(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return '<Row ' + dict.__repr__(self) + '>'

class Table(list):
    """A list of rows, each of which is a dictionary."""

    def any(self, predicate):
        for row in self:
            if predicate(row):
                return True
        return False

    def filter(self, predicate):
        return Table(filter(predicate, self))
    
    def find(self, target):
        if (self.any(lambda row: isinstance(target, dict))):
            raise TypeError(f'Table.find() expected a dict, got {type(target)}')
        
        for row in self:
            if target in row.values():
                return row
        
        return None