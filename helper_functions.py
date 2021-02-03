def get_dates():
    import datetime
    import pandas as pd
    first_day_month = datetime.date.today().replace(day=1)
    date_list = [first_day_month + datetime.timedelta(days=x) for x in range(120)]
    month, weekday, day = [], [], []
    for date in date_list:
        month.append(date.month)
        weekday.append(date.weekday())
        day.append(date.day)
    df = pd.DataFrame(list(zip(month, weekday, day)), index=date_list, columns=['month', 'dow', 'day'])
    ds = df[(df['dow'] == 6)].groupby(['month'])['day'].rank()
    ds = ds[ds.index >= datetime.date.today()]
    dates, full_dates = [], []
    for i in ds.index.tolist():
        dates.append(i.strftime('%b-%d'))
        full_dates.append(i.strftime('%Y-%m-%d'))
    integers = ds.tolist()
    return dates, integers, full_dates


def load_meetings(full_dates, int_list, specific_int, conferences_list, meetings_list):
    out = []
    for meeting in meetings_list:
        if int_list[specific_int] in meeting['frequency']:
            out.append(meeting)
    for conference in conferences_list:
        if full_dates[specific_int] == conference['date']:
            out = []
            out.append(conference)
    return out
