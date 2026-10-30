#!/usr/bin/env python3
"""Compile reviewed camera-time cuts into a synchronized frame edit plan.

Input JSON (seconds are finite JSON numbers):
  {
    "fps": "30000/1001",
    "source_duration_seconds": 120.0,
    "source_start_seconds": 0.0,
    "source_end_seconds": 120.0,
    "sync": {"screen_offset_seconds": 0.0},
    "screen_duration_seconds": 120.0,
    "cuts": [{"start": 5.0, "end": 6.0, "reason": "Reviewed restart",
              "evidence": "private/project-local/evidence.json"}],
    "camera_source": "Footages/camera.mp4",
    "screen_source": "Footages/screen.mov"
  }

Required: fps, source_duration_seconds, cuts. Start defaults to zero; end
defaults to source duration; sync offset defaults to zero. Screen duration
and source paths are optional metadata. Screen time = camera time + offset.
Cuts must be inside the selected source range. A selected range mapping
outside the screen is rejected; adjust its start/end explicitly. Other
metadata is preserved. No editorial judgments or media operations occur.

Each retained interval is rounded inward: ceil(start * fps), floor(end * fps).
Frame bounds are half-open [start_frame, end_frame), with camera source frame
zero as origin. Derived second values are display conveniences; use integer
frames and the rational fps for rendering. No source or existing output is
overwritten unless --force is given for a distinct existing output.
"""

import argparse
import json
import math
import os
from pathlib import Path
from fractions import Fraction
import tempfile


def _reject_constant(value):
    raise ValueError("JSON contains non-finite value: " + value)


def _validate_json_numbers(value, path="input"):
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if isinstance(value, (int, float)):
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError(path + " must contain only finite numbers")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_numbers(item, "{}[{}]".format(path, index))
    elif isinstance(value, dict):
        for key, item in value.items():
            _validate_json_numbers(item, path + "." + key)


def _seconds(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a finite JSON number")
    _validate_json_numbers(value, name)
    return Fraction(str(value))


def _fps(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("fps must be a positive rational string or number")
    try:
        result = Fraction(str(value))
        valid = result > 0 and math.isfinite(float(result))
    except (ValueError, ZeroDivisionError, OverflowError):
        valid = False
    if not valid:
        raise ValueError("fps must be a positive finite rational string or number")
    return result


def _ceil(value):
    return -(-value.numerator // value.denominator)


def compile_plan(payload):
    """Return a new plan; never mutate payload or read/write media/files."""
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    _validate_json_numbers(payload)
    for required in ("fps", "source_duration_seconds", "cuts"):
        if required not in payload:
            raise ValueError("missing required field: " + required)
    fps = _fps(payload["fps"])
    duration = _seconds(payload["source_duration_seconds"], "source_duration_seconds")
    start = _seconds(payload.get("source_start_seconds", 0), "source_start_seconds")
    end = _seconds(payload.get("source_end_seconds", payload["source_duration_seconds"]),
                   "source_end_seconds")
    if duration <= 0:
        raise ValueError("source_duration_seconds must be positive")
    if not 0 <= start < end <= duration:
        raise ValueError("require 0 <= source_start_seconds < source_end_seconds "
                         "<= source_duration_seconds")

    sync = payload.get("sync", {})
    if not isinstance(sync, dict):
        raise ValueError("sync must be a JSON object")
    offset = _seconds(sync.get("screen_offset_seconds", 0), "sync.screen_offset_seconds")
    if start + offset < 0:
        raise ValueError("selected source range maps before screen time zero; "
                         "increase source_start_seconds to at least {:.12g}".format(float(-offset)))
    if "screen_duration_seconds" in payload:
        screen_duration = _seconds(payload["screen_duration_seconds"], "screen_duration_seconds")
        if screen_duration <= 0:
            raise ValueError("screen_duration_seconds must be positive")
        if end + offset > screen_duration:
            raise ValueError("selected source range exceeds screen duration; "
                             "decrease source_end_seconds to at most {:.12g}".format(
                                 float(screen_duration - offset)))

    if not isinstance(payload["cuts"], list):
        raise ValueError("cuts must be a list of already reviewed intervals")
    reviewed = []
    for index, cut in enumerate(payload["cuts"]):
        name = "cuts[{}]".format(index)
        if not isinstance(cut, dict):
            raise ValueError(name + " must be a JSON object")
        for required in ("start", "end", "reason"):
            if required not in cut:
                raise ValueError(name + " missing " + required)
        cut_start = _seconds(cut["start"], name + ".start")
        cut_end = _seconds(cut["end"], name + ".end")
        if not start <= cut_start < cut_end <= end:
            raise ValueError(name + " must satisfy selected start <= cut start < "
                             "cut end <= selected end")
        if not isinstance(cut["reason"], str) or not cut["reason"].strip():
            raise ValueError(name + ".reason must be a nonempty string")
        reviewed.append((cut_start, cut_end, dict(cut)))
    reviewed.sort(key=lambda item: (item[0], item[1]))
    cursor = start
    retained = []
    for cut_start, cut_end, cut in reviewed:
        if cut_start < cursor:
            raise ValueError("reviewed cuts overlap; resolve the editorial ranges first")
        if cut_start > cursor:
            retained.append((cursor, cut_start))
        cursor = cut_end
    if cursor < end:
        retained.append((cursor, end))

    segments = []
    total_frames = 0
    for interval_start, interval_end in retained:
        start_frame = _ceil(interval_start * fps)
        end_frame_fraction = interval_end * fps
        end_frame = end_frame_fraction.numerator // end_frame_fraction.denominator
        frame_count = end_frame - start_frame
        if frame_count <= 0:
            continue
        segments.append({
            "start_frame": start_frame,
            "end_frame": end_frame,
            "output_start_frame": total_frames,
            "frame_count": frame_count,
            "start_seconds": float(Fraction(start_frame, 1) / fps),
            "end_seconds": float(Fraction(end_frame, 1) / fps),
            "output_start_seconds": float(Fraction(total_frames, 1) / fps),
            "duration_seconds": float(Fraction(frame_count, 1) / fps),
        })
        total_frames += frame_count
    if not total_frames:
        raise ValueError("no complete retained frames remain after cuts and inward rounding")

    plan = dict(payload)
    plan.update({
        "plan_schema_version": 1,
        "timebase": "camera_source_seconds",
        "fps": "{}/{}".format(fps.numerator, fps.denominator),
        "fps_numerator": fps.numerator,
        "fps_denominator": fps.denominator,
        "source_start_seconds": float(start),
        "source_end_seconds": float(end),
        "sync": dict(sync, screen_offset_seconds=float(offset)),
        "cuts": [cut for _, _, cut in reviewed],
        "rounding": "retained intervals inward: ceil start frame, floor end frame",
        "segments": segments,
        "total_frames": total_frames,
        "duration_seconds": float(Fraction(total_frames, 1) / fps),
    })
    return plan


def _write_plan(path, plan, force):
    content = json.dumps(plan, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not force:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
        return
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(path.parent),
                                         prefix="." + path.name + ".", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        os.replace(str(temporary), str(path))
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, required=True, help="Reviewed cut JSON; never modified")
    parser.add_argument("--output", type=Path, required=True, help="Compiled frame-plan JSON")
    parser.add_argument("--force", action="store_true", help="Replace an existing output, never the input")
    args = parser.parse_args(argv)
    try:
        same_path = args.input.resolve() == args.output.resolve()
        if not same_path and args.input.exists() and args.output.exists():
            same_path = os.path.samefile(str(args.input), str(args.output))
        if same_path:
            raise ValueError("input and output must be distinct files, even with --force")
        if args.output.exists() and not args.force:
            raise ValueError("output already exists; choose a new path or pass --force")
        with args.input.open(encoding="utf-8") as handle:
            payload = json.load(handle, parse_constant=_reject_constant)
        plan = compile_plan(payload)
        _write_plan(args.output, plan, args.force)
    except (ValueError, OSError) as error:
        parser.exit(2, "error: {}\n".format(error))
    print("Compiled {} segments, {} frames, {:.6f} seconds -> {}".format(
        len(plan["segments"]), plan["total_frames"], plan["duration_seconds"], args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
