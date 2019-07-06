import requests
import sys
import xml.etree.ElementTree as ET
shortterm = '_hour_by_hour'
xml  = '.xml'
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

period = sys.argv[1]
limit = int(sys.argv[2])
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
                print(report.format(name, frm, dir.get('deg'), dir.get('code'), spd.get('mps'), tmp.get('value'), psi.get('value')))
