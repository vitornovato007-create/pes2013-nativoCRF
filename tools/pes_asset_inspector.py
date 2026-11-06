#!/usr/bin/env python3
"""Read-only inspector for PES/CRI AFS .img and Sofdec .sfd files.

It reads archive indexes and bounded samples only. It never extracts,
modifies, executes, or uploads game assets.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any

AFS_MAGIC = b"AFS\x00"
SFD_MARKERS = (b"SofdecStream2", b"@CRITAGS", b"SFVFTRS", b"SFV:DCD", b"SFV:ECD")
MARKERS = (
    (b"WESYS", "WESYS marker"),
    (b"CPK ", "CRI CPK"),
    (b"RIFF", "RIFF container"),
    (b"OggS", "Ogg stream"),
    (b"\x89PNG\\r\\n\x1a\\n", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
)


class AuditError(Exception):
    pass


def read_at(handle, offset: int, size: int) -> bytes:
    handle.seek(offset)
    return handle.read(size)


def inspect_afs(path: Path, sample_bytes: int = 32) -> dict[str, Any]:
    file_size = path.stat().st_size
    with path.open("rb") as handle:
        header = read_at(handle, 0, 8)
        if len(header) != 8 or header[:4] != AFS_MAGIC:
            raise AuditError("AFS signature not found")
        count = struct.unpack_from("<I", header, 4)[0]
        if count > 1_000_000:
            raise AuditError(f"Implausible AFS entry count: {count}")
        index_end = 8 + count * 8
        if index_end > file_size:
            raise AuditError("AFS index extends beyond end of file")

        entries = []
        ranges = []
        invalid = []
        empty = 0
        marker_entry_count = 0

        for index in range(count):
            raw = read_at(handle, 8 + index * 8, 8)
            offset, size = struct.unpack("<II", raw)
            item: dict[str, Any] = {"index": index, "offset": offset, "size": size}
            if size == 0:
                empty += 1
                item["empty"] = True
            else:
                end = offset + size
                if offset < index_end:
                    invalid.append(f"entry {index}: data starts inside index")
                if end > file_size or end < offset:
                    invalid.append(f"entry {index}: range exceeds file")
                else:
                    ranges.append((offset, end, index))
                    sample = read_at(handle, offset, min(sample_bytes, size))
                    item["sample_hex"] = sample.hex(" ")
                    item["sample_ascii"] = "".join(
                        chr(b) if 32 <= b < 127 else "." for b in sample
                    )
                    item["markers"] = [label for marker, label in MARKERS if marker in sample]
                    if b"WESYS" in sample:
                        marker_entry_count += 1
            entries.append(item)

        sorted_ranges = sorted(ranges)
        overlaps = []
        previous = None
        for current in sorted_ranges:
            if previous is not None and current[0] < previous[1]:
                overlaps.append([previous[2], current[2]])
            if previous is None or current[1] > previous[1]:
                previous = current

    return {
        "file": path.name,
        "path": str(path),
        "format": "AFS",
        "size_bytes": file_size,
        "entry_count": count,
        "empty_entries": empty,
        "nonempty_entries": len(ranges),
        "index_end": index_end,
        "entries_aligned_to_2048": sum(1 for start, _, _ in ranges if start % 2048 == 0),
        "overlaps": overlaps,
        "invalid_entries": invalid,
        "entries_with_WESYS_sample_marker": marker_entry_count,
        "integrity": "valid" if not invalid and not overlaps else "check_required",
        "entries": entries,
    }


def scan_markers(path: Path, markers: tuple[bytes, ...], limit: int) -> dict[str, int]:
    found = {m.decode("ascii", "replace"): 0 for m in markers}
    max_bytes = min(path.stat().st_size, limit)
    carry = b""
    scanned = 0
    max_marker = max((len(m) for m in markers), default=1)
    with path.open("rb") as handle:
        while scanned < max_bytes:
            chunk = handle.read(min(1024 * 1024, max_bytes - scanned))
            if not chunk:
                break
            data = carry + chunk
            for marker in markers:
                found[marker.decode("ascii", "replace")] += data.count(marker)
            scanned += len(chunk)
            carry = data[-(max_marker - 1):] if max_marker > 1 else b""
    return {key: value for key, value in found.items() if value}


def inspect_sfd(path: Path) -> dict[str, Any]:
    size = path.stat().st_size
    with path.open("rb") as handle:
        header = read_at(handle, 0, min(64, size))
    mpeg_ps = header.startswith(b"\x00\x00\x01\xba")
    markers = scan_markers(path, SFD_MARKERS, 8 * 1024 * 1024)
    return {
        "file": path.name,
        "path": str(path),
        "format": "SFD candidate" if mpeg_ps or markers else "unknown",
        "size_bytes": size,
        "mpeg_program_stream_pack_header": mpeg_ps,
        "markers_in_first_8_mib": markers,
        "header_hex": header[:32].hex(" "),
        "note": "Markers are indicators only; exact video/audio codecs are not decoded.",
    }


def inspect_file(path: Path, sample_bytes: int) -> dict[str, Any]:
    if path.suffix.lower() == ".img":
        return inspect_afs(path, sample_bytes)
    if path.suffix.lower() == ".sfd":
        return inspect_sfd(path)
    raise AuditError(f"Unsupported file extension: {path.suffix}")


def collect_files(inputs: list[Path]) -> list[Path]:
    found = []
    for item in inputs:
        if item.is_file() and item.suffix.lower() in {".img", ".sfd"}:
            found.append(item)
        elif item.is_dir():
            found.extend(
                p for p in item.rglob("*")
                if p.is_file() and p.suffix.lower() in {".img", ".sfd"}
            )
        else:
            raise AuditError(f"Input not found or unsupported: {item}")
    return sorted(set(found))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only inspection of AFS IMG archives and CRI SFD files."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--sample-bytes", type=int, default=32)
    args = parser.parse_args(argv)
    if not 8 <= args.sample_bytes <= 256:
        parser.error("--sample-bytes must be between 8 and 256")

    try:
        files = collect_files(args.paths)
        if not files:
            raise AuditError("No .img or .sfd files found")
        results = []
        for path in files:
            try:
                results.append(inspect_file(path, args.sample_bytes))
            except (OSError, AuditError, struct.error) as exc:
                results.append({"file": path.name, "path": str(path), "error": str(exc)})
        report = {
            "tool": "PES Asset Inspector",
            "version": "0.1.0",
            "read_only": True,
            "files_analyzed": len(results),
            "results": results,
        }
        output = json.dumps(report, indent=2, ensure_ascii=False)
        print(output)
        if args.json_path:
            args.json_path.parent.mkdir(parents=True, exist_ok=True)
            args.json_path.write_text(output + "\\n", encoding="utf-8")
        return 1 if any("error" in item for item in results) else 0
    except (OSError, AuditError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
