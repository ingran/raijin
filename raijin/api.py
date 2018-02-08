# -*- coding: utf-8 -*-

import linkero.core.linkero as linkero
import raijin
import time

raijin = raijin.Raijin()
api_base_path = "/raijin/api/v1"

parser = linkero.reqparse.RequestParser()
parser.add_argument('datetime')
parser.add_argument('date')

class holidays(linkero.Resource):
    def get(self):
        data = {}
        start_time = time.time()
        response = raijin.getHolidays(None, True)
        data["time_exec_secs"] = (time.time() - start_time)
        data["response"] = response
        links = []
        links.append({"rel": "self", "href": linkero.getResourceURL(endpoint="holidays", absolute=True)})
        for year in response:
            links.append({"rel": year, "href": linkero.getResourceURL("year-holiday", "year", year, True)})
        data["links"] = links
        return data


class holidays_by_year(linkero.Resource):
    def get(self, year):
        data = {}
        start_time = time.time()
        response = raijin.getHolidays(year, True)
        data["time_exec_secs"] = (time.time() - start_time)
        data["response"] = response
        if "message" in response:
            return data, 400    # Return BAD REQUEST code
        else:
            data["year"] = year
            return data


class workable(linkero.Resource):
    def get(self, date):
        data = {}
        start_time = time.time()
        response = raijin.isWorkable(date)
        data["time_exec_secs"] = (time.time() - start_time)
        data["response"] = response
        if "message" in str(response):
            return data, 400     # Return BAD REQUEST code
        else:
            data["date"] = date
            return data


class tariff(linkero.Resource):
    def get(self, name):
        params = parser.parse_args()
        data = {}

        if (params['datetime'] is None):
            data["date"] = raijin.getCurDate()
            data["time"] = raijin.getCurTime()
            sdatetime = []
            sdatetime.append(data["date"])
            sdatetime.append(" " + data["time"])
        else:
            sdatetime = params['datetime'].split(" ")
            if len(sdatetime) == 1:
                sdatetime.append("")
            else:
                sdatetime[1] = " " + sdatetime[1]

        start_time = time.time()
        response = raijin.getTariff(name,  sdatetime[0] + sdatetime[1])
        data["time_exec_secs"] = (time.time() - start_time)

        data["response"] = response
        if "message" in response:
            return data, 400        # Return BAD REQUEST code
        else:
            data["tariff"] = name
            data["date"] = sdatetime[0]
            data["time"] = sdatetime[1]

            # HATEOAS
            # --------------------
            links = []
            if (params['datetime'] is None):
                links.append({"rel": "self", "href": linkero.getResourceURL("tariff", "name", name, True)})
                links.append({"rel": "filter_by_datetime", "href": linkero.getResourceURL("tariff", "name", name, True)
                                                               + "?datetime=<datetime-value>",
                          "datetime-format": "^([0-9]{2}-[0-9]{2}-[0-9]{4} [0-9]{2}:[0-9]{2}(:[0-9]{2})*)$"})
            else:
                links.append({"rel": "self", "href": linkero.getResourceURL("tariff", "name", name, True)
                                                                   + "?datetime="+sdatetime[0] + " " + sdatetime[1]})
                links.append({"rel": "current_tariff", "href": linkero.getResourceURL("tariff", "name", name, True)})
            # --------------------

            data["links"] = links

            return data


class time_change(linkero.Resource):
    def get(self):
        params = parser.parse_args()
        data = {}

        if (params['date'] is None):
            data["date"] = raijin.getCurDate()
            sdatetime = []
            sdatetime.append(data["date"])
        else:
            sdatetime = params['date'].split(" ")

        start_time = time.time()
        response = raijin.timeChange(sdatetime[0])
        if len(response) == 2:
            presponse = {}
            presponse["time_change"] = response[0]
            presponse["days_left"] = response[1]
            response = presponse
        data["time_exec_secs"] = (time.time() - start_time)

        data["response"] = response
        if "message" in response:
            return data, 400  # Return BAD REQUEST code
        else:
            data["date"] = sdatetime[0]

            # HATEOAS
            # --------------------
            links = []
            if (params['date'] is None):
                links.append({"rel": "self", "href": linkero.getResourceURL(endpoint="time-change", absolute=True)})
                links.append({"rel": "filter_by_date", "href": linkero.getResourceURL(endpoint="time-change", absolute=True)
                                                                   + "?date=<date-value>",
                              "date-format": "^([0-9]{2}-[0-9]{2}-[0-9]{4})$"})
            else:
                links.append({"rel": "self", "href": linkero.getResourceURL(endpoint="time-change", absolute=True)
                                                     + "?date=" + sdatetime[0]})
                links.append({"rel": "current_time_change", "href": linkero.getResourceURL(endpoint="time-change", absolute=True)})
            # --------------------

            data["links"] = links

            return data


##
## Additional functions
##

##
## Actually setup the Api resource routing here
##
def loadRaijinAPI():
    linkero.api.add_resource(holidays, api_base_path+'/holidays', endpoint='holidays')
    linkero.api.add_resource(holidays_by_year, api_base_path+'/holidays/<year>', endpoint='year-holiday')
    linkero.api.add_resource(workable, api_base_path+'/workable/<date>', endpoint='workable')
    #linkero.api.add_resource(tariffList, api_base_path+'/tariffs', endpoint='tariffs')
    linkero.api.add_resource(tariff, api_base_path+'/tariffs/<string:name>', endpoint='tariff')
    linkero.api.add_resource(time_change, api_base_path + '/time_change', endpoint='time-change')
    linkero.logger.info('Loaded raijinAPI')
