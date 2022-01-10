import json
import datetime
import requests
from dateutil.easter import easter
from plexapi.server import PlexServer
import os


def update():
    os.chdir('/rollarr/')
    f = open(str('./data.json'))

    data = json.load(f)

    if data['Freq'] == 'Monthly':
        Date = datetime.date.today()
        Date = Date.strftime("%b")
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
        print(Date)
        if (data[Date] is None or data[Date] == 'None'):
            Path = data['Default']
            print(Path)
        else:
            Path = data[Date]
        prerolls = Path
        plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
        plex.settings.save()
        print('Pre-roll updated')
    if data['Freq'] == 'Weekly':
        Date = datetime.date.today()
        Date = Date.strftime("%Y-%m-%d")
        if data['WeekStart'] <= Date <= data['WeekEnd']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['WeekPath']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        else:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Default']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
    if data['Freq'] == 'Daily':
        Date = datetime.date.today()
        Date = Date.strftime("%a")
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
        if (data[Date] is None or data[Date] == 'None'):
            Path = data['Default']
            print(Path)
        else:
            Path = data[Date]
            print(Path)
        prerolls = Path
        plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
        plex.settings.save()
        print('Pre-roll updated')
    if data['Freq'] == 'Holiday':
        Date = datetime.date.today()
        ThanksgivingDay = 22 + (10 - datetime.date(Date.year, 11, 1).weekday()) % 7
        # Valentines Day
        if Date.strftime("%b%d") == 'Feb14' and data['Valentines Day Enabled']:
            Path = data['Valentines Day']
        # April Fools
        elif Date.strftime("%b%d") == 'Apr01' and data['April Fools Enabled']:
            Path = data['April Fools']
        # Juy 4th
        elif Date.strftime("%b%d") == 'Jul04' and data['July 4th Enabled']:
            Path = data['July 4th']
        # Mardi Gras
        elif easter(Date.year) - datetime.timedelta(days=47) == Date and data['Mardi Gras Enabled']:
            Path = data['Mardi Gras']
        # Easter
        elif easter(Date.year) - datetime.timedelta(days=3) <= Date <= easter(Date.year) and data['Easter Enabled']:
            Path = data['Easter']
        # Halloween
        elif Date.strftime("%b") == "Oct" and int(Date.strftime("%d")) >= 23 and data['Halloween Enabled']:
            Path = data['Halloween']
        # Thanksgiving
        elif (datetime.date(Date.year, 11, ThanksgivingDay) - datetime.timedelta(days=3) <= Date <= datetime.date(Date.year, 11, ThanksgivingDay) + datetime.timedelta(days=4)) and data['Thanksgiving Enabled']:
            Path = data['Thanksgiving']
        # Christmas
        elif Date.strftime("%b") == "Dec" and int(Date.strftime("%d")) >= 20 and data['Christmas Enabled']:
            Path = data['Christmas']
        else:
            Path = data['Default']
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
        prerolls = Path
        plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
        plex.settings.save()
        print('Pre-roll updated')
    if data['Freq'] == 'Custom':
        Date = datetime.date.today()
        Date = Date.strftime("%Y-%m-%d")
        if data['Start1'] <= Date <= data['End1']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path1']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start2'] <= Date <= data['End2']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path2']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start3'] <= Date <= data['End3']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path3']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start4'] <= Date <= data['End4']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path4']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start5'] <= Date <= data['End5']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path5']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start6'] <= Date <= data['End6']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path6']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start7'] <= Date <= data['End7']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path7']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start8'] <= Date <= data['End8']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path8']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start9'] <= Date <= data['End9']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path9']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
        elif data['Start10'] <= Date <= data['End10']:
            session = requests.Session()
            session.verify = False
            requests.packages.urllib3.disable_warnings()
            plex = PlexServer(data['URL'], data['Token'], session, timeout=None)
            prerolls = data['Path10']
            plex.settings.get('cinemaTrailersPrerollID').set(prerolls)
            plex.settings.save()
            print('Pre-roll updated')
# Closing file
    f.close()


if __name__ == '__main__':
    update()
