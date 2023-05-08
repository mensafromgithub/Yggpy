class TreeError(Exception):
    def __init__(self, error: dict):
        self.error = error


class TypeError(TreeError):
    def __init__(self, error: dict):
        super().__init__(error)

    def __str__(self):
        return f"Wrong type {self.error['Error']['Type']} for attribute: {self.error['attribute']['Name']}. It can be {', '.join(self.error['attribute']['Types'])}"


class ConnectionError(TreeError):
    def __init__(self, error: dict):
        super().__init__(error)

    def __str__(self):
        return f"Wrong inputs for attribute: {self.error['attribute']['Name']}"
