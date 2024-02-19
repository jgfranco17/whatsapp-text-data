import datetime as dt
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ChatMessageEntry:
    """Object represention of a chat message entry."""
    date: str
    time: str
    sender: str
    text: str

    def to_dict(self) -> Dict[str, str]:
        """Convert the data to dictionary format.

        Returns:
            Dict[str, str]: Dictionary of data
        """
        return {
            "date": self.date,
            "time": self.time,
            "sender": self.sender,
            "text": self.text
        }


@dataclass(frozen=True)
class UserData:
    name: str
    messages: List[ChatMessageEntry]


@dataclass(frozen=True)
class WhatsappChatLog:
    file: str
    start: str
    end: str
    length: int
    users: List[UserData]
    entries: List[ChatMessageEntry]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.file,
            "start": self.start,
            "end": self.end,
            "duration": days_between_dates(start_date=self.start, end_date=self.end),
            "length": self.length,
            "users": [
                {
                    "name": user.name,
                    "count": len(user.messages),
                    "messages": user.messages
                } for user in self.users
            ],
            "history": [entry.to_dict() for entry in self.entries]
        }


def days_between_dates(start_date: str, end_date: str, date_format: str = "%Y-%m-%d"):
    if not date_format:
        raise ValueError(f"Invalid date format provided: '{date_format}'")
    start_datetime = dt.datetime.strptime(start_date, date_format)
    end_datetime = dt.datetime.strptime(end_date, date_format)
    delta = end_datetime - start_datetime
    return delta.days