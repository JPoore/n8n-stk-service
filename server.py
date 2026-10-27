import os, glob, re, hashlib, tempfile, uuid
# Self-patch stkclient with a machine-unique serial on startup
sn = hashlib.md5(str(uuid.getnode()).encode()).hexdigest().upper()
for p in glob.glob("/usr/local/lib/python*/site-packages/stkclient/*.py"):
    txt = open(p).read()
    new_txt = re.sub(r"\b[0-9A-F]{32}\b", sn, txt, flags=re.I)
    if new_txt != txt: open(p, "w").write(new_txt)

import stkclient
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

app = FastAPI()
CLIENT_FILE = Path("/data/client.json")

@app.post("/send")
async def send_to_kindle(file: UploadFile = File(...), title: str = Form(None), author: str = Form("Obsidian")):
    if not CLIENT_FILE.exists():
        raise HTTPException(status_code=500, detail="client.json missing. Run auth.py inside the container first.")
    with open(CLIENT_FILE, "r") as f:
        client = stkclient.Client.load(f)
        
    devs_resp = client.get_owned_devices()
    devs = getattr(devs_resp, "owned_devices", devs_resp)
    dest = [d.device_serial_number for d in devs if hasattr(d, "device_serial_number")]
    
    if not dest:
        raise HTTPException(status_code=404, detail="No Kindle devices found")
        
    suffix = Path(file.filename).suffix or ".pdf"
    doc_title = title or Path(file.filename).stem
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)
        
    try:
        # Pushing force_convert=False to maintain native Print Replica status for Kindle Scribe
        client.send_file(tmp_path, dest, author=author, title=doc_title, format=suffix.lstrip(".").lower())
        with open(CLIENT_FILE, "w") as f:
            client.dump(f)
    finally:
        if tmp_path.exists():
            os.remove(tmp_path)
            
    return {"status": "sent", "title": doc_title, "destinations": dest}
