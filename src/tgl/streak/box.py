class Box:
    def __init__(self, name: str):
        self.name = name
        self.headline = ""
        self.location = ""
        self.position = ""
        self.company = ""
        self.email = ""
        self.phone = ""
        # self.connected = ""

    def first_name(self):
        return self.name.split()[0]

    def __str__(self):
        return (
            f"Box: name={self.name}, Headline={self.headline},"
            f" Location={self.location}, Position={self.position},"
            f" Company={self.company}, Email={self.email}, Phone={self.phone},"
            # f" Connected={self.connected}"
        )
