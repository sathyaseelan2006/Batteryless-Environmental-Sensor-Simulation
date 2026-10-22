# Batteryless Sensor Node — Simulation

A runnable simulation of the core mechanisms for a self-calibrating batteryless environmental sensor node:
- Solar harvesting into a supercapacitor
- On-node neural-network solar predictor (14 inputs, 12 ReLU hidden units)
- Pre-charge assurance (Eq. 1) & opportunistic calibration gating
- Least-Age-of-Information-Slack-First (LASF) scheduler
- Naive fixed-timer baseline comparison highlighting brownout avoidance

The app opens on the **Summer (Clear-Sky Solar Charging)** scenario. Scenario weather and environmental readings are synthetic model inputs; results are prototype simulations, not measurements from hardware or a particular location. Preset settings are adjustable in the sidebar.

The app's embedded 3D view replays the same Python trace used by the charts. Its timeline can be scrubbed; changing Streamlit conditions and recalculating sends the new irradiance, capacitor state, and task events to the animation. Radio transmission remains architecture-only because the quantitative model does not schedule a radio task.

## Project Structure

- `sensor_sim.py` — Pure Python simulation engine (no Streamlit dependencies). Can be unit-tested or imported into Jupyter/analysis pipelines.
- `app.py` — Interactive Streamlit web interface with parameter controls and real-time visualization.
- `requirements.txt` — Python dependencies (`streamlit`, `numpy`, `pandas`, `scikit-learn`, `plotly`).

## Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your browser at `http://localhost:8501`.

## Key Simulation Features & Visualizations

1. **KPI Dashboard**: Calibrations executed vs deferred, sensing operations, and zero brownouts for this architecture vs naive fixed-timer failures.
2. **Energy & Irradiance Trace**: Visualizes actual vs NN-predicted irradiance alongside capacitor State-of-Charge (SoC) and execution markers.
3. **Predictor Benchmarks**: Compares MAE of NN vs EWMA and WCMA baselines.
4. **Scheduler Timeline & AoI**: Step-by-step task scheduling decisions and Age-of-Information sawtooth curves.
5. **Raw Data & CSV Export**: Export per-slot trace data and event logs.
