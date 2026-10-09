"""Generate reproducible synthetic last-mile delivery data for the demo project."""
from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "input"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate(seed: int = 2026) -> None:
    rng = random.Random(seed)
    centers = [(5, 7), (7, 31), (30, 6), (32, 30), (19, 20)]
    zone_names = ["Northwest", "Northeast", "Southwest", "Southeast", "Central"]
    stops: list[dict] = []

    # Create 260 candidate delivery stops across five synthetic delivery zones.
    for i in range(1, 261):
        zone_idx = (i - 1) % len(centers)
        cx, cy = centers[zone_idx]
        x = min(39.0, max(1.0, rng.gauss(cx, 3.3)))
        y = min(39.0, max(1.0, rng.gauss(cy, 3.3)))
        stops.append({
            "stop_id": f"S{i:03d}",
            "zone": zone_names[zone_idx],
            "x_km": round(x, 3),
            "y_km": round(y, 3),
            "packages": rng.randint(1, 4),
            "service_minutes": rng.choice([4, 5, 5, 6, 7]),
            "priority": rng.choice(["Standard", "Standard", "Standard", "Priority"]),
        })
    rng.shuffle(stops)
    write_csv(INPUT / "delivery_stops.csv", stops,
              ["stop_id", "zone", "x_km", "y_km", "packages", "service_minutes", "priority"])

    write_csv(INPUT / "depot.csv", [{"depot_id": "DEPOT-01", "x_km": 20.0, "y_km": 20.0}],
              ["depot_id", "x_km", "y_km"])

    demands = [160, 180, 200, 220, 240]
    fleets = [5, 6, 7, 8, 9]
    scenarios = []
    for demand in demands:
        for fleet in fleets:
            scenarios.append({
                "scenario_id": f"D{demand}_V{fleet}",
                "demand_stops": demand,
                "fleet_size": fleet,
                "vehicle_capacity_stops": 60,
                "shift_limit_minutes": 600,
                "avg_speed_kmh": 30,
                "distance_factor": 1.22,
            })
    write_csv(INPUT / "scenario_grid.csv", scenarios,
              ["scenario_id", "demand_stops", "fleet_size", "vehicle_capacity_stops",
               "shift_limit_minutes", "avg_speed_kmh", "distance_factor"])

    fleet_rows = [{
        "vehicle_id": f"V{i:02d}", "vehicle_type": "Van", "max_stops_per_shift": 60,
        "shift_limit_minutes": 600, "nominal_capacity_packages": 100,
    } for i in range(1, 10)]
    write_csv(INPUT / "fleet_specifications.csv", fleet_rows,
              ["vehicle_id", "vehicle_type", "max_stops_per_shift", "shift_limit_minutes", "nominal_capacity_packages"])


if __name__ == "__main__":
    generate()
    print(f"Synthetic input files written to {INPUT}")
