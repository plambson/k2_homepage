from flask import Flask, render_template, request, redirect
import config
import os
from helper_functions import get_dates, load_meetings
from datastore_helper import fetch_meetings
from google.cloud import datastore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "kingsbridge2-81ce0161a48e.json"
app = Flask(__name__)
app.secret_key = config.secret_key
app.config.header = config.header
app.config.dates, app.config.integers, app.config.full_dates = get_dates()
app.config.all_meetings = fetch_meetings()
app.config.date_int = 0  # initial sunday to show on the homepage, upcoming sunday
app.config.meetings = load_meetings(app.config.full_dates,
                                    app.config.integers,
                                    app.config.date_int,
                                    config.conferences,
                                    app.config.all_meetings)
app.config.accordions = config.additional_info


@app.route('/')
def index():
    return render_template('index.html',
                           title='Kingsbridge Home Page'
                           )


@app.route('/meeting', methods=['POST', 'GET'])
def meeting():
    title = request.args.get('meeting_title')
    link = request.args.get('meting_link')
    return render_template('meeting_info.html',
                           title=title,
                           link=link)


@app.route('/coming_soon')
def coming_soon():
    return render_template('coming_soon.html')


@app.route('/modify', methods=['POST', 'GET'])
def modify():
    app.config.date_int = int(request.args.get('integer'))
    app.config.meetings = load_meetings(app.config.full_dates,
                                        app.config.integers,
                                        app.config.date_int,
                                        config.conferences,
                                        app.config.all_meetings)
    return redirect('/')


@app.route('/list_meetings')
def list_meetings():
    return render_template('list_meetings.html',
                           title='Meetings List'
                           )


@app.route('/edit', methods=['GET'])
def edit():
    index_pos = int(request.args.get('index_position'))
    return render_template('edit_meeting.html',
                           title='Edit Meeting',
                           meeting=app.config.all_meetings[index_pos],
                           index_pos=index_pos
                           )


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    index_pos = int(request.args.get('index_position'))
    key = app.config.all_meetings[index_pos].key
    client = datastore.Client()
    client.delete(key)
    app.config.all_meetings = fetch_meetings()
    app.config.meetings = load_meetings(app.config.full_dates,
                                        app.config.integers,
                                        app.config.date_int,
                                        config.conferences,
                                        app.config.all_meetings)
    return redirect('/list_meetings')


@app.route('/new')
def new():
    return render_template('new_meeting.html',
                           title='Create Meeting'
                           )


@app.route('/update', methods=['POST'])
def update():
    # create freq list
    freq = []
    if request.form.get('freq_1') == '':
        freq.append(1)
    if request.form.get('freq_2') == '':
        freq.append(2)
    if request.form.get('freq_3') == '':
        freq.append(3)
    if request.form.get('freq_4') == '':
        freq.append(4)
    if request.form.get('freq_5') == '':
        freq.append(5)
    client = datastore.Client()
    key = app.config.all_meetings[int(request.form.get('index_pos'))].key
    entity = datastore.Entity(key=key)
    entity.update({
        'title': request.form.get('meetingTitle'),
        'description': request.form.get('meetingDescription'),
        'time': request.form.get('meetingTime'),
        'frequency': freq,
        'link': request.form.get('meetingLink')
    })
    client.put(entity)
    app.config.all_meetings = fetch_meetings()
    app.config.meetings = load_meetings(app.config.full_dates,
                                        app.config.integers,
                                        app.config.date_int,
                                        config.conferences,
                                        app.config.all_meetings)
    return redirect('/list_meetings')


@app.route('/create', methods=['POST'])
def create():
    # create freq list
    freq = []
    if request.form.get('freq_1') == '':
        freq.append(1)
    if request.form.get('freq_2') == '':
        freq.append(2)
    if request.form.get('freq_3') == '':
        freq.append(3)
    if request.form.get('freq_4') == '':
        freq.append(4)
    if request.form.get('freq_5') == '':
        freq.append(5)
    client = datastore.Client()
    kind = "meetings"
    name = request.form.get('meetingTitle')
    meeting_key = client.key(kind, name)
    # Prepares the new entity
    meeting = datastore.Entity(key=meeting_key)
    meeting['title'] = request.form.get('meetingTitle')
    meeting['description'] = request.form.get('meetingDescription')
    meeting['time'] = request.form.get('meetingTime')
    meeting['frequency'] = freq
    meeting['link'] = request.form.get('meetingLink')
    # Saves the entity
    client.put(meeting)

    app.config.all_meetings = fetch_meetings()
    app.config.meetings = load_meetings(app.config.full_dates,
                                        app.config.integers,
                                        app.config.date_int,
                                        config.conferences,
                                        app.config.all_meetings)
    return redirect('/list_meetings')


if __name__ == "__main__":
    app.run()
