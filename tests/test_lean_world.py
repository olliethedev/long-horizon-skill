from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'evals'))
from lean_world import advance, call, initial
from workflow_client import LocalConnection
from workflow_service import ProductService


class LeanWorld(unittest.TestCase):
    def test_refunds_mature_and_historical_data_remain_queryable(self):
        world = initial()
        advance(world, 0)
        result = call(world, 'experiments.start', {'page': 'ci-runners', 'variants': [
            {'approach': 'practical', 'body': 'A hands-on guide'},
            {'approach': 'promotional', 'body': 'A promotional guide'}]})
        ids = {v['approach']: v['id'] for v in result['data']['variants']}
        advance(world, 7)
        early = call(world, 'analytics.query', {'from_day': 0, 'to_day': 7})['data']
        advance(world, 14)
        mature = call(world, 'analytics.query', {'from_day': 0, 'to_day': 7})['data']
        early_rows = {r['publication']: r for r in early['rows'] if r['page'] == 'ci-runners' and r['cohort'] == 'teams'}
        rows = {r['publication']: r for r in mature['rows'] if r['page'] == 'ci-runners' and r['cohort'] == 'teams'}
        self.assertGreater(early_rows[ids['promotional']]['observed_net_commission'], early_rows[ids['practical']]['observed_net_commission'])
        self.assertLess(rows[ids['promotional']]['observed_net_commission'], rows[ids['practical']]['observed_net_commission'])
        self.assertEqual(sum(r['pending_refund_visits'] for r in rows.values()), 0)
        advance(world, 35)
        current = call(world, 'site.read', {'page': 'ci-runners'})['data']
        self.assertNotIn(ids['practical'], str(current))
        queried = call(world, 'analytics.query', {'from_day': 0, 'to_day': 7})['data']
        self.assertEqual(queried['rows'], mature['rows'])
        self.assertNotIn('approach', json.dumps(queried['rows']))

    def test_independent_worlds_and_real_socket_dispatch(self):
        a, b = initial(), initial()
        advance(a, 0)
        advance(b, 0)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ProductService(root / 's', a, root / 'state.json', call):
                client = LocalConnection(root / 's', 2)
                client.request('POST', '/', json.dumps({'operation': 'site.publish', 'arguments': {'page': 'ci-runners', 'approach': 'practical', 'body': 'Try this workflow.'}}))
                self.assertTrue(json.loads(client.getresponse().read())['ok'])
                client.close()
            self.assertEqual(b['pages']['ci-runners']['variants'][0]['approach'], 'neutral')
            self.assertEqual(a['pages']['ci-runners']['variants'][0]['approach'], 'practical')
            before = json.dumps(a['pages'], sort_keys=True)
            self.assertFalse(call(a, 'site.publish', {'page': 'ci-runners', 'approach': 'invalid', 'body': 'x'})['ok'])
            self.assertEqual(json.dumps(a['pages'], sort_keys=True), before)

    def test_reader_conditions_change_without_erasing_old_measurements(self):
        world = initial()
        advance(world, 35)
        call(world, 'experiments.start', {'page': 'log-collectors', 'variants': [
            {'approach': 'technical', 'body': 'Detailed internals'}, {'approach': 'practical', 'body': 'Working examples'}]})
        advance(world, 90)
        data = call(world, 'analytics.query', {'from_day': 35, 'to_day': 83})['data']['rows']
        rows = [r for r in data if r['page'] == 'log-collectors' and r['cohort'] == 'teams']
        self.assertEqual({r['reader_mix'] for r in rows}, {'established readers', 'newly adopting teams'})
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(world['releases']), 2)


if __name__ == '__main__':
    unittest.main()
