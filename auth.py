import glob, re, hashlib, uuid
# Generate a unique 32-hex serial for this specific machine to prevent Amazon DeviceInfoToken 403 errors
sn = hashlib.md5(str(uuid.getnode()).encode()).hexdigest().upper()
for p in glob.glob("/usr/local/lib/python*/site-packages/stkclient/*.py"):
    txt = open(p).read()
    new_txt = re.sub(r"\b[0-9A-F]{32}\b", sn, txt, flags=re.I)
    if new_txt != txt: open(p, "w").write(new_txt)

import stkclient
oauth = stkclient.OAuth2()
print("\n1. Open this URL and sign in:\n" + oauth.get_signin_url())
url = input("\n2. Paste Redirect URL: ").strip()
c = oauth.create_client(url)
with open("/data/client.json", "w") as f:
    c.dump(f)
devs = c.get_owned_devices()
devs_list = getattr(devs, "owned_devices", devs)
print("\nSuccess! Devices:", [(getattr(d, "device_name", "Device"), getattr(d, "device_serial_number", "")) for d in devs_list])
