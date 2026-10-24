"""Submit and poll Neurosnap jobs.

The API key is read from NEUROSNAP_API_KEY and is never printed, logged, or
written to disk -- only its presence is reported.
"""
import os, sys, time, json, pathlib, requests

BASE = "https://neurosnap.ai/api"


def key():
    k = os.environ.get("NEUROSNAP_API_KEY")
    if not k:
        sys.exit("NEUROSNAP_API_KEY is not set in this process's environment.")
    return k


def submit(service: str, fields: dict, note: str = "") -> str:
    """fields: name -> str, or (filename, bytes) for file inputs."""
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    enc = MultipartEncoder(fields={
        n: (v if isinstance(v, str) else (v[0], v[1], "application/octet-stream"))
        for n, v in fields.items()
    })
    r = requests.post(
        f"{BASE}/job/submit/{service}",
        params={"note": note} if note else None,
        headers={"X-API-KEY": key(), "Content-Type": enc.content_type},
        data=enc, timeout=300,
    )
    r.raise_for_status()
    return r.json()


def status(job_id: str):
    r = requests.get(f"{BASE}/job/status/{job_id}",
                     headers={"X-API-KEY": key()}, timeout=60)
    r.raise_for_status()
    return r.json()


def wait(job_id: str, every=30, limit=7200):
    t0 = time.time()
    while time.time() - t0 < limit:
        s = status(job_id)
        print(f"[{int(time.time()-t0):5d}s] {s}", flush=True)
        if isinstance(s, str) and s.lower() in ("completed", "failed"):
            return s
        if isinstance(s, dict) and str(s.get("status", "")).lower() in ("completed", "failed"):
            return s
        time.sleep(every)
    raise TimeoutError(job_id)


if __name__ == "__main__":
    # Smoke test: does the host answer at all, and is the key accepted?
    try:
        r = requests.get(f"{BASE}/services", headers={"X-API-KEY": key()}, timeout=60)
        print("HTTP", r.status_code)
        print(r.text[:2000])
    except Exception as e:
        print("FAILED:", type(e).__name__, e)
