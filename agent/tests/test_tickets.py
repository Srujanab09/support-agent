from pathlib import Path

import pytest

from ticket_models import load_tickets

DATA = Path(__file__).resolve().parents[2] / "data" / "tickets.jsonl"


@pytest.fixture(scope="module")
def tickets():
    return load_tickets(DATA)


def test_there_are_20_tickets(tickets):
    assert len(tickets) == 20


def test_ids_are_unique(tickets):
    ids = [t.id for t in tickets]
    assert len(ids) == len(set(ids))


def test_every_category_is_used(tickets):
    used = {t.expected.category for t in tickets}
    assert used == {"discovery", "jobs", "alerts", "firmware", "api", "other"}


def test_ask_for_matches_what_is_missing(tickets):
    for t in tickets:
        if "version" in t.expected.ask_for:
            assert t.version is None, f"{t.id} asks for the version but already has one"
        if "error_code" in t.expected.ask_for:
            assert t.error_code is None, f"{t.id} asks for the error code but already has one"
        if "device_ids" in t.expected.ask_for:
            assert not t.device_ids, f"{t.id} asks for device IDs but already lists some"
