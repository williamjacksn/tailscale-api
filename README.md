# Tailscale API tools

This repository contains tools for working with the [Tailscale API][a].

[a]: https://tailscale.com/kb/1101/api

### Contents

**`tailscale_api`**

This module provides the `TailscaleAPIClient` object for working with the API. You can
authenticate with the API using either an API access token or an OAuth client ID and
secret.

```python
import tailscale_api

tsc = tailscale_api.TailscaleAPIClient()

# authenticate with an access token
token = 'tskey-api-...'
tsc.set_token(token)
for device in tsc.devices():
    print(device.get('name'))

# authenticate with oauth
ts_client_id = 'kHJw5W...'
ts_client_secret = 'tskey-client-...'
tsc.set_oauth_client_info(ts_client_id, ts_client_secret)
tsc.set_token(tsc.get_oauth_token())
for device in tsc.devices():
    print(device.get('name'))
```

**`examples/check-devices.py`**

This script will check all devices in a Tailscale network, and send a notification email
if any devices:

* have a Tailscale software update available
* have a machine key that will expire within 15 days
* have a machine key that has already expired

This script is only provided as an example. If you want to use the script as it is
written, you will need to provide Tailscale OAuth information and SMTP server
credentials using environment variables.
