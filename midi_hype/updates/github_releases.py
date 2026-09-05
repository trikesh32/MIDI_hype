from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass


GITHUB_OWNER = "trikesh32"
GITHUB_REPO = "MIDI_hype"


@dataclass(frozen=True)
class ReleaseInfo:
    version: str
    name: str
    notes: str
    url: str


class GitHubReleaseClient:
    def __init__(self, owner: str = GITHUB_OWNER, repo: str = GITHUB_REPO) -> None:
        self.owner = owner
        self.repo = repo

    def fetch_latest_release(self) -> ReleaseInfo:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/latest"
        request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "MIDI-Hype"})
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
        tag = str(payload.get("tag_name", "0.0.0")).lstrip("v")
        return ReleaseInfo(
            version=tag,
            name=str(payload.get("name", tag)),
            notes=str(payload.get("body", "")),
            url=str(payload.get("html_url", "https://github.com")),
        )


def _version_tuple(version: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", version)
    return tuple(int(part) for part in parts[:3]) or (0,)


def is_newer_version(candidate: str, current: str) -> bool:
    return _version_tuple(candidate) > _version_tuple(current)

