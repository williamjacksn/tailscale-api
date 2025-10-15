import httpx

from . import models


class TailscaleAPIClient:
    base_url: str = "https://api.tailscale.com/api/v2"
    client_id: str = None
    client_secret: str = None
    session: httpx.Client = httpx.Client()

    def devices(self) -> list[models.Device]:
        url = f"{self.base_url}/tailnet/-/devices"
        response = self.session.get(url)
        response.raise_for_status()
        return [models.Device(d) for d in response.json().get("devices")]

    def get_oauth_token(self) -> str:
        url = f"{self.base_url}/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def set_oauth_client_info(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def set_token(self, token: str) -> None:
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
            }
        )
