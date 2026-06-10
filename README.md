# RigSignal — Elastic Fleet Integration

Elastic Fleet integration package for [RigSignal](https://github.com/MathewRJ/RigSignal) — real-time gaming telemetry for Elasticsearch.

Captures FPS, frame timing percentiles, GPU/CPU thermals and utilisation, memory, storage, network, audio, power, and kernel-level scheduler/I/O/GPU traces via eBPF.

## Install via Fleet (custom registry)

Add the RigSignal custom package registry to your Fleet instance, then install like any other integration.

**1. Configure Fleet to use the RigSignal registry**

In Kibana: `Fleet → Settings → Package Registry URL`

Set to: `https://MathewRJ.github.io/RigSignal-Integration`

**2. Install the integration**

`Fleet → Integrations → search "RigSignal" → Add RigSignal`

**3. Install the agent binary**

Download the rigsignal-agent for your platform from the [RigSignal releases page](https://github.com/MathewRJ/RigSignal/releases).

**4. Configure the agent**

Create `/etc/rigsignal/rigsignal.toml` (Linux) or `%APPDATA%\rigsignal\rigsignal.toml` (Windows):

```toml
[elasticsearch]
url      = "https://your-instance.es.us-central1.gcp.elastic.cloud"
api_key  = "your-ingest-api-key"
```

The ingest API key needs `create_doc` + `auto_configure` on `metrics-rigsignal.*` and `logs-rigsignal.*`.

## Data streams

| Stream | Type | Content |
|---|---|---|
| `metrics-rigsignal.cpu-*` | metrics | CPU utilisation, temperature, frequency |
| `metrics-rigsignal.gpu-*` | metrics | GPU utilisation, VRAM, temperature, power |
| `metrics-rigsignal.frame-*` | metrics | FPS, frame time percentiles, stutter count |
| `metrics-rigsignal.memory-*` | metrics | RAM usage, swap, process RSS |
| `metrics-rigsignal.storage-*` | metrics | Disk I/O, latency |
| `metrics-rigsignal.network-*` | metrics | Bytes/packets in/out |
| `metrics-rigsignal.audio-*` | metrics | Latency, buffer size, xruns |
| `metrics-rigsignal.power-*` | metrics | Battery, AC state, TDP |
| `metrics-rigsignal.ebpf-*` | metrics | Scheduler migrations, GPU fence latency, futex wait |
| `metrics-rigsignal.ebpf_thread-*` | metrics | Per-thread runqueue latency, switches, and migrations |
| `metrics-rigsignal.session-*` | metrics | Per-session aggregates, game metadata |
| `logs-rigsignal.events-*` | logs | Game start/end, settings changes |

## Dashboards

Five dashboards are included:

- **Player Overview** — session history, top games by FPS and playtime
- **Game Performance** — FPS trends, frame timing, stutter analysis
- **Game Engine** — eBPF kernel traces, shader compile detection
- **Hardware Environment** — thermal and power headroom
- **Software Environment** — driver versions, OS context, audio health

## Steam Deck

RigSignal supports the Steam Deck. Install in Desktop Mode:

```bash
curl -sSfL https://mathewrj.github.io/RigSignal-Integration/install.sh | sh
rigsignal setup
```

Installs to `~/.local/bin/` — **survives SteamOS updates** with no reinstall needed.

**eBPF caveat:** the eBPF daemon requires root/`CAP_BPF` and installs to `/usr/`, which
SteamOS resets on OS updates. Reinstall via `yay -S rigsignal-git` after a system update
to restore eBPF streams. All other data streams (CPU, GPU, frame timing, memory, etc.)
are unaffected and continue working without eBPF.

## Licence

Apache 2.0 — see [LICENSE](LICENSE).
