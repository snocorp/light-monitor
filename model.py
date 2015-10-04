from google.appengine.ext import ndb


class DataPoint(ndb.Model):
    """A model for representing an gathered data point."""
    date = ndb.DateTimeProperty(auto_now_add=True)
    light = ndb.IntegerProperty(indexed=False)
