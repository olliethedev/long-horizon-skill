import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from workflow_clock import Event, next_transition


class WorkflowClock(unittest.TestCase):
    def test_world_changes_do_not_rescue_a_missing_schedule(self):
        tape = (Event('revision', 7, 'product'), Event('audit', 28, 'product'))
        day, consumed, wakes = 0, frozenset(), []
        while True:
            step = next_transition(day=day, horizon=42, events=tape, consumed=consumed,
                                   scheduled_day=None, enabled=True)
            if step is None:
                break
            day = step.day
            consumed |= frozenset(event.identity for event in step.events)
            wakes.extend(step.wake_reasons)
        self.assertEqual(consumed, frozenset({'revision', 'audit'}))
        self.assertEqual(wakes, [])

    def test_tied_events_apply_before_one_combined_wake(self):
        tape = (Event('owner-scope', 7, 'owner', True), Event('deployment', 7, 'product'))
        step = next_transition(day=0, horizon=42, events=tape, consumed=frozenset(),
                               scheduled_day=7, enabled=True)
        self.assertEqual([event.identity for event in step.events], ['deployment', 'owner-scope'])
        self.assertEqual(step.wake_reasons, ('owner-scope', 'confirmed_schedule'))

    def test_paused_task_requires_explicit_owner_wake_after_restoration(self):
        tape = (Event('access-restored', 14, 'product'), Event('resume', 21, 'owner', True))
        restored = next_transition(day=7, horizon=42, events=tape, consumed=frozenset(),
                                   scheduled_day=10, enabled=False)
        self.assertEqual(restored.day, 14)
        self.assertEqual(restored.wake_reasons, ())
        resumed = next_transition(day=14, horizon=42, events=tape,
                                  consumed=frozenset({'access-restored'}),
                                  scheduled_day=10, enabled=False)
        self.assertEqual(resumed.day, 21)
        self.assertEqual(resumed.wake_reasons, ('resume',))

    def test_independent_schedules_share_the_same_event_tape(self):
        tape = (Event('audit', 14, 'product'),)
        early = next_transition(day=0, horizon=42, events=tape, consumed=frozenset(),
                                scheduled_day=7, enabled=True)
        late = next_transition(day=0, horizon=42, events=tape, consumed=frozenset(),
                               scheduled_day=21, enabled=True)
        self.assertEqual((early.day, early.scheduled_run_due), (7, True))
        self.assertEqual((late.day, late.scheduled_run_due), (14, False))
        self.assertEqual(tape, (Event('audit', 14, 'product'),))

    def test_future_run_beyond_horizon_is_not_executed(self):
        self.assertIsNone(next_transition(day=42, horizon=42, events=(),
                                         consumed=frozenset(), scheduled_day=49, enabled=True))

    def test_missed_events_or_runs_cannot_be_silently_discarded(self):
        for events, scheduled in (((Event('missed', 7, 'product'),), None), ((), 7)):
            with self.subTest(events=events, scheduled=scheduled), self.assertRaises(ValueError):
                next_transition(day=14, horizon=42, events=events, consumed=frozenset(),
                                scheduled_day=scheduled, enabled=True)


if __name__ == '__main__':
    unittest.main()
