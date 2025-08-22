
# Week 5 — SSL (Self-Signed), Monitoring, Documentation & Finalization

> Secure the stack end-to-end using a **self-signed certificate** for HTTPS, add observability, and finalize docs.

This week you’ll add an HTTPS reverse proxy (NGINX) that uses a **self-signed TLS cert** (good for local/dev and quick demos), bring up **Prometheus + Grafana** monitoring (with optional Blackbox HTTP probes), and finish documentation.

> ⚠️ Self-signed certificates are **not trusted** by browsers by default. Expect a warning page unless you add the cert to your OS/browser trust store. Use Let’s Encrypt or a managed cert in real production.

---

## What you’ll build

* **TLS/SSL termination** with **NGINX** using a self-signed certificate.
* **Monitoring** via **Prometheus** + **Grafana** (optional **Blackbox Exporter**).
* **Documentation**: final project README, architecture diagram.

---

## Repo map (Week 5 bits)

* `nginx/default.conf` — reverse-proxy config.
* `frontend/certs/` — local directory to hold `selfsigned.crt` and `selfsigned.key` (you create this).
* `prometheus/` — Prometheus config (e.g., `prometheus.yml`).
* `grafana/provisioning/` — Grafana datasource/dashboard provisioning (optional).
* `blackbox.simple.yml` — example Blackbox Exporter config (optional).
* `docker-compose.yml` — core stack (monitoring may be in a separate compose file).

---

## Prereqs

* A host (local Docker or EC2) with Docker & Docker Compose.
* Open security group / firewall for ports **80** and **443** (and **9090**, **13000**, **9115** if exposing monitoring).

---

## 1) HTTPS with a self-signed cert

### A) Generate the certificate

Create a `frontend/certs/` folder at the repo root and generate a key/cert pair with Subject Alternative Names (SANs). Replace values to match your setup (domain or IP):

```
mkdir -p frontend/certs

# Example for a dev hostname and an IP (adjust as needed)
openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes \
  -keyout certs/selfsigned.key -out certs/selfsigned.crt \
  -subj "/CN=app.local" \
  -addext "subjectAltName=DNS:app.local,IP:127.0.0.1,IP:<IP_ADDRESS>"
```


### B) NGINX reverse proxy config

Update `frontend/default.conf` to point at the certs and your app services:

```
# HTTPS
server {
  listen 443 ssl http2;
  server_name _;
  
  ...
  
  ssl_certificate     /etc/nginx/certs/selfsigned.crt;
  ssl_certificate_key /etc/nginx/certs/selfsigned.key;
  
  ...
}
```

### C) Compose service for the proxy

Add or update the reverse proxy in your docker-compose.yml (use your actual network/services):

Bring it up:

```
docker-compose stop frontend
docker-compose up -d
```

### D) Browser trust (dev)

* Visit `https://<host>` — you’ll see a trust warning (expected).
* For a cleaner local experience, import `certs/selfsigned.crt` into your OS/browser trust store.
* For CLI checks, skip verification: `curl -k https://<host>`.

---

## 2) Monitoring stack (Prometheus + Grafana)

Give your 3-tier app basic observability: **Prometheus** scrapes metrics/health, **Grafana** visualizes them, and the **Blackbox Exporter** can probe your public HTTP endpoint (useful even if the app doesn’t expose `/metrics`). This setup is lightweight and dev-friendly, works fine with your **self-signed TLS**.

### How it fits together

* **Prometheus** pulls metrics on an interval (e.g., every 15s) from targets inside your Docker network and from Blackbox probes.
* **Grafana** is pre-wired to Prometheus and can auto-load dashboards via provisioning.
* **Blackbox Exporter** runs HTTP checks against your app URL (e.g., `https://<host>/health`).

### Files & what they contain (quick read)

* `prometheus/prometheus.yml` → Global scrape interval + jobs for **backend** and **frontend** (container DNS names/ports), plus an optional **blackbox** job that probes `https://<host>/health`.
* `blackbox.simple.yml` → Probe **modules** (e.g., `http_2xx`); you can enable `insecure_skip_verify` for self-signed HTTPS if needed.
* `grafana/provisioning/datasources/datasource.yml` → A **Prometheus datasource** pointing to `http://<host>:9090`, usually marked as default.
* `grafana/provisioning/dashboards/dashboards.yml` + `grafana/provisioning/dashboards/*.json` → Tells Grafana to **auto-import** dashboards from JSON files into a named folder.
* `monitoring/docker-compose-monitoring.yml` (optional) → Defines the **Prometheus**, **Grafana**, and **Blackbox Exporter** services, their ports (e.g., 9090/13000/9115), volumes, and the shared Docker network.

### Bring it up (high-level)

* Ensure your app services are running on the same Docker network (e.g., `appnet`).
* Start monitoring:
  `docker compose -f monitoring/docker-compose-monitoring.yml up -d`
* Visit **Prometheus** at `http://<host>:9090` and **Grafana** at `http://<host>:13000` (change the admin password on first login).

### What you should see

* Prometheus **Targets** for your frontend/backend show **UP**.
* A Blackbox probe returning **2xx** for `https://<host>/health` (expected to work with self-signed; configure the module accordingly).
* Grafana shows pre-provisioned dashboards/datasources without manual clicks.

### Tips

* Keep Prometheus/Blackbox inside the private network; only expose Grafana if you must (and protect it).

---


## 5) Validation checklist

* [ ] `https://<host>` loads the app via NGINX (browser shows a **self-signed warning**).
* [ ] `curl -k https://<host>/health` returns `ok`.
* [ ] Prometheus targets are **UP** and scraping.
* [ ] Grafana has a Prometheus datasource and shows live panels.
* [ ] (If used) Blackbox probe reports `http_2xx` for your endpoint.

---

## 6) Troubleshooting

* **Browser says “Not Secure”** → expected for self-signed; import `selfsigned.crt` into trust store or proceed with the warning.
* **TLS handshake errors** → ensure SANs include the exact hostname/IP you’re using; regenerate the cert with correct SANs.
* **NGINX fails to start** → `docker compose logs reverse-proxy`; test config with `nginx -t`.
* **Prometheus target down** → verify container names/ports and Docker network; `docker exec -it <prometheus> wget -qO- http://backend:8080/health`.

---

## 7) TO-DO

* Update `architecture.png` to include **NGINX (TLS)** + **Prometheus/Grafana**.

---
