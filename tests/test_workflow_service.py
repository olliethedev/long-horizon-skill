import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from workflow_client import LocalConnection
from workflow_service import ProductService
from workflow_world import initial


class WorkflowService(unittest.TestCase):
    def test_lost_ack_replay_and_revision_conflict_preserve_one_effect(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            state = initial('revenue')
            socket = folder / 'service.sock'
            with ProductService(socket, state, folder / 'state.json'):
                def request(operation, arguments):
                    result = subprocess.run([sys.executable, str(ROOT / 'evals/workflow_client.py'),
                                             operation, json.dumps(arguments), '--socket', str(socket)],
                                            capture_output=True, text=True, check=True)
                    return json.loads(result.stdout)
                request('owner.ask', {'topic': 'authority', 'question': 'What changes may I make?'})
                args = {'request_id': 'offer-a', 'expected_revision': 1,
                        'config': {'offer': 'compact', 'include_wallet': True}}
                self.assertEqual(request('change', args)['error'], 'response_lost')
                self.assertEqual(request('status', {})['revision'], 2)
                self.assertTrue(request('change', args)['replayed'])
                self.assertEqual(request('change', {**args, 'request_id': 'offer-b'})['error'], 'revision_conflict')
                self.assertEqual(state['revision'], 2)
                self.assertEqual(len(state['operations']), 1)
                self.assertEqual(state['violations'], [])
            self.assertFalse(socket.exists())

    def test_socket_cannot_select_or_mutate_another_trajectory(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            first, second = initial('revenue'), initial('feedback')
            with ProductService(folder / 'a.sock', first, folder / 'a.json'), \
                 ProductService(folder / 'b.sock', second, folder / 'b.json'):
                connection = LocalConnection(folder / 'a.sock')
                try:
                    connection.request('POST', '/', json.dumps({'operation': 'lifecycle',
                        'arguments': {'request_id': 'stop-b', 'status': 'terminated'}, 'trial': 'b'}))
                    response = connection.getresponse()
                    self.assertEqual(response.status, 400)
                    response.read()
                finally:
                    connection.close()
                self.assertEqual(first['scheduler']['status'], 'active')
                self.assertEqual(second['scheduler']['status'], 'active')


if __name__ == '__main__':
    unittest.main()
