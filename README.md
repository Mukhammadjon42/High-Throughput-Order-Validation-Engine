# High-Throughput Order Validation Engine

A containerized, production-grade microservice architecture designed to validate stock trade requests, prevent double-executions (idempotency management), and simulate strict financial network isolation. 

This project demonstrates practical implementations of multi-container networking, stateful caching, safe Docker volume binding, and automated structured logging—key skills required for Production Support, Trade Support, and DevOps environments.

---

## 🏗️ Architecture Blueprint

The system splits infrastructure into two isolated network zones to mirror strict banking security practices:
1. **`frontend-gw` (Public Ingress):** Exposes port `9000` to allow client applications or upstream order routers to communicate with the Web API.
2. **`backend-secure` (Private Data Tier):** A completely isolated network bridging the API and the Redis database cache. The Redis instance exposes no public ports to the host machine, mitigating external security threats.

### 4. Reading and Auditing Logs (Support Operations)

As a Production Support Specialist, you can monitor and audit the system logs using two different methodologies depending on your access rights:

#### Method A: Tailing Logs from the Host Filesystem (Recommended)
Because of the active volume bind-mount, logs are streamed directly to your host machine. You can read them using standard Linux command-line utilities without accessing the container:
```bash

# Dump all container console logs
docker compose logs

# Follow/stream live application logs dynamically
docker compose logs -f order-engine

# Read the entire log history
cat live_logs/engine.log

# Stream/tail the logs in real-time as trades come in
tail -f live_logs/engine.log

```text
 [ Upstream Client / Curl ] 
            │
    (Port 9000 Ingress)
            ▼
┌───────────────────────────┐
│       order-engine        │  ◄─── (Shares frontend-gw & backend-secure)
└───────────┬───────────────┘
            │
    (Internal DNS Routing)
            ▼
┌───────────────────────────┐
│        order-cache        │  ◄─── (Isolated in backend-secure tier)
│         (Redis)           │       [No Public Ingress Allowed]
└───────────────────────────┘
