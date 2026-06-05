# Tailscale API tools

## Contents

**`tailscale_api`**

This module provides the `TailscaleAPIClient` object for working with the
[Tailscale API][a]. You can authenticate with the API using either an API access token
or an OAuth client ID and secret.

[a]: https://tailscale.com/kb/1101/api

```python
import tailscale_api

tsc = tailscale_api.TailscaleAPIClient()

# authenticate with an access token
token = 'tskey-api-...'
tsc.set_token(token)
for device in tsc.devices():
    print(device.name)

# authenticate with oauth
ts_client_id = 'kHJw5W...'
ts_client_secret = 'tskey-client-...'
tsc.set_oauth_client_info(ts_client_id, ts_client_secret)
tsc.set_token(tsc.get_oauth_token())
for device in tsc.devices():
    print(device.name)
```

The `TailscaleAPIClient` object does not currently support all available features of the Tailscale API.
