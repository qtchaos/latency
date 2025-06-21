# latency.py

Tiny server that allows browsers to measure real latency.

## Why?

There is no good way to measure time to first byte (TTFB) in browsers, the only exception being the `Performance` API which allows you to view resource timings, the caveat being that you need a server that returns the `Timing-Allow-Origin` header, which this server does.

## Usage

Start the server either with the Docker image or by simply running the file:

```bash
uv run latency.py
```

Then use the following JavaScript code (also in `/examples`) to measure latency. Before starting your measurements there should be a warmup request to ensure proper results (even though TTFB shouldn't include the time it takes to establish the first connection, it is still a good precaution) and please for gods sake use a median of the results if you are measuring more than once and want an accurate representation of the latency.

```javascript
async function measureLatency() {
    return new Promise((resolve) => {
        const url = `http://localhost:8000/?t=${Date.now()}`;
        const img = new Image();
        img.src = url;
        img.onload = () => {
            const entry = performance
                .getEntriesByType("resource")
                .find((e) => e.name === url);

            const latency = entry.responseStart - entry.requestStart;
            resolve(latency);
        };
    });
}
```
