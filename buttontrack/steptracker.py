"""
Simple step tracking class
"""
from dataclasses import dataclass
from buttontrack.arrowstate import ArrowState
from buttontrack.time import current_ts


class StepOverview:
    IDLE_TIME = 30  # time in seconds

    def __init__(self):
        self.arrow_tracker = ArrowState()
        self.step_intervals = []
        self.start_session_steps = self.get_server_steps()

    def steps_total(self):
        """total lifetime steps"""
        return self.start_session_steps + self.steps_session()

    def get_server_steps(self):
        pass  # todo

    def steps_session(self):
        """returns how many steps this session"""
        submitted_steps = sum([item.steps for item in self.step_intervals])
        return submitted_steps + self.steps_interval()

    def steps_interval(self):
        """returns how many steps in current interval"""
        return self.arrow_tracker.buttons_pressed

    def update(self):
        self.arrow_tracker.update()
        if (
            self.arrow_tracker.total > 500
            and current_ts() - self.arrow_tracker.last_ts > self.IDLE_TIME
        ):
            self.submit_arrow_tracker()

    def submit_arrow_tracker(self):
        """dumps arrow_tracker to server, and then resets it"""
        interval = self.arrow_tracker.export()
        self.arrow_tracker.reset()
        self.submit_interval(interval)
        self.step_intervals.append(interval)

    def submit_interval(self):
        """submits current interval"""
        pass  # todo: asynchronously submit interval
