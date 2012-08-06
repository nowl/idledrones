from datetime import datetime

def trim_events(events):
    # TODO trim this based on time and number
    return events[0:50]

def log_event(mint, user, event):
    events = mint.get_events(user)
    cur_time = datetime.utcnow()
    formatted_time = cur_time.strftime('%m/%d/%y %I:%M:%S %p')
    new_event = {'timestamp': cur_time,
                 'formatted time': formatted_time,
                 'event string': event}
    events.insert(0, new_event)

    mint.set_events(user, trim_events(events))

    print 'event: %s: [%s] %s' % (user, cur_time, event)
