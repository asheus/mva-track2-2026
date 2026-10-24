import subprocess, io, os

class CurlRangeFile(io.RawIOBase):
    """Minimal seekable read-only file over an HTTP range endpoint, via curl.

    Uses curl rather than requests/fsspec because Hugging Face's Xet CDN issues a
    signed redirect whose signature is invalidated if the URL is re-encoded, which
    both requests and fsspec do.
    """
    def __init__(self, url, size=None):
        self.url, self._pos = url, 0
        self.size = size if size is not None else self._probe()
        self.bytes_read = 0
        self.n_requests = 0

    def _curl(self, rng):
        p = subprocess.run(["curl", "-sL", "--max-time", "120", "-r", rng, self.url],
                           capture_output=True)
        if p.returncode: raise IOError(f"curl {p.returncode}: {p.stderr[:200]}")
        return p.stdout

    def _probe(self):
        p = subprocess.run(["curl","-sL","-o","/dev/null","-D","-","-r","0-0",self.url],
                           capture_output=True, text=True)
        for ln in p.stdout.splitlines():
            if ln.lower().startswith("content-range"):
                return int(ln.split("/")[-1].strip())
        raise IOError("no content-range")

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self._pos
    def seek(self, off, whence=0):
        self._pos = off if whence==0 else self._pos+off if whence==1 else self.size+off
        return self._pos
    def read(self, n=-1):
        if n is None or n < 0: n = self.size - self._pos
        if n == 0 or self._pos >= self.size: return b""
        end = min(self._pos + n, self.size) - 1
        data = self._curl(f"{self._pos}-{end}")
        self._pos += len(data); self.bytes_read += len(data); self.n_requests += 1
        return data
    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d; return len(d)
