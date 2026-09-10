# Local Impulse integration

Both recorded integration runs passed. A scheduled continuation survived a deliberately failed script and a daemon restart; a fresh process recovered the retained files and disabled future work. Replaying the same request ID did not duplicate the operation. Final cleanup reported no errors and the isolated daemon was stopped.

The test used a temporary `IMPULSE_HOME`, scripts and about twelve seconds of real elapsed time. It used no model sessions, production tasks or external notices. This verifies a local scheduling boundary, not autonomous product outcomes.

Run the maintained test with a fresh local output directory:

```sh
python3 evals/impulse_integration.py --output evals/runs/impulse-NEW
```

Detailed receipts and logs are retained locally.
