class NasaApiUrlBuilder:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.lon = None
        self.lat = None
        self.date = None
        self.dim = None
        self.api_key = None

    def set_lon(self, lon: float) -> 'NasaApiUrlBuilder':
        self.lon = lon
        return self

    def set_lat(self, lat: float) -> 'NasaApiUrlBuilder':
        self.lat = lat
        return self

    def set_date(self, date: str) -> 'NasaApiUrlBuilder':
        self.date = date
        return self

    def set_dim(self, dim: float) -> 'NasaApiUrlBuilder':
        self.dim = dim
        return self

    def set_api_key(self, api_key: str) -> 'NasaApiUrlBuilder':
        self.api_key = api_key
        return self

    def build(self) -> str:
        if not all((self.base_url, self.lon, self.lat, self.date, self.dim, self.api_key)):
            raise ValueError("Missing required parameters to build the URL")
        return f"{self.base_url}?lon={self.lon}&lat={self.lat}&date={self.date}&dim={self.dim}&api_key={self.api_key}"
