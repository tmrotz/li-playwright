class Box:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def first_name(self):
        return self._name.split()[0]

    @property
    def box_key(self):
        return self._box_key

    @box_key.setter
    def box_key(self, box_key: str):
        self._box_key = box_key

    @property
    def stage_key(self):
        return self._stage_key

    @stage_key.setter
    def stage_key(self, stage_key: str):
        self._stage_key = stage_key

    @property
    def headline(self):
        return self._headline

    @headline.setter
    def headline(self, headline: str):
        self._headline = headline

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location: str):
        self._location = location

    def __str__(self):
        return f"Box: name={self._name}, headline={self._headline}, location={self._location}"
