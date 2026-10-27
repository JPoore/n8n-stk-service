# n8n Send-to-Kindle (stk-service)

A lightweight FastAPI microservice wrapped around `stkclient` that exposes Amazon's unofficial "Send to Kindle" API as a simple local HTTP POST endpoint. 

This project was specifically designed to bypass the quirks of Amazon's `@kindle.com` email gateway so platforms like **n8n** and **Obsidian** can programmatically send PDFs to the Kindle Scribe. Bypassing the email gateway guarantees documents arrive as native **Print Replicas**, retaining the ability to handwrite on pages and preserving the Scribe's native "Share" (export) button.

### ⚠️ AI Generation Disclaimer
> **Disclaimer:** The code, structure, and documentation in this repository were entirely designed, written, and debugged by Google's Gemini large language model during an automated workflow engineering session. 

### Why is this needed?
1. The standard `@kindle.com` email gateway sometimes rejects dynamic PDFs or strips their layout, disabling the native pen tools.
2. `stkclient` defaults to a globally shared device serial number, causing Amazon to throw `403 Forbidden (Failed to validate DeviceInfoToken)` errors when multiple users authenticate. This container securely self-patches `stkclient` on the fly to generate a unique 32-character hex serial derived from your host machine's MAC address.

### Setup Instructions
1. Spin up the container using Docker Compose:
   ```bash
   docker-compose up -d
Follow the URL provided to log into Amazon, then paste the redirect URL back into the terminal.

Usage in n8n
Simply create an HTTP Request node in n8n:

Method: POST

URL: http://<your-server-ip>:3007/send

Send Body: Checked (Multipart Form Data)

Body Parameters:

file: data (Binary PDF File)

title: Journal - Today (String, Optional)

author: Obsidian (String, Optional)

Persistence
The Amazon OAuth tokens are saved to the mapped ./data/client.json volume. Your unique authentication tokens will survive container rebuilds and server reboots.
