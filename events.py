from datetime import datetime

def log_event(mint, user, event):
    events = mint.get_events(user)
    new_event = "[%s] %s" % (datetime.utcnow(), event)
    events.append(new_event)
    mint.set_events(user, events)
