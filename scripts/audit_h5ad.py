#!/usr/bin/env python3
"""Lightweight H5AD structure and categorical-label audit using h5py."""

import argparse
from collections import Counter
from pathlib import Path

import h5py


def decode(value):
    return value.decode() if isinstance(value, bytes) else str(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("h5ad", type=Path)
    parser.add_argument("--labels", nargs="*", default=["ct", "celltype", "sample"])
    args = parser.parse_args()

    with h5py.File(args.h5ad, "r") as handle:
        n_obs = len(handle["obs"]["_index"])
        n_var = len(handle["var"]["_index"])
        print(f"file\t{args.h5ad}")
        print(f"shape\t{n_obs}\t{n_var}")
        print(f"obs_fields\t{','.join(handle['obs'].keys())}")
        if "obsm" in handle:
            print(f"obsm_fields\t{','.join(handle['obsm'].keys())}")

        for field in args.labels:
            if field not in handle["obs"]:
                continue
            obj = handle["obs"][field]
            if not isinstance(obj, h5py.Group) or not {"codes", "categories"} <= set(obj.keys()):
                print(f"label\t{field}\tnon-categorical")
                continue
            categories = [decode(v) for v in obj["categories"][:]]
            counts = Counter(categories[i] for i in obj["codes"][:] if i >= 0)
            for category in categories:
                print(f"label\t{field}\t{category}\t{counts[category]}")


if __name__ == "__main__":
    main()
