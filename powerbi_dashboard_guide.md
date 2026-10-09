# Power BI Dashboard Guide

## Recommended report pages

### 1. Executive Overview
- KPI cards: demand stops, fleet size, optimized distance, baseline distance, distance reduction, total route hours.
- Clustered bar chart: nearest-neighbor baseline km vs optimized km by scenario.
- Line chart: distance reduction (%) by demand stops, with fleet size as a legend or slicer.
- Slicers: `scenario_id`, `demand_stops`, `fleet_size`, `solver`.

### 2. Fleet & Route Performance
- Matrix by vehicle: stop count, package count, distance, route duration, shift utilization.
- Scatter plot: route distance (x) versus route duration (y), bubble size = stops.
- Bar chart: route duration by vehicle.
- KPI: active fleet utilization (%) = vehicles assigned at least one stop / vehicles scheduled.

**Metric note:** `active_fleet_utilization_pct` is the share of scheduled vehicles assigned a non-empty route. It is distinct from `average_shift_utilization_pct`, which measures route-hours against scheduled shift-hours. The model requires all scenario vehicles to be dispatched, so the active-fleet metric is expected to be 100%; use shift utilization to compare workload intensity.

### 3. Route Stop Explorer
- Table: scenario, vehicle, sequence, stop ID, zone, priority, package count.
- Scatter plot: use `x_km` and `y_km` to visualize the synthetic route plane, colored by vehicle or zone. These are Cartesian coordinates, not real latitude/longitude; do not place them on a geographic map without converting to real coordinates.
- Filters: scenario, vehicle, zone, priority.

### 4. Scenario Analysis
- Heatmap: rows = `demand_stops`; columns = `fleet_size`; values = distance reduction or total route hours.
- Compare optimized distance, route duration, and shift utilization when demand or fleet size changes.
- Flag scenarios with a distance reduction below the team's chosen threshold; do not hard-code an improvement claim without checking the generated CSV.

## Data model

Import these CSV files from `data/output/`:
- `scenario_summary.csv` — one row per demand/fleet scenario.
- `optimized_routes.csv` — one row per vehicle route per scenario.
- `optimized_stop_assignments.csv` — stop sequence and vehicle assignment.
- `vehicle_utilization.csv` — route-level utilization measures.
- `nearest_neighbor_baseline_routes.csv` — route-level baseline metrics.
- `zone_summary.csv` — zone aggregation for the showcase scenario.

Recommended relationships: `scenario_summary[scenario_id]` 1-to-many `optimized_routes[scenario_id]`, `optimized_routes[scenario_id, vehicle_id]` 1-to-many `optimized_stop_assignments[scenario_id, vehicle_id]`, and similarly connect the baseline table by scenario and vehicle when comparing route-level records. Avoid joining route detail directly to zone aggregates if it multiplies rows.
