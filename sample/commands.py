class Command:
    """Class to store and check different commands"""
    def __init__(self, command_name: str, min_argument_count: int, error_string = "ERROR") -> None:
        self.name = command_name
        self.min_argument_count = min_argument_count
        self.error_message = error_string

    def check_command(self, another : str) -> bool:
        """Check if given command is okay"""
        command = another.split()
        return command[0] == self.name and len(command) > self.min_argument_count

    def wrong_arguments(self, another : str) -> bool:
        """Check if command get the wrong amount of arguments"""
        command = another.split()
        return command[0] == self.name and not self.check_command(another)

    def error(self) -> str:
        """Get error message"""
        return self.error_message
