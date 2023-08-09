from utils.common import logger


class EventManager:
    def __init__(self):
        self.event_handlers = {}

    def subscribe(self, event_name, handler):
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                return handler(*args, **kwargs)
        else:
            logger.info(f'There is no such event - {event_name}')
