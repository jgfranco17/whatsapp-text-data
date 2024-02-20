import json
import logging
import os
import re
import sys
from typing import List, Tuple
from .models import ChatMessageEntry, UserData, WhatsappChatLog


logger = logging.getLogger(__name__)

class TextParser:
    def __init__(self, filepath: str):
        # Initialize and validate the file
        self.__filepath = os.path.abspath(filepath)
        self.__contents = []
        if not os.path.exists(self.__filepath):
            raise ValueError(f"File does not exist: {self.__filepath}")
        file, extension = os.path.splitext(self.__filepath)
        if not extension == ".txt":
            raise ValueError(f"Invalid file extension {extension} for file {file}")

        # Read file contents
        try:
            with open(self.__filepath, "r") as chat_file:
                print(f"Read {len(self.__contents)} from file '{filepath}'")
                self.__contents = chat_file.readlines()
                self.__chat_members, self.__chat_messages = self.__read_text_data(self.__contents)

            logger.debug(f"Read {len(self.__chat_messages)} from file.")

        except Exception as e:
            print(f"Failed to initialize chat parser: {e}")
            sys.exit(1)

    @staticmethod
    def __read_text_data(lines: List[str]) -> Tuple[List[UserData], List[ChatMessageEntry]]:
        """Read file lines and parse into ChatMessage data

        Args:
            lines (List[str]): Text lines data

        Returns:
            List[ChatMessage]: Compiled list of parsed data
        """
        REGEX_PATTERN = r"\[(\d{4}/\d{2}/\d{2}), (\d{1,2}:\d{2}:\d{2})\s*(AM|PM)?\]\s*(.*?):\s*(.*)"
        data = []
        members = []
        user_dataclasses = []
        media_count = 0

        try:
            for line in lines:
                line = line.strip()
                if "encrypted" in line:
                    continue
                if "omitted" in line:
                    media_count += 1
                    continue
                match = re.match(REGEX_PATTERN, line)
                if match is not None and match.start() == 0:
                    date = match.group(1)
                    time = match.group(2)
                    am_pm = match.group(3)
                    sender = match.group(4)
                    text = match.group(5)
                    if all((date, time, sender, text)):
                        if sender not in members:
                            members.append(sender)
                        data.append(ChatMessageEntry(
                            date=date.replace("/", "-"),
                            time=f"{time} {am_pm}",
                            sender=sender,
                            text=text
                        ))

            member_data = {member: [] for member in members}
            for member in member_data.keys():
                member_data[member] = [msg.text for msg in data if msg.sender == member]
            for name, chats in member_data.items():
                user_dataclasses.append(UserData(name=name, messages=chats))

            members_listed = " and ".join(members)
            logger.debug(f"{media_count} lines skipped due to media content.")
            print(f"Read {len(data):,} lines for chat history between {members_listed}.")
            return user_dataclasses, data

        except Exception as e:
            raise RuntimeError(f"Failed to parse: {e}") from e

    def filter_by_key(self, keyword: str):
        messages_with_keyword = [msg for msg in self.__chat_messages if keyword in msg.text.lower()]
        count = len(messages_with_keyword)
        print(f"Messages with keyword '{keyword}': {count} ({100*(count/len(self.__chat_messages)):.2f}% of messages)")

    def export_json(self) -> None:
        """Export the JSON representation of the chat data."""
        try:
            filepath_base, _ = os.path.splitext(self.__filepath)
            start_date = self.__chat_messages[0].date
            end_date = self.__chat_messages[-1].date
            filename = f"{filepath_base}_start={start_date}_end={end_date}.json"
            full_file_path = os.path.join(os.getcwd(), filename)

            # Parse the chat into JSON format
            data = WhatsappChatLog(
                file=self.__filepath,
                start=start_date,
                end=end_date,
                length=len(self.__chat_messages),
                users=self.__chat_members,
                entries=self.__chat_messages
            )
            with open(full_file_path, "w") as json_data:
                json.dump(data.to_dict(), json_data, indent=4)
                print(f"Wrote chat to '{filename}'")

        except Exception as e:
            print(f"Failed to export JSON data: {e}")
            sys.exit(1)
