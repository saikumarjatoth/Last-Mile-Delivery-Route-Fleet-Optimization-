# Last-Mile Delivery Route & Fleet Optimization

A reproducible, portfolio-ready operations research project that optimizes synthetic last-mile delivery routes for a city delivery network. It compares a nearest-neighbor baseline with a multi-vehicle routing solution, evaluates 25 demand/fleet scenarios, and exports Power BI-ready route and fleet tables.

> **Data note:** This is a synthetic demonstration project. All locations, package counts, scenarios, distances, and performance results are generated for portfolio use and are not claims about a real logistics operation.

## Project highlights

- Routes **160–240 delivery stops** across 25 demand/fleet combinations (5 demand levels × 5 fleet sizes).
- Uses **Google OR-Tools Routing Solver** with distance minimization, stop-capacity constraints, route-duration limits, and Guided Local Search.
- Benchmarks optimized routes against a transparent nearest-neighbor baseline.
- Reports distance reduction, route duration, vehicle workload, active-fleet utilization, and shift utilization.
- Exports route-stop assignments and scenario summaries that can be imported directly into Power BI.

## Repository structure

```text
last-mile-delivery-optimization/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── src/
│   ├── generate_data.py
│   ├── optimize_routes.py
│   └── run_project.py
├── data/
│   ├── input/
│   │   ├── delivery_stops.csv
│   │   ├── depot.csv
│   │   ├── fleet_specifications.csv
│   │   └── scenario_grid.csv
│   └── output/
│       ├── scenario_summary.csv
│       ├── optimized_routes.csv
│       ├── optimized_stop_assignments.csv
│       ├── nearest_neighbor_baseline_routes.csv
│       ├── vehicle_utilization.csv
│       └── zone_summary.csv
├── notebooks/
│   └── last_mile_route_optimization.ipynb
├── docs/
│   └── powerbi_dashboard_guide.md
└── tests/
    └── test_model.py
```

## Business problem

Last-mile delivery teams need to sequence customer stops and allocate a limited vehicle fleet while balancing distance, delivery workload, and shift limits. A simple nearest-neighbor route can make locally attractive choices that lead to inefficient vehicle tours. This project compares that baseline with a vehicle-routing optimization model and then tests how results change under different demand and fleet sizes.

## Methodology

1. **Generate synthetic data.** Create 260 candidate stops distributed across five delivery zones, one central depot, package counts, and service-time estimates.
2. **Build a baseline.** Construct a nearest-neighbor tour and split it into a balanced set of vehicle routes.
3. **Optimize routes.** OR-Tools minimizes total travel distance with per-vehicle stop-capacity and shift-duration constraints. The configured scenario fleet is dispatched with a non-empty route for each vehicle to make fleet activation comparable across scenarios.
4. **Test robustness.** Evaluate 25 combinations of 160/180/200/220/240 stops and fleets of 5/6/7/8/9 vehicles.
5. **Export analytics.** Save per-scenario performance, routes, stop assignments, baseline comparisons, and vehicle utilization metrics as CSV files.

When OR-Tools is installed, the primary solver is **Path Cheapest Arc + Guided Local Search**. A dependency-light angular-sweep + 2-opt fallback is included so the repository can still generate sample output tables in environments where OR-Tools has not been installed. Install `requirements.txt` to use the primary OR-Tools implementation.

## Run the project

Use Python 3.10 or newer.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Regenerate synthetic input files and all output CSVs
python src/run_project.py

# 3. Run tests
python -m unittest discover -s tests -v
```

The output tables are written to `data/output/`. The default scenario for the resume/demo walkthrough is `D220_V7` (220 stops, 7 vehicles).

## Key metrics

- **Distance reduction (%)** = `(baseline distance − optimized distance) / baseline distance × 100`.
- **Route duration (minutes)** = estimated drive time at the scenario's average speed + customer service minutes.
- **Active-fleet utilization (%)** = vehicles assigned at least one stop / vehicles scheduled × 100. Since the model requires each scheduled vehicle to serve at least one stop, this metric is expected to be 100% in feasible scenarios; it reflects fleet activation, not vehicle capacity or time utilization.
- **Shift utilization (%)** = route duration / available shift minutes × 100, summarized across the fleet to show workload intensity.
- **Stop capacity** = maximum delivery stops assigned to one vehicle in each scenario.

Check the generated `scenario_summary.csv` before quoting a particular percentage on a resume. Route improvements depend on the synthetic data, scenario settings, and installed solver version; no fixed distance reduction is guaranteed by the code.

## Notebook walkthrough

Open [`notebooks/last_mile_route_optimization.ipynb`](notebooks/last_mile_route_optimization.ipynb) in Jupyter to regenerate the data, inspect the scenario KPIs, compare route distances, and review the showcase fleet. Run it from the repository root.

## Sample output note

The checked-in CSVs were generated in an environment without OR-Tools, so their `solver` field reports the included angular-sweep + 2-opt fallback. In that sample run, mean distance reduction is about 20.4% across the 25 scenarios, and the `D220_V7` showcase is about 25.1%. Running after installing `requirements.txt` invokes OR-Tools and can produce different results; regenerate and quote the resulting values from your own output files.

## Power BI dashboard

See [`docs/powerbi_dashboard_guide.md`](docs/powerbi_dashboard_guide.md) for report pages, KPIs, recommended visuals, filters, and relationships. In Power BI Desktop, use **Get Data → Text/CSV** and load the output files under `data/output/`.

## Suggested resume entry

**Last-Mile Delivery Route & Fleet Optimization** — Python, Google OR-Tools, Pandas, Power BI

- Built OR-Tools routes for 200+ daily stops, benchmarking total distance against a nearest-neighbor baseline.
- Evaluated 25 demand–fleet scenarios, comparing route distance, duration, and vehicle workload to test routing robustness.
- Prepared Power BI-ready fleet datasets tracking route distance, duration, and utilization across scenario configurations.

Replace these generic bullets with the exact numbers from your generated CSVs once you run the project in your environment. Do not claim a 12% reduction unless `scenario_summary.csv` supports it for the scenario or aggregate you state.

## Limitations and possible extensions

- Synthetic coordinates are in kilometres on a Cartesian plane; they are not real GPS coordinates and do not account for road-network restrictions or live traffic.
- The baseline is intentionally simple and is intended for comparison, not as a production dispatch system.
- Add real road distances via a routing API, vehicle-specific capacities, delivery time windows, driver breaks, traffic profiles, emissions, and route maps as next steps.

## License

This repository is provided under the MIT License; see [`LICENSE`](LICENSE).
