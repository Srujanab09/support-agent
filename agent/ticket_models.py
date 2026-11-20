"""Data models for support tickets in data/tickets.jsonl."""
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

Category = Literal["discovery", "jobs", "alerts", "firmware", "api", "other"]
Urgency = Literal["low", "medium", "high", "critical"]
AskFor = Literal["version", "error_code", "device_ids", "discovery_settings", "time_window"]
Tool = Literal[
    "find_device", "get_device", "list_alerts", "list_groups", "get_discovery_job",
    "get_job", "list_jobs", "start_discovery", "rerun_job", "start_firmware_update",
]
TicketId = Annotated[str, StringConstraints(pattern=r"^T-\d{3}$")]
DeviceId = Annotated[str, StringConstraints(pattern=r"^srv-[a-z]-\d{3}$")]
ErrorCode = Annotated[str, StringConstraints(pattern=r"^(DSC|JOB|FW)-\d{3}$")]


class Expected(BaseModel):
    """The answer key: what a correct agent should do with this ticket."""
    category: Category
    urgency: Urgency
    ask_for: list[AskFor]
    tools: list[Tool]


class Ticket(BaseModel):
    id: TicketId
    created: date
    subject: Annotated[str, StringConstraints(min_length=5)]
    body: Annotated[str, StringConstraints(min_length=10)]
    version: str | None
    device_ids: list[DeviceId]
    error_code: ErrorCode | None
    expected: Expected


def load_tickets(path: Path) -> list[Ticket]:
    """Read one ticket per line, and fail with the line number if one is invalid."""
    tickets = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                tickets.append(Ticket.model_validate_json(line))
            except ValueError as err:
                raise ValueError(f"Line {line_no} is not a valid ticket:\n{err}") from err
    return tickets
