# RigSignal

Real-time gaming telemetry for Elasticsearch. Captures FPS, frame timing percentiles, GPU/CPU thermals, memory, storage, network, audio, power draw, and kernel-level scheduler/I/O/GPU traces via eBPF — streamed live while you play.

## Requirements

- Elasticsearch 8.13+ or Elastic Cloud Serverless
- [rigsignal-agent](https://github.com/MathewRJ/RigSignal/releases) installed on the gaming machine
- An API key with `create_doc` + `auto_configure` on `metrics-rigsignal.*` and `logs-rigsignal.*`

## Setup

1. Install this integration via Fleet
2. Install the rigsignal-agent binary on your gaming machine
3. Configure `/etc/rigsignal/rigsignal.toml` with your Elasticsearch URL and API key
4. Start the agent: `systemctl --user start rigsignal-agent`

## Data streams

| Stream | Content |
|---|---|
| `metrics-rigsignal.cpu` | CPU utilisation, temperature, frequency per core |
| `metrics-rigsignal.gpu` | GPU utilisation, VRAM, temperature, power draw |
| `metrics-rigsignal.frame` | FPS, frame time percentiles (p50/p95/p99), stutter count |
| `metrics-rigsignal.memory` | RAM, swap, process RSS |
| `metrics-rigsignal.storage` | Disk I/O bytes and latency |
| `metrics-rigsignal.network` | Bytes and packets in/out |
| `metrics-rigsignal.audio` | Latency, buffer size, xrun count |
| `metrics-rigsignal.power` | Battery %, charge rate, AC state, TDP |
| `metrics-rigsignal.ebpf` | Kernel scheduler migrations, GPU fence latency, futex waits |
| `metrics-rigsignal.ebpf_thread` | Per-thread runqueue latency, switches, and migrations |
| `metrics-rigsignal.session` | Per-session aggregates, game metadata, settings |
| `logs-rigsignal.events` | Game start/end events, settings changes |

## Dashboards

- **Player Overview** — session history and top games
- **Game Performance** — FPS trends, frame timing, stutter analysis
- **Game Engine** — eBPF kernel traces, shader compile detection
- **Hardware Environment** — thermal and power headroom
- **Software Environment** — driver versions, OS context, audio health
