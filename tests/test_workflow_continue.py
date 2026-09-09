from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from recall import dump
from native_harnesses import Harness
from workflow_continue import LaunchBudget, advance, claim_live_continuation, position, run_remainder
from workflow_runner import inventory
from workflow_world import initial


class ContinueBoundaries(unittest.TestCase):
    def test_four_slots_are_shared_across_trajectories_without_a_fifth_launch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, output = root / 'source', root / 'output'
            output.mkdir()
            for arm in ('skill', 'no-skill'):
                folder = source / 'trajectories/codex/revenue' / arm
                folder.mkdir(parents=True)
                self.prefix(folder)
            before = inventory(source)
            budget = LaunchBudget(output)
            def successful_session(harness, state, *args):
                state['scheduler']['day'] = state['day'] + 1
                return {'exit_code': 0, 'model_launch_attempted': True}
            with patch('workflow_continue.runner.run_session', side_effect=successful_session) as native:
                harness = Harness('codex', Path('/unused'), {})
                first = run_remainder(harness, 'revenue', 'skill', source, output, True, budget)
                second = run_remainder(harness, 'revenue', 'no-skill', source, output, True, budget)
            self.assertEqual(native.call_count, 4)
            self.assertEqual(budget.used, 4)
            self.assertEqual(first['actual_sessions'], 4)
            self.assertEqual(second['actual_sessions'], 0)
            self.assertEqual(first['stop_reason'], 'owner_session_budget_exhausted')
            self.assertEqual(second['stop_reason'], 'owner_session_budget_exhausted')
            self.assertEqual(inventory(source), before)
            self.assertEqual(len(list((output / 'launch-slots').glob('*.json'))), 4)

    def test_a_second_output_cannot_relaunch_the_same_original_decisions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            claim_live_continuation(root / 'source', root / 'first')
            with self.assertRaises(FileExistsError):
                claim_live_continuation(root / 'source', root / 'second')

    def prefix(self, root, domain='revenue', schedule=7):
        product = root / 'product'
        product.mkdir()
        (product / 'memory.md').write_text('Retained original action and observation')
        after = initial(domain)
        after['scheduler'].update(day=schedule, instruction='Original assignment', enabled=True)
        session = {'index': 0, 'finished_at': 'test', 'exit_code': 0,
            'model_launch_attempted': True, 'temporary_auth_home_removed': True,
            'credential_scan': {'complete': True, 'matches': []},
            'product_after': inventory(product)}
        dump(root / 'sessions/00/manifest.json', session)
        dump(root / 'sessions/00/state-after.json', after)
        boundary = deepcopy(after)
        advance(boundary)
        result = {'domain': domain, 'actual_sessions': 1, 'sessions': [session],
            'state': boundary, 'stop_reason': 'infrastructure_stop_before_launch'}
        dump(root / 'trajectory.json', result)
        return result

    def test_confirmed_wake_retains_original_memory_and_does_not_replay_product_event(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prefix(root)
            state, count, reasons, instruction = position(root)
            self.assertEqual((count, state['day'], reasons, instruction),
                             (1, 7, ['confirmed_schedule'], 'Original assignment'))
            self.assertEqual(state['consumed_events'], ['footer-accessibility'])
            self.assertEqual(state['revision'], 2)
            self.assertEqual(state['scheduler']['day'], 7)

    def test_consumed_owner_instruction_is_preserved_at_the_pending_wake(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prefix(root, 'feedback', None)
            state, count, reasons, instruction = position(root)
            self.assertEqual((count, state['day'], reasons, instruction), (1, 21, ['owner-resume'], None))
            self.assertTrue(state['large_export'])
            self.assertEqual(state['owner_resume_day'], 21)
            self.assertEqual(state['consumed_events'].count('owner-resume'), 1)

    def test_completed_failed_censored_and_corrupted_prefixes_are_refused(self):
        for fault in ('completed', 'failed', 'censored', 'memory', 'clock', 'scan', 'inventory'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                result = self.prefix(root)
                if fault == 'completed':
                    result['stop_reason'] = 'horizon_or_no_further_wake'
                elif fault == 'censored':
                    result['stop_reason'] = 'session_cap'
                elif fault == 'failed':
                    result['sessions'][0]['exit_code'] = 1
                    dump(root / 'sessions/00/manifest.json', result['sessions'][0])
                elif fault == 'scan':
                    result['sessions'][0]['credential_scan']['complete'] = False
                    dump(root / 'sessions/00/manifest.json', result['sessions'][0])
                elif fault == 'memory':
                    (root / 'product/memory.md').write_text('Changed after completed decision')
                elif fault == 'clock':
                    result['state']['day'] = 8
                else:
                    dump(root / 'sessions/01/manifest.json', {})
                dump(root / 'trajectory.json', result)
                with self.assertRaises(ValueError):
                    position(root)

    def test_unlaunched_case_requires_empty_original_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'product').mkdir()
            result = {'domain': 'revenue', 'actual_sessions': 0, 'sessions': [],
                'state': initial('revenue'), 'stop_reason': 'infrastructure_stop_before_launch'}
            dump(root / 'trajectory.json', result)
            self.assertEqual(position(root)[1:], (0, ['initial_owner_request'], None))
            (root / 'product/coaching.md').write_text('Never seed an unlaunched baseline')
            with self.assertRaises(ValueError):
                position(root)


if __name__ == '__main__':
    unittest.main()
