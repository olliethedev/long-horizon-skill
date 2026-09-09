"""Deterministic evaluation time; product events never imply agent wakeups."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Event:
    identity: str
    day: int
    kind: Literal['product', 'owner']
    wake: bool = False

    def __post_init__(self) -> None:
        if self.day < 0:
            raise ValueError('Event day must be nonnegative')
        if self.kind == 'product' and self.wake:
            raise ValueError('A product event cannot implicitly wake the agent')


@dataclass(frozen=True)
class Transition:
    day: int
    events: tuple[Event, ...]
    scheduled_run_due: bool

    @property
    def wake_reasons(self) -> tuple[str, ...]:
        owner = tuple(event.identity for event in self.events if event.wake)
        return owner + (('confirmed_schedule',) if self.scheduled_run_due else ())


def next_transition(*, day: int, horizon: int, events: tuple[Event, ...],
                    consumed: frozenset[str], scheduled_day: int | None,
                    enabled: bool) -> Transition | None:
    """Choose time only; the caller applies events before starting any agent.

    Consumed identities make same-day events possible without replaying them.
    Each arm supplies its own schedule and consumed set against the same event
    tape. A disabled task ignores its stale scheduled date but can still receive
    an explicit owner instruction. One timestamp produces at most one wake.
    """
    if day < 0 or horizon < day:
        raise ValueError('Expected 0 <= current day <= horizon')
    identities = [event.identity for event in events]
    if len(set(identities)) != len(identities):
        raise ValueError('Event identities must be unique')
    pending = tuple(event for event in events if event.identity not in consumed)
    if any(event.day < day for event in pending):
        raise ValueError('An earlier event was not consumed')
    if enabled and scheduled_day is not None and scheduled_day < day:
        raise ValueError('A due run cannot be silently skipped')
    candidates = [event.day for event in pending if event.day <= horizon]
    if enabled and scheduled_day is not None and scheduled_day <= horizon:
        candidates.append(scheduled_day)
    if not candidates:
        return None
    next_day = min(candidates)
    due_events = tuple(sorted((event for event in pending if event.day == next_day),
                             key=lambda event: (event.kind != 'product', event.identity)))
    return Transition(next_day, due_events, enabled and scheduled_day == next_day)
