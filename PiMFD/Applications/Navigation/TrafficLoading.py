import json
from time import gmtime
import traceback

import requests

from PiMFD.Applications.Navigation.MapEntities import MapEntity


__author__ = 'Matt Eland'


class TrafficIncident(MapEntity):
    """
    Represents a traffic incident
    """

    description = None
    congestion_info = None
    detour = None
    start = None
    end = None
    lane = None
    road_closed = False
    severity = None
    to_point = None
    last_modified = None
    incident_type = None
    verified = False


class MapTraffic(object):
    options = None

    def __init__(self, options):
        super(MapTraffic, self).__init__()

        self.options = options

    def get_traffic(self, bounds):

        incidents = None

        if not self.options.bing_maps_key:
            return None

        url = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/%f,%f,%f,%f?key=%s" % (
            bounds[1],
            bounds[2],
            bounds[3],
            bounds[0],
            self.options.bing_maps_key
        )

        print("Fetching traffic from: " + url)
        data = None

        # TODO: What the heck? This looks to be infinitely calling the URL with no failover. That bad.
        request = True
        while request:
            try:
                response = requests.get(url)
                response_text = response.text
                print(response_text)
                data = json.loads(response_text)

            except:
                error_message = "Unhandled error getting request {0}\n".format(str(traceback.format_exc()))
                print(error_message)
                request = False
            else:
                break

        if data:
            incidents = list()
            resource_sets = data['resourceSets']
            if len(resource_sets) > 0:
                resources = resource_sets[0]['resources']
                if len(resources) > 0:
                    for res in resources:
                        lat = res['point']['coordinates'][0]
                        lng = res['point']['coordinates'][1]
                        incident = TrafficIncident(lat, lng)

                        incident.id = self.get_safe_value(res, 'incidentId')
                        incident.congestion_info = self.get_safe_value(res, 'congestion')
                        incident.description = self.get_safe_value(res, 'description')
                        incident.detour = self.get_safe_value(res, 'detour')
                        incident.lane = self.get_safe_value(res, 'lane')
                        incident.incident_type = self.get_safe_value(res, 'type')
                        incident.road_closed = self.get_safe_value(res, 'roadClosed')
                        incident.severity = self.get_safe_value(res, 'severity')
                        incident.verified = self.get_safe_value(res, 'verified')
                        incident.end = self.get_safe_value(res, 'end')
                        incident.start = self.get_safe_value(res, 'start')

                        if incident.incident_type:
                            incident.incident_type = int(incident.incident_type)
                            if incident.incident_type == 1:
                                incident.name = 'Accident'
                            elif incident.incident_type == 2:
                                incident.name = 'Congestion'
                            elif incident.incident_type == 3:
                                incident.name = 'Disabled Vehicle'
                            elif incident.incident_type == 4:
                                incident.name = 'Mass Transit'  # Whaaaaaat?
                            elif incident.incident_type == 5:
                                incident.name = 'Misc. Traffic'
                            elif incident.incident_type == 6:
                                incident.name = 'News Alert'
                            elif incident.incident_type == 7:
                                incident.name = 'Event'
                            elif incident.incident_type == 8:
                                incident.name = 'Hazard'
                            elif incident.incident_type == 9:
                                incident.name = 'Construction'
                            elif incident.incident_type == 10:
                                incident.name = 'Alert'
                            elif incident.incident_type == 11:
                                incident.name = 'Weather'

                        incidents.append(incident)

        return incidents

    @staticmethod
    def get_safe_value(res, key):

        value = None

        if key in res:
            value = res[key]

            if value and '/date' in str.lower(str(value)):
                substr = str(value[6:-5])
                seconds = int(substr)
                value = gmtime(seconds)

        return value
