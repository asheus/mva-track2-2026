"""Minimal seekable read-only file over HTTP Range requests, proxy-aware.

fsspec+aiohttp choked on Hugging Face's Xet redirect; urllib honours HTTPS_PROXY
and follows the 302 to the signed CDN URL, so we resolve once and range-read that.
"""
import io, urllib.request


class HttpFile(io.RawIOBase):
    def __init__(self, url, chunk=1 << 20):
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=120) as r:
            self.url = r.geturl()                      # resolved, signed URL
            self.size = int(r.headers["Content-Length"])
        self._pos = 0

    def _get(self, start, end):
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{end}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self._pos

    def seek(self, off, whence=0):
        self._pos = off if whence == 0 else (self._pos + off if whence == 1 else self.size + off)
        return self._pos

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self._pos
        if n == 0 or self._pos >= self.size:
            return b""
        end = min(self._pos + n, self.size) - 1
        data = self._get(self._pos, end)
        self._pos += len(data)
        return data

    def readinto(self, b):
        d = self.read(len(b))
        b[:len(d)] = d
        return len(d)
