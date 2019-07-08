import requests
import sys
import json
import utils
import urls
import xml.etree.ElementTree as ET

period, limit, verbose = utils.handleArgs(sys.argv)

report = '''
    place: {}
    time: {}
    direction: {} (deg)  code: {}
    force: {}
    temp: {} pressure: {} (hpa)
    ______________________
    '''

for url in urls.urls:
    request = url
    if period == "short":
        request = request + urls.shortterm
    request = request + urls.xml
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
                    urls.webhook_url, data=json.dumps(slack_data),
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code != 200:
                    raise ValueError(
                        'Request to slack returned an error %s, the response is:\n%s'
                        % (response.status_code, response.text)
                    )
