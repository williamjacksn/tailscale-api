class TailscaleAPIClient:
    base_url = 'https://api.tailscale.com/api/v2'

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
