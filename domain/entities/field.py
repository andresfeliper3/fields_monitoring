class Field:
    def __init__(self, field_id: str, lon: float, lat: float, dim: float, date: str):
        self.field_id = field_id
        self.lon = lon
        self.lat = lat
        self.dim = dim
        self.date = date
