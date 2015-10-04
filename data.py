import datetime
import json
import model
import time
import webapp2

class DataHandler(webapp2.RequestHandler):
    def get(self, since_timestamp):
        since = datetime.datetime.fromtimestamp(int(since_timestamp))
        data_points = model.DataPoint.query(model.DataPoint.date > since)


        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('[')

        iterator = data_points.iter()
        for dp in iterator:
            self.response.write(json.dumps({'date': int(time.mktime(dp.date.timetuple())), 'light': dp.light}))
            if iterator.has_next():
                self.response.write(',')
        self.response.write(']')

app = webapp2.WSGIApplication([
    ('/data/(\d+)', DataHandler),
], debug=True)
