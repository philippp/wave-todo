import datetime
from google.appengine.ext import db

class TodoItem(db.Model):
    title = db.StringProperty()
    waveId = db.StringProperty()
    dateCreated = db.DateTimeProperty(default=datetime.datetime.now())
    dateCompleted = db.DateTimeProperty(default=None)
