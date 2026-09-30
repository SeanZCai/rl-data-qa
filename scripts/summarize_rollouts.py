#!/usr/bin/env python3
"""Validate normalized rollout verdicts and compute conditional unbiased pass@k."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import sys


class InvalidRecords(ValueError):
    pass


def pass_at_k(n: int, c: int, k: int) -> float:
    if any(type(value) is not int for value in (n, c, k)):
        raise ValueError("n, c, and k must be integers")
    if not 0 <= c <= n or not 1 <= k <= n:
        raise ValueError("require 0 <= c <= n and 1 <= k <= n")
    if n - c < k:
        return 1.0
    if c == 0:
        return 0.0
    # Sum log miss-probabilities; expm1 preserves precision for rare successes.
    return -math.expm1(sum(math.log1p(-c / (n - i)) for i in range(k)))


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise InvalidRecords(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def invalid_constant(value):
    raise InvalidRecords(f"nonstandard JSON constant: {value}")


def read_records(path: Path):
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line, object_pairs_hook=unique_object,
                                    parse_constant=invalid_constant)
            except ValueError as exc:
                raise InvalidRecords(f"line {line_number}: {exc}") from exc
            yield line_number, record


def summarize(records, ks=(1, 5), min_samples=16):
    if not ks or any(type(k) is not int or k < 1 for k in ks):
        raise ValueError("k values must be positive integers")
    if type(min_samples) is not int or min_samples < 1:
        raise ValueError("min_samples must be a positive integer")
    ks = sorted(set(ks))
    groups = defaultdict(Counter)
    seen = set()
    for line, record in records:
        if not isinstance(record, dict):
            raise InvalidRecords(f"line {line}: expected an object")
        for field in ("task_id", "model", "condition", "sample_id"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                raise InvalidRecords(f"line {line}: {field} must be a nonempty string")
        if type(record.get("seed")) is not int:
            raise InvalidRecords(f"line {line}: seed must be an integer")
        status = record.get("status")
        if not isinstance(status, str) or status not in {"pass", "fail", "environment_failure"}:
            raise InvalidRecords(f"line {line}: unknown or missing status")
        key = tuple(record[field] for field in ("task_id", "model", "condition", "seed"))
        identity = (*key, record["sample_id"])
        if identity in seen:
            raise InvalidRecords(f"line {line}: duplicate rollout identity {identity}")
        seen.add(identity)
        groups[key][status] += 1
    if not groups:
        raise InvalidRecords("no rollout records")

    output, warnings = [], []
    for key, counts in sorted(groups.items()):
        n = counts["pass"] + counts["fail"]
        c = counts["pass"]
        env = counts["environment_failure"]
        attempts = n + env
        cell = dict(zip(("task_id", "model", "condition", "seed"), key))
        estimates = {str(k): pass_at_k(n, c, k) if n >= k else None for k in ks}
        output.append({**cell, "attempts": attempts, "n": n, "c": c,
                       "environment_failures": env, "environment_failure_rate": env / attempts,
                       "success_per_attempt": c / attempts,
                       "conditional_pass_at_k": estimates})
        if n < min_samples:
            warnings.append({**cell, "code": "low_sample_count", "n": n,
                             "minimum": min_samples})
        if any(n < k for k in ks):
            warnings.append({**cell, "code": "unsupported_k", "values": [k for k in ks if n < k]})
        if env:
            warnings.append({**cell, "code": "environment_failures_present", "count": env})

    tasks = sorted({key[0] for key in groups})
    configurations = sorted({key[1:] for key in groups})
    missing = [dict(zip(("task_id", "model", "condition", "seed"), (task, *config)))
               for task in tasks for config in configurations if (task, *config) not in groups]
    if missing:
        warnings.append({"code": "incomplete_observed_grid", "count": len(missing)})
    attempts = len(seen)
    failures = sum(cell["environment_failures"] for cell in output)
    return {"schema_version": 1, "assessment": "metrics_only", "groups": output,
            "attempts": attempts, "environment_failures": failures,
            "environment_failure_rate": failures / attempts,
            "missing_observed_cells": missing, "warnings": warnings,
            "uncertainty": "not_computed", "release_readiness": "not_assessed"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="Normalized JSONL verdict records")
    parser.add_argument("--k", nargs="+", type=int, default=[1, 5])
    parser.add_argument("--min-samples", type=int, default=16)
    args = parser.parse_args(argv)
    try:
        result = summarize(read_records(args.records), args.k, args.min_samples)
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
