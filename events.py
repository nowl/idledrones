from datetime import datetime

def log_event(mint, user, event):
    events = mint.get_events(user)
    cur_time = datetime.utcnow()
    formatted_time = cur_time.strftime('%m/%d/%y %I:%M:%S %p')
    new_event = {'timestamp': cur_time,
                 'formatted time': formatted_time,
                 'event string': event}
    events.append(new_event)
    mint.set_events(user, events)

    print 'event: %s: [%s] %s' % (user, cur_time, event)
