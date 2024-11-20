from typing import Text


class CharlatanExceptions(Exception):
    def __init__(self, text):
        self.text = text

    def get_message(self) -> Text:
        return self.text or " "


class AgentNotExists(CharlatanExceptions):
    """Doesnt exists Agent in Charlatan_Manager"""
    def __init__(self, text):
        super().__init__(text)


class AgentNotReady(CharlatanExceptions):
    def __init__(self, text):
        """Agent.isReady() = false """
        super().__init__(text)


class FolderNotFound(CharlatanExceptions):
    def __init__(self, text):
        """Not found the folder"""
        super().__init__(text)
