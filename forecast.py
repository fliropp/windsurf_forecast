import requests
import sys
import json
import utils
import xml.etree.ElementTree as ET

period, limit, verbose = utils.handleArgs(sys.argv)
shortterm = '_hour_by_hour'
xml  = '.xml'
webhook_url = 'https://hooks.slack.com/services/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'

urls = ['https://www.yr.no/place/Norway/Akershus/Frogn/Torkilstranda/forecast',
        'https://www.yr.no/sted/Norge/%C3%98stfold/Rygge/Larkollen~2779456/forecast',
        'https://www.yr.no/place/Norway/%C3%98stfold/Hvaler/Brattest%C3%B8/forecast',
        'https://www.yr.no/place/Sweden/V%C3%A4stra_G%C3%B6taland/Ross%C3%B6-Lyngnholmen/forecast',
        'https://www.yr.no/place/Norway/%C3%98stfold/Hvaler/%C3%98rekroken/forecast',
        'https://www.yr.no/place/Norway/Vestfold/T%C3%B8nsberg/Ringshaugbukta/forecast',
        'https://www.yr.no/place/Sweden/%C3%96rebro/Apelviken/forecast',
        'https://www.yr.no/place/Norway/Akershus/B%C3%A6rum/Halden_brygge/forecast',
        'https://www.yr.no/place/Norway/Vestfold/T%C3%B8nsberg/Skallevollbukta/forecast',
        'https://www.yr.no/place/Norway/Vestfold/T%C3%B8nsberg/Feskj%C3%A6r/forecast',
        'https://www.yr.no/place/Norway/Vestfold/Larvik/Omlidstranda_camping/forecast']


report = '''
    place: {}
    time: {}
    direction: {} (deg)  code: {}
    force: {}
    temp: {} pressure: {} (hpa)
    ______________________
    '''

for url in urls:
    request = url
    if period == "short":
        request = request + shortterm
    request = request + xml
    response = requests.get(request)

    if response:
        root = ET.fromstring(response.text.encode('utf-8').strip())
        forecast = root.findall('./forecast/tabular/time')
        name = root.find('./location/name').text.encode('utf-8').strip()
        for child in forecast:
            frm = child.get('from')
            dir = child.find('windDirection')
            spd = child.find('windSpeed')
            tmp = child.find('temperature')
            psi = child.find('pressure')

            if float(spd.get('mps')) > limit:

                if verbose:
                    print(report.format(name, frm, dir.get('deg'), dir.get('code'), spd.get('mps'), tmp.get('value'), psi.get('value')))

                slack_data = {'text': "Ahoi! {} will have windspeed: {} mps from {} around time {}".format(name, spd.get('mps'), dir.get('code'), frm )}
                response = requests.post(
                    webhook_url, data=json.dumps(slack_data),
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code != 200:
                    raise ValueError(
                        'Request to slack returned an error %s, the response is:\n%s'
                        % (response.status_code, response.text)
                    )
