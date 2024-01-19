import datetime
import email.message
import os
import smtplib
import tailscale

ts_client_id = os.getenv('TS_CLIENT_ID')
ts_client_secret = os.getenv('TS_CLIENT_SECRET')

tsc = tailscale.TailscaleAPIClient()
tsc.set_oauth_client_info(ts_client_id, ts_client_secret)
tsc.set_token(tsc.get_oauth_token())

now = datetime.datetime.now(tz=datetime.UTC)

alerts = []
for d in tsc.devices():
    device_name = d.get('name').split('.')[0]
    device_expires = datetime.datetime.strptime(d.get('expires'), '%Y-%m-%dT%H:%M:%SZ').astimezone(datetime.UTC)
    if d.get('updateAvailable'):
        alerts.append(f'A client update is available for {device_name}')
    if device_expires < now:
        alerts.append(f'The key for {device_name} has expired.')
    elif device_expires < now + datetime.timedelta(days=15):
        alerts.append(f'The key for {device_name} will expire at {device_expires}')

for alert in alerts:
    print(alert)

if alerts:
    msg = email.message.EmailMessage()
    msg['Subject'] = 'Tailscale network alerts'
    msg['From'] = os.getenv('SMTP_FROM')
    msg['To'] = os.getenv('SMTP_TO')
    msg.set_content('\n'.join(alerts))
    with smtplib.SMTP_SSL(host=os.getenv('SMTP_SERVER')) as s:
        s.login(user=os.getenv('SMTP_USERNAME'), password=os.getenv('SMTP_PASSWORD'))
        s.send_message(msg)
