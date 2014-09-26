'''
Big Red Hacks RHINE Python Reference Client
Required libraries: requests
Compatible with both Python 2 and Python 3.
'''

from requests import get

class InvalidRequest(Exception):
    pass

class CallError(Exception):
    pass

class Rhine:
    conv = staticmethod(lambda es: ','.join(es) \
        if type(es) is list else es)
    conv_ = staticmethod(lambda es: ',' \
        .join(['(' + ','.join(sub) + ')' for sub in es]))
    
    def __init__(self, api_key):
        self.api_key = api_key

    def _call(self, req):
        response = get('http://api.rhine.io/' + self.api_key + '/' + req)
        try:
            data = response.json()
        except:
            raise InvalidRequest(req + ' is not a valid request.')
        if 'error' in data:
            raise CallError('Error: ' + data['error'])
        return data

    def distance(self, entity1, entity2):
        return float(self._call('distance/{0}/{1}' \
            .format(Rhine.conv(entity1), Rhine.conv(entity2)))['distance'])

    def best_match(self, tomatch, possibilities, num):
        response = self._call('best_match/{0}/{1}/{2}' \
            .format(Rhine.conv(tomatch), Rhine.conv_(possibilities), num))['best_match']
        return eval(response.replace('NaN', 'float(\'nan\')'))

    def synonym_check(self, entity1, entity2):
        return self._call('synonym_check/{0}/{1}' \
            .format(entity1, entity2))['synonym'] == 'True'

    def entity_extraction(self, text):
        return self._call('entity_extraction/{0}' \
            .format(text))['entities']

    def closest_entities(self, entity):
        return self._call('closest_entities/{0}' \
            .format(entity))['closest_entities']
