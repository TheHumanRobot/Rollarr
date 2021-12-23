import PySimpleGUI as sg
import webbrowser
import PrerollUpdate
from plexapi.server import PlexServer
import re
import requests
import yaml
from urllib.parse import quote_plus, urlencode


from plexapi import media, utils, settings, library
from plexapi.base import Playable, PlexPartialObject
from plexapi.exceptions import BadRequest, NotFound

from argparse import ArgumentParser
import os
from os.path import exists
import random
import pathlib
from configparser import *
import pathlib
import datetime
import json

print('#############################')
print('#                           #')
print('#  Plex Automated Preroll!  #')
print('#                           #')
print('#############################' + '\n')


button_base64 =b'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'

if exists('data.json'):
    print('ready')
else:
    with open('data.json', 'w') as outfile:
        json.dump({'URL': ''}, outfile)

with open('data.json') as json_file:
    output = json.load(json_file)

sg.theme('DarkBlue')

col_1 = [[sg.Text('Automate your Plex Preroll!', size=(30, 1), font=("Helvetica", 25))],
    [sg.Text('Plex Server URL')],
    [sg.InputText(output.get('URL'), key='URL')],
    [sg.Text('Plex Server Token')],
    [sg.InputText(output.get('Token'), key='Token')],
    [sg.Text('Schedule')],
    [sg.Listbox(values=['Monthly','Weekly','Daily', 'Holiday', 'Custom'], size=(20,5), key='Freq', default_values=output.get('Freq'), enable_events = True)],
    [sg.Text('Default Files')],
    [sg.In(default_text=output.get('Default'),key='Default'), sg.FilesBrowse()],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Save(), sg.Submit()],
    [sg.Button('', image_data=button_base64, key='Buy', button_color='Yellow')]]
col_month = [[sg.Text('Select your files', size=(20, 1), font=("Helvetica", 15))],
            [sg.Text("Jan : ", size=(5, 1), justification='right'), sg.In(default_text= output.get('Jan') ,key='Jan'), sg.FilesBrowse()],
            [sg.Text("Feb : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Feb'),key='Feb'), sg.FilesBrowse()],
            [sg.Text("Mar : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Mar'),key='Mar'), sg.FilesBrowse()],
            [sg.Text("Apr : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Apr'),key='Apr'), sg.FilesBrowse()],
            [sg.Text("May : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('May'),key='May'), sg.FilesBrowse()],
            [sg.Text("Jun : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Jun'),key='Jun'), sg.FilesBrowse()],
            [sg.Text("Jul : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Jul'),key='Jul'), sg.FilesBrowse()],
            [sg.Text("Aug : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Aug'),key='Aug'), sg.FilesBrowse()],
            [sg.Text("Sep : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Sep'),key='Sep'), sg.FilesBrowse()],
            [sg.Text("Oct : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Oct'),key='Oct'), sg.FilesBrowse()],
            [sg.Text("Nov : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Nov'),key='Nov'), sg.FilesBrowse()],
            [sg.Text("Dec : ", size=(5, 1) , justification='right'), sg.In(default_text=output.get('Dec'),key='Dec'), sg.FilesBrowse()]];
col_week = [[sg.Text('Select your files', size=(20, 1), font=("Helvetica", 15))],
          [sg.Text('Start Date', size=(10, 1)), sg.InputText(default_text=output.get('WeekStart'),key='WeekStart',), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('End Date', size=(10, 1)), sg.InputText(default_text=output.get('WeekEnd'), key='WeekEnd'), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('Path: ', size=(10, 1)), sg.In(default_text=output.get('WeekPath'), key='WeekPath', justification='right'), sg.FilesBrowse()],
]

col_day = [[sg.Text('Select your files', size=(20, 1), font=("Helvetica", 15))],
            [sg.Text('Monday', size=(10, 1)), sg.In(default_text=output.get('Mon'),key='Mon'), sg.FilesBrowse()],
            [sg.Text('Tuesday', size=(10, 1)), sg.In(default_text=output.get('Tue'),key='Tue'), sg.FilesBrowse()],
            [sg.Text('Wednesday', size=(10, 1)), sg.In(default_text=output.get('Wed'),key='Wed'), sg.FilesBrowse()],
            [sg.Text('Thursday', size=(10, 1)), sg.In(default_text=output.get('Thu'),key='Thur'), sg.FilesBrowse()],
            [sg.Text('Friday', size=(10, 1)), sg.In(default_text=output.get('Fri'),key='Fri'), sg.FilesBrowse()],
            [sg.Text('Saturday', size=(10, 1)), sg.In(default_text=output.get('Sat'),key='Sat'), sg.FilesBrowse()],
            [sg.Text('Sunday', size=(10, 1)), sg.In(default_text=output.get('Sun'),key='Sun'), sg.FilesBrowse()]]

col_holiday = [[sg.Text('Select your files', size=(20, 1), font=("Helvetica", 15))],
            [sg.Text('Valentines Day', size=(11, 1)), sg.In(default_text=output.get('Valentines Day'),key='Valentines Day'), sg.FilesBrowse(),sg.Checkbox('Enable', key='Valentines Day Enabled', default=output.get('Valentines Day Enabled'))],
            [sg.Text('April Fools', size=(11, 1)), sg.In(default_text=output.get('April Fools'),key='April Fools'), sg.FilesBrowse(),sg.Checkbox('Enable', key='April Fools Enabled', default=output.get('April Fools Enabled'))],
            [ sg.Text('July 4th', size=(11, 1)), sg.In(default_text=output.get('July 4th'),key='July 4th'), sg.FilesBrowse(),sg.Checkbox('Enable', key='July 4th Enabled', default=output.get('July 4th Enabled'))],
               [sg.Text('Mardi Gras', size=(11, 1)), sg.In(default_text=output.get('Mardi Gras'), key='Mardi Gras'),
                sg.FilesBrowse(),
                sg.Checkbox('Enable', key='Mardi Gras Enabled', default=output.get('Mardi Gras Enabled'))],
               [sg.Text('Easter', size=(11, 1)), sg.In(default_text=output.get('Easter'), key='Easter'), sg.FilesBrowse(),
                sg.Checkbox('Enable', key='Easter Enabled', default=output.get('Easter Enabled'))],
               [sg.Text('Halloween', size=(11, 1)), sg.In(default_text=output.get('Halloween'), key='Halloween'),
                sg.FilesBrowse(),
                sg.Checkbox('Enable', key='Halloween Enabled', default=output.get('Halloween Enabled'))],
               [sg.Text('Thanksgiving', size=(11, 1)), sg.In(default_text=output.get('Thanksgiving'), key='Thanksgiving'),
                sg.FilesBrowse(),
                sg.Checkbox('Enable', key='Thanksgiving Enabled', default=output.get('Thanksgiving Enabled'))],
               [sg.Text('Christmas', size=(11, 1)), sg.In(default_text=output.get('Christmas'), key='Christmas'),
                sg.FilesBrowse(),
                sg.Checkbox('Enable', key='Christmas Enabled', default=output.get('Christmas Enabled'))]]

col_custom = [[sg.Text('Select your files', size=(20, 1), font=("Helvetica", 15))],
             [sg.Text('Custom Configuration')],
             [sg.Text('Playback is determined by order then date')],
             [sg.Text('1.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path1', ''), key='Path1', justification='right'), sg.FilesBrowse()],
             [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start1', ''),key='Start1', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End1'), key='End1', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
             [sg.Text('2.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path2', ''),key='Path2', justification='right'), sg.FilesBrowse()],
             [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start2'),key='Start2', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End2'), key='End2', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('3.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path3', ''),key='Path3', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start3'),key='Start3', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End3'), key='End3', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('4.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path4', ''),key='Path4', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start4'),key='Start4', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End4'), key='End4', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('5.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path5', ''),key='Path5', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start5'),key='Start5', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End5'), key='End5', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('6.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path6', ''),key='Path6', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start6'),key='Start6', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End6'), key='End6', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('7.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path7', ''),key='Path7', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start7'),key='Start7', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End7'), key='End7', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('8.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path8', ''),key='Path8', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start8'),key='Start8', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End8'), key='End8', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('9.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path9', ''),key='Path9', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start9'),key='Start9', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End9'), key='End9', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],
            [sg.Text('10.'), sg.Text('Path: ', size=(5, 1)), sg.In(default_text=output.get('Path10', ''), key='Path10', justification='right'), sg.FilesBrowse()],
            [sg.Text('Start Date', size=(8, 1)), sg.InputText(default_text=output.get('Start10'),key='Start10', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d'), sg.Text('End Date', size=(8, 1)), sg.InputText(default_text=output.get('End10'), key='End10', size=(12,1)), sg.CalendarButton(button_text="Select", format='%Y-%m-%d')],

]

layout = [[sg.Frame(layout=col_1, title='',border_width=0), sg.Frame(layout=col_custom, title='',border_width=0, visible=False, key='Custom'), sg.Frame(layout=col_month, title='',border_width=0, visible=False, key='Month'), sg.Frame(layout=col_week, title='',border_width=0, visible=False, key='Week'), sg.Frame(layout=col_day, title='',border_width=0, visible=False, key='Day'), sg.Frame(layout=col_holiday, title='',border_width=0, visible=False, key='Holiday')]

     ]
window = sg.Window('Plex Automated Preroll', layout)
while True:
    event, values = window.read()
    if event == 'Buy':
        webbrowser.open_new('https://www.buymeacoffee.com/thehumanrobot')
    if event == 'Save':

        with open('data.json', 'w') as outfile:
            json.dump({'URL': values['URL'], 'Token': values['Token'], 'Freq': values['Freq'], 'Jan': values['Jan'], 'Feb': values['Feb'], 'Mar': values['Mar'], 'Apr': values['Apr'], 'May': values['May'], 'Jun': values['Jun'], 'Jul': values['Jul'], 'Aug': values['Aug'], 'Sep': values['Sep'], 'Oct': values['Oct'], 'Nov': values['Nov'], 'Dec': values['Dec'],
                   'WeekStart': values['WeekStart'], 'WeekEnd': values['WeekEnd'], 'WeekPath': values['WeekPath'], 'Sun': values['Sun'], 'Mon': values['Mon'], 'Tue': values['Tue'], 'Wed': values['Wed'], 'Thu': values['Thur'], 'Fri': values['Fri'], 'Sat': values['Sat'],
                   'Valentines Day': values['Valentines Day'], 'April Fools': values['April Fools'], 'July 4th': values['July 4th'], 'Mardi Gras': values['Mardi Gras'], 'Easter': values['Easter'], 'Halloween': values['Halloween'], 'Thanksgiving': values['Thanksgiving'], 'Christmas': values['Christmas'], 'Valentines Day Enabled': values['Valentines Day Enabled']
                      , 'April Fools Enabled': values['April Fools Enabled'], 'July 4th Enabled': values['July 4th Enabled'], 'Mardi Gras Enabled': values['Mardi Gras Enabled'], 'Easter Enabled': values['Easter Enabled'], 'Halloween Enabled': values['Halloween Enabled'], 'Thanksgiving Enabled': values['Thanksgiving Enabled'], 'Christmas Enabled': values['Christmas Enabled'], 'Default': values['Default']
                       , 'Start1': values['Start1'], 'Start2': values['Start2'], 'Start3': values['Start3'], 'Start4': values['Start4'], 'Start5': values['Start5'], 'Start6': values['Start6'], 'Start7': values['Start7'], 'Start8': values['Start8'], 'Start9': values['Start9'], 'Start10': values['Start10']
                       , 'End1': values['Start1'], 'End2': values['End2'], 'End3': values['End3'], 'End4': values['End4'], 'End5': values['End5'], 'End6': values['End6'], 'End7': values['End7'], 'End8': values['End8'], 'End9': values['End9'], 'End10': values['End10']
                       , 'Path1': values['Path1'], 'Path2': values['Path2'], 'Path3': values['Path3'], 'Path4': values['Path4'], 'Path5': values['Path5'], 'Path6': values['Path6'], 'Path7': values['Path7'], 'Path8': values['Path8'], 'Path9': values['Path9'], 'Path10': values['Path10']}, outfile)
        sg.popup('Your changes are saved')
    if event == 'Submit':

        with open('data.json', 'w') as outfile:
            json.dump({'URL': values['URL'], 'Token': values['Token'], 'Freq': values['Freq'], 'Jan': values['Jan'], 'Feb': values['Feb'], 'Mar': values['Mar'], 'Apr': values['Apr'], 'May': values['May'], 'Jun': values['Jun'], 'Jul': values['Jul'], 'Aug': values['Aug'], 'Sep': values['Sep'], 'Oct': values['Oct'], 'Nov': values['Nov'], 'Dec': values['Dec'],
                   'WeekStart': values['WeekStart'], 'WeekEnd': values['WeekEnd'], 'WeekPath': values['WeekPath'], 'Sun': values['Sun'], 'Mon': values['Mon'], 'Tue': values['Tue'], 'Wed': values['Wed'], 'Thu': values['Thur'], 'Fri': values['Fri'], 'Sat': values['Sat'],
                   'Valentines Day': values['Valentines Day'], 'April Fools': values['April Fools'], 'July 4th': values['July 4th'], 'Mardi Gras': values['Mardi Gras'], 'Easter': values['Easter'], 'Halloween': values['Halloween'], 'Thanksgiving': values['Thanksgiving'], 'Christmas': values['Christmas'], 'Valentines Day Enabled': values['Valentines Day Enabled']
                      , 'April Fools Enabled': values['April Fools Enabled'], 'July 4th Enabled': values['July 4th Enabled'], 'Mardi Gras Enabled': values['Mardi Gras Enabled'], 'Easter Enabled': values['Easter Enabled'], 'Halloween Enabled': values['Halloween Enabled'], 'Thanksgiving Enabled': values['Thanksgiving Enabled'], 'Christmas Enabled': values['Christmas Enabled'], 'Default': values['Default']
                       , 'Start1': values['Start1'], 'Start2': values['Start2'], 'Start3': values['Start3'], 'Start4': values['Start4'], 'Start5': values['Start5'], 'Start6': values['Start6'], 'Start7': values['Start7'], 'Start8': values['Start8'], 'Start9': values['Start9'], 'Start10': values['Start10']
                       , 'End1': values['Start1'], 'End2': values['End2'], 'End3': values['End3'], 'End4': values['End4'], 'End5': values['End5'], 'End6': values['End6'], 'End7': values['End7'], 'End8': values['End8'], 'End9': values['End9'], 'End10': values['End10']
                       , 'Path1': values['Path1'], 'Path2': values['Path2'], 'Path3': values['Path3'], 'Path4': values['Path4'], 'Path5': values['Path5'], 'Path6': values['Path6'], 'Path7': values['Path7'], 'Path8': values['Path8'], 'Path9': values['Path9'], 'Path10': values['Path10']}, outfile)
        PrerollUpdate.update()
        sg.popup('Your Pre-roll is updated!')

    if event == 'Freq':
        if values['Freq'] == ['Monthly']:
            window['Month'].update(visible=True)
            window['Week'].update(visible=False)
            window['Day'].update(visible=False)
            window['Holiday'].update(visible=False)
            window['Custom'].update(visible=False)
        elif values['Freq'] == ['Weekly']:
            window['Month'].update(visible=False)
            window['Week'].update(visible=True)
            window['Day'].update(visible=False)
            window['Holiday'].update(visible=False)
            window['Custom'].update(visible=False)
        elif values['Freq'] == ['Daily']:
            window['Month'].update(visible=False)
            window['Week'].update(visible=False)
            window['Day'].update(visible=True)
            window['Holiday'].update(visible=False)
            window['Custom'].update(visible=False)
        elif values['Freq'] == ['Holiday']:
            window['Month'].update(visible=False)
            window['Week'].update(visible=False)
            window['Day'].update(visible=False)
            window['Holiday'].update(visible=True)
            window['Custom'].update(visible=False)
        elif values['Freq'] == ['Custom']:
            window['Month'].update(visible=False)
            window['Week'].update(visible=False)
            window['Day'].update(visible=False)
            window['Holiday'].update(visible=False)
            window['Custom'].update(visible=True)
    if event == sg.WIN_CLOSED:
        break

window.close()
