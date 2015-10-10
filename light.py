from google.appengine.api import urlfetch

import config
import json
import logging
import model
import webapp2

class RequestLightData(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        result = urlfetch.fetch(config.EIMP_AGENT_URL)
        self.response.status = result.status_code

        if result.status_code == 200:
            data = json.loads(result.content)

            logging.debug(data)

            data_point = model.DataPoint(
                light = int(data['light'])
                )
            data_point.put()

            self.response.write(result.content)
        else:
            self.response.write(result.content)


app = webapp2.WSGIApplication([
    ('/light', RequestLightData),
], debug=False)
