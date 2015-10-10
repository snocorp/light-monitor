from google.appengine.ext import ndb


class DataPoint(ndb.Model):
    """A model for representing an gathered data point."""
    date = ndb.DateTimeProperty(auto_now_add=True)
    light = ndb.IntegerProperty(indexed=False)

class DailyArchive(ndb.Model):
    """A model for storing a day of data points."""
    date = ndb.DateTimeProperty(auto_now_add=False)
    data = ndb.JsonProperty(indexed=False)
