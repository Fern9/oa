class Activity(object):
    def __init__(self, name, participants, state=1):
        self.name = name
        self.state = state
        self.participants = participants

    def has_permission(self):
        return False



