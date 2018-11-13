from api import db


class Dictable:

    def to_dict(self, hidden=None):
        return {
            key: getattr(self, key) for key in self.__class__.__dict__['__table__']._columns.keys()
        }


class Todo(db.Model, Dictable):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    complete = db.Column(db.Boolean, default=False)
