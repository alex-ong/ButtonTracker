"""
Simple step tracking class
"""
from dataclasses import dataclass
from buttontrack.arrowstate import ArrowState
from buttontrack.time import current_ts
from buttontrack.stats import readfile, writefile


class StepTracker:
    IDLE_TIME = 30  # time in seconds
    MIN_STEPS_PER_INTERVAL = 500  # minimum number of steps to submit

    def __init__(self, arrow_state: ArrowState):
        self.arrow_tracker = arrow_state
        self.step_intervals = []
        self.start_session_steps = self.get_server_steps()

    def get_server_steps(self):
        """returns how many steps we have done"""
        return readfile()

    @property
    def steps_total(self):
        """total lifetime steps"""
        return self.start_session_steps + self.steps_session

    @property
    def steps_session(self):
        """returns how many steps this session"""
        submitted_steps = sum([item.num_steps for item in self.step_intervals])
        return submitted_steps + self.steps_interval

    @property
    def steps_interval(self):
        """returns how many steps in current interval"""
        return self.arrow_tracker.buttons_pressed

    def update(self):
        """Async update to submit intervals to server"""
        if (
            self.arrow_tracker.step_count > self.MIN_STEPS_PER_INTERVAL
            and self.arrow_tracker.is_neutral
            and current_ts() - self.arrow_tracker.last_updated > self.IDLE_TIME
        ):
            self.submit_arrow_tracker()

    def submit_arrow_tracker(self):
        """dumps arrow_tracker to server, and then resets it"""
        interval = self.arrow_tracker.create_new_interval()
        self.submit_interval(interval)
        self.step_intervals.append(interval)

    def submit_interval(self, interval):
        """submits current interval"""
        pass  # todo: asynchronously submit interval
