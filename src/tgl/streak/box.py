from datetime import datetime


class Box:
    def __init__(self, name: str):
        self.name = name
        self.headline = ""
        self.location = ""
        self.email = ""
        self.phone = ""
        self._connected = None
        self.linkedin = ""

    @property
    def connected(self):
        if self._connected is not None:
            return int(self._connected.timestamp())
        else:
            return ""

    @connected.setter
    def connected(self, value: datetime):
        self._connected = value

    def first_name(self):
        return self.name.split()[0]

    def __str__(self):
        return (
            f"Box: name={self.name}, Headline={self.headline},"
            f" Location={self.location},"
            f" Email={self.email}, Phone={self.phone},"
            f" Connected={self.connected}, Linkedin={self.linkedin}"
        )
