import datetime
import json
import model
import time
import webapp2

class DailyArchiveHandler(webapp2.RequestHandler):
    def get(self, days_ago):
        days = int(days_ago)
        if days < 1:
            days = 1
        since = datetime.datetime.utcnow()
        midnight = datetime.datetime(since.year, since.month, since.day)
        yesterday = midnight - datetime.timedelta(days)
        midnight = yesterday + datetime.timedelta(1)

        data = []
        data_points = model.DataPoint.query(model.DataPoint.date >= yesterday, model.DataPoint.date < midnight)
        iterator = data_points.iter()
        for dp in iterator:
            data.append({'date': int(time.mktime(dp.date.timetuple())), 'light': dp.light})

        update_flag = False

        archive = model.DailyArchive.query(model.DataPoint.date == yesterday).get()
        if archive == None:
            archive = model.DailyArchive(
                date = yesterday,
                data = data
                )
        else:
            update_flag = True
            archive.data = data
        archive.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({'count': len(data), 'update': update_flag, 'from': yesterday.isoformat(), 'to': midnight.isoformat()}))



app = webapp2.WSGIApplication([
    ('/daily_archive/(\d+)', DailyArchiveHandler),
], debug=False)
