import datetime
import json
import model
import time
import webapp2

class DataHandler(webapp2.RequestHandler):
    def get(self, since_timestamp):
        since = datetime.datetime.fromtimestamp(int(since_timestamp))
        since_midnight = datetime.datetime(since.year, since.month, since.day)
        daily_archives = model.DailyArchive.query(model.DailyArchive.date >= since_midnight)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('[')

        data_written = False
        last_archive_date = None

        iterator = daily_archives.iter()
        for archive in iterator:
            length = len(archive.data)
            for index, dp in enumerate(archive.data):
                self.response.write(json.dumps(dp))
                data_written = True
                if length > index + 1:
                    self.response.write(',')
            if iterator.has_next():
                self.response.write(',')
            else:
                last_archive_date = archive.date

        if last_archive_date != None:
            since = last_archive_date + datetime.timedelta(1)
        data_points = model.DataPoint.query(model.DataPoint.date >= since)

        iterator = data_points.iter()
        for dp in iterator:
            if data_written:
                self.response.write(',')
            self.response.write(json.dumps({'date': int(time.mktime(dp.date.timetuple())), 'light': dp.light}))
            data_written = True
        self.response.write(']')

app = webapp2.WSGIApplication([
    ('/data/(\d+)', DataHandler),
], debug=False)
