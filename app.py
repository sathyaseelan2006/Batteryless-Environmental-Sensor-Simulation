"""
app.py — Interactive Scientific Simulation Studio for Batteryless Environmental Sensor Node.

Comprehensive Scientific Suite:
- Interactive Sunlight & Solar Flux Controller (0 - 1200 W/m² & AM1.5 Lux Conversion)
- Real-Time Subsystem Inspector: Solar PV, MPPT Boost, Supercapacitor, Power Rails
- Physical Sensor Models: SHT40 Thermohygrometer & MOX Gas Sensor with Drift & Thermal Annealing
- Energy Orchestration Engine: Pre-Charge Assurance (Eq. 1) & LASF Scheduling (Eq. 2-3)
- Impact & Result Analytics: Calibrated vs Uncalibrated Drift & Zero Brownouts vs Naive Failures
- 3D Hardware Model with Live Electrical Flow Visualization
"""

import json
from html import escape
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import streamlit as st
import streamlit.components.v1 as components

from sensor_sim import (
    SimConfig,
    run_simulation,
    evaluate_instant_physics,
    SLOTS_PER_DAY,
    SLOT_HOURS,
)

pio.templates.default = "plotly_white"
render_plotly_chart = st.plotly_chart

def show_chart(figure, **kwargs):
    """Keep charts readable against the dashboard's light canvas in every theme."""
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font_color="#253c54",
    )
    figure.update_xaxes(color="#53657b", gridcolor="#e4eaf1", zerolinecolor="#e4eaf1")
    figure.update_yaxes(color="#53657b", gridcolor="#e4eaf1", zerolinecolor="#e4eaf1")
    return render_plotly_chart(figure, **kwargs)

st.set_page_config(
    page_title="Batteryless Sensor Node | Scientific Simulation Studio",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="auto"
)

# --------------------------------------------------------------------------
# Modern Premium CSS Styling
# --------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
:root { color-scheme: light; }
.stApp { background: #f5f7fa; color: #172b43; font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #f5f7fa; color: #172b43; }
[data-testid="stHeader"] { background: rgba(245,247,250,.92); }
[data-testid="stSidebar"] { background: #fff; border-right: 1px solid #e4eaf1; }
[data-testid="stSidebar"] > div:first-child { background: #fff; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color: #53657b; }
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 { color: #172b43; }
.block-container { max-width: 1560px; padding-top: 1.8rem; padding-bottom: 3rem; }
h1, h2, h3 { color: #172b43; letter-spacing: -.035em; font-weight: 700 !important; }
[data-testid="stMetric"] { background: #fff; border: 1px solid #e4eaf1; border-radius: 12px; padding: 14px 16px; box-shadow: 0 2px 8px #18314b08; }
[data-testid="stMetricLabel"] { color: #667991; font-size: .80rem; font-weight: 600; }
[data-testid="stMetricValue"] { color: #172b43; font-size: 1.55rem; font-weight: 700; }
div.stButton > button { min-height: 38px; border-radius: 8px; border: 1px solid #dce4ed; background: #fff; color: #334960; font-weight: 600; transition: .15s ease; }
div.stButton > button:hover { border-color: #62a992; color: #176b55; background: #f2faf7; }
div.stButton > button[kind="primary"] { background: #176b55; border-color: #176b55; color: #fff; }
div.stButton > button[kind="primary"]:hover { background: #115742; border-color: #115742; }
[data-testid="stBaseButton-primary"] { background: #176b55 !important; border-color: #176b55 !important; color: #fff !important; }
[data-testid="stSlider"] [role="slider"] { background: #176b55 !important; border-color: #176b55 !important; }
[data-testid="stSlider"] [data-baseweb="slider"] > div > div { background: #176b55 !important; }
[data-testid="stTabs"] [role="tab"] { color: #667991; font-weight: 600; font-size: 0.95rem; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: #176b55 !important; border-bottom-color: #176b55 !important; }
[data-baseweb="tab-highlight"] { background-color: #176b55 !important; }
.hero { display:flex; align-items:center; gap:16px; margin:0 0 12px; }
.hero-icon { width:50px; height:50px; border-radius:14px; display:grid; place-items:center; background:#e7f4ef; color:#176b55; flex:none; }
.hero-icon svg { width:28px; height:28px; }
.hero-copy h1 { margin:0; padding:0; font-size:2.1rem; line-height: 1.2; }
.hero-copy p { margin:4px 0 0; color:#65788e; font-size:0.96rem; }

/* Control Deck Container */
.sunlight-deck { background:#fff; border:1px solid #e4eaf1; border-radius:14px; padding:18px 22px; margin-bottom:20px; box-shadow:0 3px 12px #18314b08; }
.deck-badge { display:inline-block; font-size:0.72rem; font-weight:700; letter-spacing:0.06em; color:#176b55; background:#e7f4ef; padding:4px 10px; border-radius:6px; margin-bottom:8px; }
.deck-title { font-size:1.15rem; font-weight:700; color:#172b43; margin-bottom:4px; }
.deck-desc { font-size:0.86rem; color:#65788e; margin-bottom:12px; }

/* Subsystem Inspector Cards */
.subsystem-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin:16px 0; }
.subsystem-card { background:#fff; border:1px solid #e4eaf1; border-radius:12px; padding:16px; box-shadow:0 2px 8px #18314b06; }
.subsystem-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #f0f4f8; }
.subsystem-title { font-size:0.92rem; font-weight:700; color:#172b43; display:flex; align-items:center; gap:8px; }
.status-pill { font-size:0.72rem; font-weight:700; padding:3px 9px; border-radius:20px; }
.pill-active { background:#e7f4ef; color:#176b55; }
.pill-warning { background:#fef3e2; color:#b45309; }
.pill-danger { background:#fee2e2; color:#b91c1c; }
.pill-neutral { background:#f1f5f9; color:#475569; }

.param-row { display:flex; justify-content:space-between; align-items:center; padding:5px 0; font-size:0.82rem; border-bottom:1px dashed #f1f5f8; }
.param-label { color:#667991; }
.param-val { font-weight:600; color:#172b43; font-family:'DM Mono', monospace; }
.param-formula { font-size:0.74rem; color:#889bb0; font-style:italic; margin-top:6px; }

.model-heading { display:flex; align-items:center; gap:10px; margin:0 0 4px; }
.model-flow-legend { display:flex; align-items:center; flex-wrap:wrap; gap:7px 14px; margin:8px 0; padding:8px 12px; border:1px solid #e4eaf1; border-radius:9px; background:#fff; color:#53657b; font-size:.72rem; }
.model-flow-legend span { display:inline-flex; align-items:center; gap:6px; }
.model-flow-legend i { width:8px; height:8px; border-radius:50%; display:inline-block; }
.model-flow-legend i.harvest { background:#ffc76a; }
.model-flow-legend i.stored { background:#68b5ff; }
.model-flow-legend i.signals { width:12px; height:0; border-top:2px dashed #b898ff; border-radius:0; }
.model-flow-legend i.heater { background:#55e6ad; }

.equation-box { background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid #176b55; border-radius:8px; padding:14px 18px; margin:14px 0; }
.equation-box h4 { margin:0 0 6px; color:#172b43; font-size:0.95rem; }
.equation-box p { margin:0; font-size:0.84rem; color:#475569; line-height:1.5; }

/* Architecture Tab Specific Styling */
.arch-hero-box { background:#fff; border:1px solid #e4eaf1; border-radius:12px; padding:18px 22px; margin-bottom:18px; box-shadow:0 2px 10px #18314b06; }
.arch-tag { display:inline-block; font-size:0.72rem; font-weight:700; letter-spacing:0.06em; color:#176b55; background:#e7f4ef; padding:3px 9px; border-radius:6px; margin-right:8px; }
.bus-legend-container { display:flex; gap:16px; flex-wrap:wrap; margin:12px 0 16px; padding:12px 16px; background:#fff; border:1px solid #e4eaf1; border-radius:10px; }
.bus-item { display:flex; align-items:center; gap:8px; font-size:0.82rem; font-weight:600; color:#334960; }
.bus-line { width:24px; height:3px; border-radius:2px; display:inline-block; }
.bus-line.pwr { background:#ef4444; }
.bus-line.adc { background:#3b82f6; border-top:2px dashed #3b82f6; height:0; }
.bus-line.dig { background:#1e293b; }
.bus-line.gpo { background:#10b981; }
.arch-card { background:#fff; border:1px solid #e4eaf1; border-radius:12px; padding:16px; box-shadow:0 2px 8px #18314b06; margin-bottom:14px; }
.arch-card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; border-bottom:1px solid #f0f4f8; padding-bottom:8px; }
.arch-card-title { font-size:0.95rem; font-weight:700; color:#172b43; display:flex; align-items:center; gap:8px; }
.arch-card-part { font-family:'DM Mono', monospace; font-size:0.75rem; background:#f1f5f9; padding:2px 7px; border-radius:4px; color:#475569; }
.arch-prop { font-size:0.83rem; margin-bottom:6px; color:#53657b; line-height:1.45; }
.arch-prop b { color:#172b43; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Predefined Environmental Condition Profiles
# --------------------------------------------------------------------------
PRESET_CONDITIONS = {
    "Summer": {
        "badge": "Clear-Sky Solar Charging",
        "description": "High solar abundance (1100 W/m² peak). Rapid supercapacitor charging enables timely heater calibrations, keeping sensor drift near zero with no brownouts.",
        "charging_speed_label": "308 mW peak harvest · Fast recharge",
        "params": {
            "days": 6, "cloud_variability": 0.05, "seed": 42,
            "peak_irradiance": 1100.0, "panel_area_cm2": 14, "panel_efficiency": 0.20,
            "cap_farads": 2.0, "v_max": 5.0, "v_min": 2.2, "idle_leakage_mw": 0.15,
            "sensing_mta_h": 1.0, "calib_power_mw": 120, "calib_duration_min": 1.8,
            "calib_mta_h": 24.0, "peak_threshold": 0.55, "condition": "Clear Sky"
        }
    },
    "Monsoon": {
        "badge": "Intermittent Cloud Dynamics",
        "description": "Cloud-covered sky with 0.85 attenuation dips. Demonstrates the NN forecaster's ability to selectively trigger calibration only when solar peaks appear.",
        "charging_speed_label": "Intermittent solar input · Gating demonstrated",
        "params": {
            "days": 7, "cloud_variability": 0.85, "seed": 105,
            "peak_irradiance": 750.0, "panel_area_cm2": 8, "panel_efficiency": 0.16,
            "cap_farads": 2.0, "v_max": 4.8, "v_min": 2.2, "idle_leakage_mw": 0.25,
            "sensing_mta_h": 1.0, "calib_power_mw": 130, "calib_duration_min": 1.8,
            "calib_mta_h": 16.0, "peak_threshold": 0.45, "condition": "Monsoon"
        }
    },
    "Winter": {
        "badge": "Nordic Low-Angle Solar Trickle",
        "description": "Weak low-angle sunlight (420 W/m² peak) and short photoperiod. LASF safely defers expensive calibration to protect uninterrupted environmental sensing.",
        "charging_speed_label": "Low solar flux · Prioritizes sensing survival",
        "params": {
            "days": 6, "cloud_variability": 0.30, "seed": 88,
            "peak_irradiance": 420.0, "panel_area_cm2": 8, "panel_efficiency": 0.15,
            "cap_farads": 2.2, "v_max": 4.5, "v_min": 2.2, "idle_leakage_mw": 0.15,
            "sensing_mta_h": 0.75, "calib_power_mw": 110, "calib_duration_min": 1.4,
            "calib_mta_h": 36.0, "peak_threshold": 0.35, "condition": "Winter"
        }
    },
    "Urban": {
        "badge": "Urban Canyon Building Shadow",
        "description": "Step-function shade drop from neighboring skyscrapers between 11:30 and 14:00. Tests Pre-Charge Assurance when sunlight collapses mid-day.",
        "charging_speed_label": "Stepped shade transitions · Brownout test",
        "params": {
            "days": 6, "cloud_variability": 0.60, "seed": 63,
            "peak_irradiance": 750.0, "panel_area_cm2": 9, "panel_efficiency": 0.17,
            "cap_farads": 1.5, "v_max": 4.8, "v_min": 2.2, "idle_leakage_mw": 0.20,
            "sensing_mta_h": 1.0, "calib_power_mw": 120, "calib_duration_min": 1.8,
            "calib_mta_h": 20.0, "peak_threshold": 0.48, "condition": "Urban"
        }
    },
    "Greenhouse": {
        "badge": "Agricultural High Duty Cycle",
        "description": "High solar input with aggressive 12-hour calibration cycle. Demonstrates rapid supercapacitor recharge following 140 mW hotplate desorption pulses.",
        "charging_speed_label": "High duty cycle · Fast thermal resets",
        "params": {
            "days": 5, "cloud_variability": 0.20, "seed": 12,
            "peak_irradiance": 950.0, "panel_area_cm2": 15, "panel_efficiency": 0.19,
            "cap_farads": 3.0, "v_max": 5.2, "v_min": 2.2, "idle_leakage_mw": 0.20,
            "sensing_mta_h": 0.5, "calib_power_mw": 140, "calib_duration_min": 2.0,
            "calib_mta_h": 12.0, "peak_threshold": 0.50, "condition": "Clear Sky"
        }
    },
    "Indoor": {
        "badge": "Indoor Diffuse Micro-Harvesting",
        "description": "Sub-milliwatt diffuse light (280 W/m²). Calibration is heavily throttled to preserve node life, illustrating graceful degradation without shutdown.",
        "charging_speed_label": "Micro-watt harvesting · Ultra-low-power mode",
        "params": {
            "days": 5, "cloud_variability": 0.15, "seed": 99,
            "peak_irradiance": 280.0, "panel_area_cm2": 12, "panel_efficiency": 0.13,
            "cap_farads": 2.0, "v_max": 4.2, "v_min": 2.2, "idle_leakage_mw": 0.08,
            "sensing_mta_h": 1.5, "calib_power_mw": 95, "calib_duration_min": 1.0,
            "calib_mta_h": 48.0, "peak_threshold": 0.30, "condition": "Indoor"
        }
    },
}

# --------------------------------------------------------------------------
# State Synchronization
# --------------------------------------------------------------------------
default_profile = list(PRESET_CONDITIONS.keys())[0]
if "active_profile" not in st.session_state or st.session_state["active_profile"] not in PRESET_CONDITIONS:
    st.session_state["active_profile"] = default_profile

def apply_profile(profile_name):
    st.session_state["active_profile"] = profile_name
    st.session_state["timeline_hour"] = 12.5
    if profile_name in PRESET_CONDITIONS:
        params = PRESET_CONDITIONS[profile_name]["params"]
        widget_keys = {
            "days": "w_days", "cloud_variability": "w_cloud", "peak_irradiance": "w_peak",
            "panel_area_cm2": "w_area", "panel_efficiency": "w_eff", "seed": "w_seed",
            "cap_farads": "w_cap", "v_max": "w_vmax", "v_min": "w_vmin",
            "idle_leakage_mw": "w_leak", "sensing_mta_h": "w_sense_mta",
            "calib_power_mw": "w_calib_p", "calib_duration_min": "w_calib_d",
            "calib_mta_h": "w_calib_mta", "peak_threshold": "w_thresh",
            "condition": "w_cond",
        }
        for k, v in params.items():
            st.session_state[f"cfg_{k}"] = v
            if widget_keys.get(k) in st.session_state:
                st.session_state[widget_keys[k]] = v

default_p = PRESET_CONDITIONS[st.session_state["active_profile"]]["params"]
for k, v in default_p.items():
    if f"cfg_{k}" not in st.session_state:
        st.session_state[f"cfg_{k}"] = v

# --------------------------------------------------------------------------
# Top Hero Banner
# --------------------------------------------------------------------------
st.markdown("""
<div class="hero">
  <div class="hero-icon">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>
    </svg>
  </div>
  <div class="hero-copy">
    <h1>Batteryless Environmental Sensor Node</h1>
    <p>Scientific Simulation Studio: Adjust solar irradiance, inspect intermediate sensor/circuit equations, and verify autonomous brownout prevention.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Interactive Sunlight Control Deck (Prominently Placed)
# --------------------------------------------------------------------------
with st.container():
    st.markdown("""
    <div class="sunlight-deck">
      <div class="deck-badge">INTERACTIVE SOLAR &amp; SENSOR TESTBENCH</div>
      <div class="deck-title">Adjust Sunlight &amp; Observe Scientific Operation in Real-Time</div>
      <div class="deck-desc">
        Change the solar flux below to immediately see how the PV panel, supercapacitor, dual power rails (1.8V / 3.3V), SHT40, and MOX gas sensor respond with exact mathematical precision.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_env, col_sun_slider, col_sun_kpi = st.columns([1.2, 2.3, 1.5], gap="medium")

    with col_env:
        selected_prof = st.selectbox(
            "Select Scenario Preset",
            list(PRESET_CONDITIONS.keys()),
            index=list(PRESET_CONDITIONS.keys()).index(st.session_state["active_profile"]),
            key="prof_select",
            on_change=lambda: apply_profile(st.session_state["prof_select"])
        )
        current_prof = PRESET_CONDITIONS[st.session_state["active_profile"]]
        st.caption(f"**{current_prof['badge']}**\n\n{current_prof['charging_speed_label']}")

    with col_sun_slider:
        live_sunlight = st.slider(
            "☀️ Solar Flux Irradiance G (W/m²)",
            min_value=0,
            max_value=1300,
            value=int(st.session_state.get("cfg_peak_irradiance", 900.0)),
            step=25,
            key="live_sun_slider",
            help="Solar irradiance at Earth's surface (AM1.5 spectrum). Clear solar noon is ~1000 W/m²."
        )
        # Quick-set condition buttons
        btn1, btn2, btn3, btn4, btn5, btn6 = st.columns(6)
        if btn1.button("☀️ Noon (1050)", use_container_width=True):
            st.session_state["live_sun_slider"] = 1050
            st.session_state["cfg_peak_irradiance"] = 1050.0
            st.rerun()
        if btn2.button("⛅ Cloud (580)", use_container_width=True):
            st.session_state["live_sun_slider"] = 580
            st.session_state["cfg_peak_irradiance"] = 580.0
            st.rerun()
        if btn3.button("🌧️ Storm (180)", use_container_width=True):
            st.session_state["live_sun_slider"] = 180
            st.session_state["cfg_peak_irradiance"] = 180.0
            st.rerun()
        if btn4.button("🏢 Shade (80)", use_container_width=True):
            st.session_state["live_sun_slider"] = 80
            st.session_state["cfg_peak_irradiance"] = 80.0
            st.rerun()
        if btn5.button("🌙 Night (0)", use_container_width=True):
            st.session_state["live_sun_slider"] = 0
            st.session_state["cfg_peak_irradiance"] = 0.0
            st.rerun()
        if btn6.button("💡 Indoor (35)", use_container_width=True):
            st.session_state["live_sun_slider"] = 35
            st.session_state["cfg_peak_irradiance"] = 35.0
            st.rerun()

    # Synchronize the slider with the simulation peak irradiance
    if float(live_sunlight) != float(st.session_state["cfg_peak_irradiance"]):
        st.session_state["cfg_peak_irradiance"] = float(live_sunlight)

    with col_sun_kpi:
        panel_area_cm2 = float(st.session_state["cfg_panel_area_cm2"])
        panel_eff = float(st.session_state["cfg_panel_efficiency"])
        mppt_eff = 0.92
        calc_peak_mw = live_sunlight * (panel_area_cm2 / 10000.0) * panel_eff * mppt_eff * 1000.0
        calc_lux = live_sunlight * 120.0
        kpi_a, kpi_b = st.columns(2)
        kpi_a.metric("Illuminance", f"{calc_lux:,.0f} lx", help="Estimated terrestrial AM1.5 illuminance (1 W/m² ≈ 120 lux)")
        kpi_b.metric("Harvested Power", f"{calc_peak_mw:.1f} mW", help="Photovoltaic power delivered into supercapacitor via MPPT")
        if live_sunlight >= 600:
            st.markdown("<span class='status-pill pill-active'>☀️ Solar Abundant · Fast Capacitor Recharge</span>", unsafe_allow_html=True)
        elif live_sunlight >= 250:
            st.markdown("<span class='status-pill pill-warning'>⛅ Moderate Light · Selective Gating Active</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-pill pill-danger'>🌧️ Solar Deficit · Pre-Charge Lockout Guard</span>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Sidebar: Advanced Scientific Parameters
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Node Hardware Architecture")
    st.caption("Adjust component physical parameters. Every change recalculates the trace.")

    with st.expander("Photovoltaic & Harvester", expanded=True):
        panel_area_cm2 = st.slider("PV Panel Area (cm²)", 1, 40, int(st.session_state["cfg_panel_area_cm2"]), key="w_area")
        panel_efficiency = st.slider("Panel Efficiency η_pv", 0.05, 0.30, float(st.session_state["cfg_panel_efficiency"]), 0.01, key="w_eff")
        cloud_variability = st.slider("Cloud Attenuation Fraction", 0.0, 1.0, float(st.session_state["cfg_cloud_variability"]), 0.05, key="w_cloud")
        days = st.slider("Simulation Duration (Days)", 3, 21, int(st.session_state["cfg_days"]), key="w_days")
        seed = st.number_input("RNG Seed", value=int(st.session_state["cfg_seed"]), step=1, key="w_seed")

    with st.expander("Supercapacitor Energy Storage", expanded=True):
        cap_farads = st.slider("Capacitance C (Farads)", 0.2, 5.0, float(st.session_state["cfg_cap_farads"]), 0.1, key="w_cap")
        v_max = st.slider("Max Voltage V_max (V)", 3.0, 6.0, float(st.session_state["cfg_v_max"]), 0.1, key="w_vmax")
        v_min = st.slider("Cutoff Voltage V_min (V)", 1.5, 3.5, float(st.session_state["cfg_v_min"]), 0.1, key="w_vmin")
        idle_leakage_mw = st.slider("Circuit Idle Leakage (mW)", 0.05, 2.0, float(st.session_state["cfg_idle_leakage_mw"]), 0.05, key="w_leak")

    with st.expander("Sensors & LASF Scheduler", expanded=True):
        sensing_mta_h = st.slider("Sensing Max AoI (Hours)", 0.25, 6.0, float(st.session_state["cfg_sensing_mta_h"]), 0.25, key="w_sense_mta")
        calib_power_mw = st.slider("MOX Heater Power (mW)", 80, 200, int(st.session_state["cfg_calib_power_mw"]), 5, key="w_calib_p")
        calib_duration_min = st.slider("Heater On-Time (Min)", 0.5, 5.0, float(st.session_state["cfg_calib_duration_min"]), 0.1, key="w_calib_d")
        calib_mta_h = st.slider("Calibration Max AoI (Hours)", 4.0, 72.0, float(st.session_state["cfg_calib_mta_h"]), 1.0, key="w_calib_mta")
        peak_threshold = st.slider("Peak Forecast Threshold", 0.2, 0.9, float(st.session_state["cfg_peak_threshold"]), 0.05, key="w_thresh")

    st.button("🔄 Recalculate Simulation", type="primary", use_container_width=True)

# --------------------------------------------------------------------------
# Simulation Execution
# --------------------------------------------------------------------------
cfg = SimConfig(
    days=days,
    peak_irradiance=float(st.session_state["cfg_peak_irradiance"]),
    cloud_variability=cloud_variability,
    panel_area_m2=panel_area_cm2 / 10_000.0,
    panel_efficiency=panel_efficiency,
    mppt_efficiency=0.92,
    idle_leakage_w=idle_leakage_mw / 1000.0,
    cap_farads=cap_farads,
    v_max=v_max,
    v_min=v_min,
    cap_esr_ohms=0.15,
    sensing_mta_hours=sensing_mta_h,
    calib_power_w=calib_power_mw / 1000.0,
    calib_duration_hours=calib_duration_min / 60.0,
    calib_mta_hours=calib_mta_h,
    peak_forecast_threshold=peak_threshold,
    seed=int(seed),
    condition=current_prof["params"].get("condition", "Clear Sky"),
)

try:
    sim_result = run_simulation(cfg)
    cfg_error = None
except ValueError as e:
    sim_result = None
    cfg_error = str(e)

if cfg_error:
    st.error(f"⚠️ Physical Inconsistency: {cfg_error}")
    st.stop()

df = sim_result["trace"]
events = sim_result["events"]
summary = sim_result["summary"]
mae = sim_result["predictor_mae"]

# Physical Metrics
peak_harvester_power_mw = cfg.peak_irradiance * cfg.panel_area_m2 * cfg.panel_efficiency * cfg.mppt_efficiency * 1000.0
usable_energy_j = 0.5 * cap_farads * (v_max**2 - v_min**2)
heater_energy_j = (calib_power_mw / 1000.0) * (calib_duration_min * 60.0)

# Timeline Slider
trace_step_hours = float(df["hour"].iloc[1] - df["hour"].iloc[0]) if len(df) > 1 else 0.5
trace_max_hour = float(df["hour"].iloc[-1])
if "timeline_hour" not in st.session_state:
    st.session_state["timeline_hour"] = min(12.5, trace_max_hour)
if st.session_state.get("timeline_hour", 0.0) > trace_max_hour:
    st.session_state["timeline_hour"] = trace_max_hour

# --------------------------------------------------------------------------
# Multi-Tab Interface Organization
# --------------------------------------------------------------------------
tab_live, tab_arch, tab_bench, tab_analysis, tab_science, tab_data = st.tabs([
    "🕹️ Interactive 3D Model & Timeline",
    "🏗️ Hardware Architecture & Schematic",
    "🔬 Live Sensor & Circuit Workbench",
    "📊 Comparative Analysis & Output Impact",
    "📐 Scientific Formulas & Equations",
    "📋 Full Telemetry Data"
])

# ==========================================================================
# TAB 1: INTERACTIVE 3D MODEL & TIMELINE
# ==========================================================================
with tab_live:
    timeline_col, readout_col = st.columns([3, 1])
    with timeline_col:
        timeline_hour = st.slider(
            "Scrub Simulation Timeline (Hours)",
            min_value=0.0,
            max_value=trace_max_hour,
            value=float(st.session_state.get("timeline_hour", 12.5)),
            step=trace_step_hours,
            format="%.1f h",
            key="timeline_hour",
            help="Scrub to inspect node state at any hour. The 3D animation and metrics update automatically."
        )
    selected_index = int(np.abs(df["hour"].to_numpy() - timeline_hour).argmin())
    selected_trace = df.iloc[selected_index]
    selected_slot = int(selected_trace["slot"])
    selected_hour = float(selected_trace["hour"])
    day_number = int(selected_hour // 24) + 1
    time_in_day = selected_hour % 24
    selected_time_label = f"Day {day_number} · {int(time_in_day):02d}:{int(round((time_in_day % 1) * 60)) % 60:02d}"

    with readout_col:
        st.caption("Selected Time Slice")
        st.markdown(f"**{selected_time_label}** (Slot #{selected_slot})")

    col_model_hdr, col_model_mode = st.columns([1.7, 1.3])
    with col_model_hdr:
        st.markdown("<div class='model-heading'><svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round' style='width:22px;height:22px;color:#176b55;'><path d='m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z'/><path d='m4.3 7.6 7.7 4.5 7.7-4.5M12 21v-8.9'/></svg><h3 style='margin:0;'>Live 3D Hardware Node</h3></div>", unsafe_allow_html=True)
        st.caption("3D animated schematic following the simulation trace. Drag to rotate; scroll to zoom.")

    with col_model_mode:
        model_display_mode = st.radio(
            "3D View Mode",
            ["Standard Split View", "⛶ Fullscreen Cinema View (820px)"],
            horizontal=True,
            index=0,
            key="model_view_mode",
            help="Full-Screen Cinema View expands the 3D model across the full screen width with 820px height for crystal-clear 3D inspection."
        )

    st.markdown("""
    <div class="model-flow-legend" aria-label="3D model flow legend">
      <span><i class="harvest"></i>PV Harvested Current</span>
      <span><i class="stored"></i>Supercapacitor Regulated Rail</span>
      <span><i class="signals"></i>LASF Control &amp; Data</span>
      <span><i class="heater"></i>3.3V Switched Heater Rail</span>
    </div>
    """, unsafe_allow_html=True)

    is_cinema = "Fullscreen" in model_display_mode
    canvas_height = 820 if is_cinema else 460

    model_path = Path(__file__).with_name("batteryless_node_3d.html")
    simulation_path = Path(__file__).with_name("batteryless_simulation.js")
    if model_path.is_file() and simulation_path.is_file():
        model_html = model_path.read_text(encoding="utf-8")
        simulation_js = simulation_path.read_text(encoding="utf-8")
        calibration_events = {}
        sensing_slots = set()
        if not events.empty:
            calibration_events = {
                int(row.slot): row.event
                for row in events.itertuples(index=False)
                if row.task == "Calibration"
            }
            sensing_slots = {
                int(row.slot)
                for row in events.itertuples(index=False)
                if row.task == "Sensing" and row.event == "executed"
            }
        naive_period_slots = max(1, int(cfg.calib_mta_hours / trace_step_hours))
        trace_columns = [
            "slot", "hour", "irradiance", "soc_pct", "naive_soc_pct", "v_cap",
            "naive_v_cap", "e_stored_j", "p_harvest_mw", "p_load_mw",
        ]
        simulation_trace = []
        for row in df[trace_columns].to_dict(orient="records"):
            slot = int(row["slot"])
            simulation_trace.append({
                **{key: float(value) for key, value in row.items()},
                "calibration_event": calibration_events.get(slot, ""),
                "sensing_executed": slot in sensing_slots,
                "baseline_calibration": slot > 0 and slot % naive_period_slots == 0,
            })
        simulation_payload = {
            "scenario": st.session_state["active_profile"],
            "days": int(days),
            "start_hour": selected_hour,
            "lock_time": True,
            "peak_irradiance": float(cfg.peak_irradiance),
            "panel_area_cm2": float(panel_area_cm2),
            "panel_efficiency": float(panel_efficiency),
            "cap_farads": float(cap_farads),
            "v_min": float(v_min),
            "v_max": float(v_max),
            "idle_leakage_mw": float(idle_leakage_mw),
            "heater_power_mw": float(calib_power_mw),
            "heater_duration_min": float(calib_duration_min),
            "trace": simulation_trace,
        }
        simulation_payload_json = json.dumps(simulation_payload, separators=(",", ":"))
        model_html = model_html.replace(
            '<script src="./batteryless_simulation.js"></script>',
            f"<script>window.NODE_SIMULATION={simulation_payload_json};</script>\n<script>\n{simulation_js}\n</script>",
        )

        is_calib = selected_trace["hotplate_temp_c"] > 100.0
        card_harvest = f"""
        <div class="subsystem-card" style="margin-bottom:10px;">
          <div class="subsystem-header">
            <span class="subsystem-title">☀️ Solar Harvesting</span>
            <span class="status-pill pill-active">{selected_trace['irradiance']:.0f} W/m²</span>
          </div>
          <div class="param-row"><span class="param-label">Illuminance</span><span class="param-val">{selected_trace['lux']:,.0f} Lux</span></div>
          <div class="param-row"><span class="param-label">Harvested Power P_in</span><span class="param-val">{selected_trace['p_harvest_mw']:.1f} mW</span></div>
          <div class="param-row"><span class="param-label">PV MPP Current I_pv</span><span class="param-val">{selected_trace['i_pv_ma']:.1f} mA</span></div>
          <div class="param-row"><span class="param-label">Supercap Charge Current</span><span class="param-val">{selected_trace['i_charge_ma']:.1f} mA</span></div>
        </div>
        """
        card_cap = f"""
        <div class="subsystem-card" style="margin-bottom:10px;">
          <div class="subsystem-header">
            <span class="subsystem-title">⚡ Supercapacitor &amp; Rails</span>
            <span class="status-pill pill-active">{selected_trace['soc_pct']:.1f}% SoC</span>
          </div>
          <div class="param-row"><span class="param-label">Capacitor Voltage V_cap</span><span class="param-val">{selected_trace['v_cap']:.2f} V</span></div>
          <div class="param-row"><span class="param-label">Stored Usable Energy</span><span class="param-val">{selected_trace['e_stored_j']:.2f} J / {usable_energy_j:.2f} J</span></div>
          <div class="param-row"><span class="param-label">Net Power Balance P_net</span><span class="param-val">{selected_trace['p_net_mw']:+.1f} mW</span></div>
          <div class="param-row"><span class="param-label">3.3V Switched Rail (Heater)</span><span class="param-val">{'CLOSED (ACTIVE)' if is_calib else 'OPEN (STANDBY)'}</span></div>
          <div class="param-row"><span class="param-label">1.8V Rail (MCU &amp; SHT40)</span><span class="param-val">{selected_trace['rail_1v8_mw']:.2f} mW</span></div>
        </div>
        """
        card_sensor = f"""
        <div class="subsystem-card">
          <div class="subsystem-header">
            <span class="subsystem-title">💨 Environmental Sensors</span>
            <span class="status-pill {'pill-active' if is_calib else 'pill-neutral'}">{'🔥 Hotplate 300°C' if is_calib else 'Standby 25°C'}</span>
          </div>
          <div class="param-row"><span class="param-label">SHT40 Temp / Humidity</span><span class="param-val">{selected_trace['temp_c']:.1f} °C · {selected_trace['humidity_pct']:.0f}% RH</span></div>
          <div class="param-row"><span class="param-label">True Ambient CO₂</span><span class="param-val">{selected_trace['true_co2_ppm']:.0f} ppm</span></div>
          <div class="param-row"><span class="param-label">Measured CO₂ (Our Design)</span><span class="param-val" style="color:#176b55;">{selected_trace['co2_measured_ppm']:.0f} ppm (Δ {selected_trace['co2_error_ppm']:.0f})</span></div>
          <div class="param-row"><span class="param-label">Uncalibrated CO₂ Drift</span><span class="param-val" style="color:#b91c1c;">{selected_trace['co2_uncalibrated_ppm']:.0f} ppm (Δ {selected_trace['co2_uncalib_error_ppm']:.0f})</span></div>
          <div class="param-row"><span class="param-label">MOX Baseline R₀</span><span class="param-val">{selected_trace['mox_r0_kohm']:.1f} kΩ</span></div>
        </div>
        """

        if is_cinema:
            components.html(model_html, height=canvas_height, scrolling=False)
            st.markdown(f"<h4 style='margin:16px 0 8px;font-size:1.05rem;color:#172b43;'>🔬 Detailed Subsystem Telemetry at {selected_time_label}</h4>", unsafe_allow_html=True)
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                st.markdown(card_harvest, unsafe_allow_html=True)
            with col_t2:
                st.markdown(card_cap, unsafe_allow_html=True)
            with col_t3:
                st.markdown(card_sensor, unsafe_allow_html=True)
        else:
            model_col, telemetry_col = st.columns([1.35, 1.0], gap="large")
            with model_col:
                components.html(model_html, height=canvas_height, scrolling=False)
            with telemetry_col:
                st.markdown("<h3 style='margin:0 0 8px;font-size:1.1rem;color:#172b43;'>🔬 Detailed Subsystem Telemetry</h3>", unsafe_allow_html=True)
                st.caption(f"Exact physical states at **{selected_time_label}**")
                st.markdown(card_harvest + card_cap + card_sensor, unsafe_allow_html=True)
    else:
        st.error("3D model files missing.")

    # Voltage & Charge Graph
    st.markdown("<h4 style='margin:18px 0 6px;'>Capacitor Voltage Rails &amp; Brownout Margin</h4>", unsafe_allow_html=True)
    live_fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
        subplot_titles=("Supercapacitor Voltage Rail (V_cap) · Adaptive Node vs Naive Baseline", "State of Charge (%)"),
    )
    live_fig.add_trace(go.Scatter(x=df["hour"], y=df["v_cap"], name="Our Adaptive Node", line=dict(color="#176b55", width=2.4)), row=1, col=1)
    live_fig.add_trace(go.Scatter(x=df["hour"], y=df["naive_v_cap"], name="Conventional Fixed-Timer Baseline", line=dict(color="#d4873d", width=1.8, dash="dash")), row=1, col=1)
    live_fig.add_hline(y=cfg.v_min, line_dash="dot", line_color="#e74c3c", annotation_text=f"Cutoff V_min ({cfg.v_min}V)", row=1, col=1)
    live_fig.add_hline(y=cfg.v_max, line_dash="dot", line_color="#2ecc71", annotation_text=f"Full V_max ({cfg.v_max}V)", row=1, col=1)

    live_fig.add_trace(go.Scatter(x=df["hour"], y=df["soc_pct"], name="Adaptive Charge (%)", showlegend=False, line=dict(color="#176b55", width=2.2)), row=2, col=1)
    live_fig.add_trace(go.Scatter(x=df["hour"], y=df["naive_soc_pct"], name="Naive Charge (%)", showlegend=False, line=dict(color="#d4873d", width=1.8, dash="dash")), row=2, col=1)
    live_fig.add_vline(x=selected_hour, line_color="#3b6eaa", line_dash="dot", line_width=1.5)

    live_fig.update_xaxes(title_text="Simulation Time (Hours)", row=2, col=1)
    live_fig.update_yaxes(title_text="Volts", row=1, col=1)
    live_fig.update_yaxes(title_text="Percent (%)", range=[0, 105], row=2, col=1)
    live_fig.update_layout(
        height=400, template="plotly_white", hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=60, b=25, l=45, r=15),
    )
    show_chart(live_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    with st.expander("📐 View Hardware Block Diagram Reference", expanded=False):
        arch_ref_img = Path(__file__).with_name("architecture_reference.png")
        if arch_ref_img.is_file():
            st.image(
                str(arch_ref_img),
                caption="Hardware Block Diagram Reference — Solar Harvesting, Supercapacitor Buffer, Dual Regulated Rails, SHT40, BH1750, and Switched MOX Gas Sensor",
                use_container_width=True
            )
            st.caption("💡 For the complete engineering breakdown, signal routing specifications, and component bill-of-materials, visit the **🏗️ Hardware Architecture & Schematic** tab.")

# ==========================================================================
# TAB 2: HARDWARE ARCHITECTURE & SCHEMATIC BREAKDOWN
# ==========================================================================
with tab_arch:
    st.markdown("""
    <div class="arch-hero-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span class="arch-tag">SYSTEM HARDWARE SPECIFICATION</span>
        <span style="font-size:0.8rem; color:#64748b; font-weight:600;">Autonomous Batteryless Energy Harvesting</span>
      </div>
      <h2 style="margin:0 0 8px; font-size:1.4rem; color:#172b43;">Hardware Architecture &amp; Signal/Power Interconnect Diagram</h2>
      <p style="margin:0; font-size:0.88rem; color:#53657b; line-height:1.55;">
        The self-calibrating batteryless environmental sensor node integrates micro-solar energy harvesting, supercapacitor energy buffering, dual-rail voltage regulation, ultra-low-power sensing, and hardware-gated thermal annealing. The architecture eliminates chemical batteries entirely, providing maintenance-free operation across decades without brownout shutdowns.
      </p>
    </div>
    """, unsafe_allow_html=True)

    arch_img_file = Path(__file__).with_name("architecture_reference.png")
    if arch_img_file.is_file():
        st.image(
            str(arch_img_file),
            caption="Figure 1: Complete Hardware System Architecture Diagram — Solar PV, BQ25570 MPPT PMIC Harvester, 2.0F Supercapacitor, Dual 1.8V/3.3V Rails, STM32L4 MCU, SHT40, BH1750, MOSFET Load Switch, MOX Gas Sensor, and LoRa Wireless Module.",
            use_container_width=True
        )
    else:
        st.warning("Hardware architecture diagram image ('architecture_reference.png') was not found in the workspace.")

    # Bus Legend
    st.markdown("""
    <div class="bus-legend-container">
      <div class="bus-item"><span class="bus-line pwr"></span> <span><b>Red Solid Lines:</b> DC Power Rails (Harvested DC, Raw V_cap 2.2V–5.0V, 1.8V LDO, 3.3V Buck, Switched 3.3V Heater)</span></div>
      <div class="bus-item"><span class="bus-line adc"></span> <span><b>Blue Dashed Line:</b> V_cap Sense (Direct ADC Feedback Line to MCU for Eq. 1 Assurance)</span></div>
      <div class="bus-item"><span class="bus-line dig"></span> <span><b>Black Solid Lines:</b> Digital Buses (I²C for SHT40 &amp; BH1750, SPI/UART for LoRa/BLE)</span></div>
      <div class="bus-item"><span class="bus-line gpo"></span> <span><b>GPIO Line:</b> Discrete Gate Control (ON/OFF to MOSFET Load Switch)</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Subsystem Cards
    st.markdown("<h3 style='margin:20px 0 10px; color:#172b43;'>🔬 Detailed Subsystem Engineering Breakdown</h3>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2, gap="medium")

    with col_a1:
        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">☀️ 1. Solar Photovoltaic (PV) Panel</span>
            <span class="arch-card-part">10 cm² · 5.0V</span>
          </div>
          <div class="arch-prop"><b>Function:</b> Primary energy transducer harvesting ambient sunlight from 0 to 1200 W/m² (AM1.5 terrestrial spectrum).</div>
          <div class="arch-prop"><b>Electrical Output:</b> Generates variable DC voltage (0.5V to 5.0V) and proportional photocurrent based on solar flux and incidence angle.</div>
          <div class="arch-prop"><b>Characteristics:</b> Monocrystalline silicon cells with conversion efficiency η_pv ≈ 16%–20%. Peak electrical yield reaches 150–200 mW under clear-sky direct noon sun.</div>
          <div class="arch-prop"><b>Connection:</b> Directly routed via solid red DC bus to the input of the BQ25570 Energy Harvester PMIC.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">⚡ 2. Energy Harvester PMIC</span>
            <span class="arch-card-part">TI BQ25570</span>
          </div>
          <div class="arch-prop"><b>Function:</b> Nanopower boost charger with embedded Maximum Power Point Tracking (MPPT) optimized for high-impedance micro-energy sources.</div>
          <div class="arch-prop"><b>Cold-Start Capability:</b> Capable of autonomous bootstrap cold-start from input voltages as low as 330 mV without battery assistance.</div>
          <div class="arch-prop"><b>MPPT Tracking:</b> Dynamically samples open-circuit voltage (V_oc) every 16 seconds and clamps panel operating voltage to ~80% V_oc (the maximum power transfer point), achieving up to 92% boost efficiency.</div>
          <div class="arch-prop"><b>Energy Delivery:</b> Charges the supercapacitor buffer while enforcing over-voltage (5.0V) and under-voltage protection thresholds.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">🔋 3. Supercapacitor Energy Reservoir</span>
            <span class="arch-card-part">2.0 F / 5.0 V</span>
          </div>
          <div class="arch-prop"><b>Function:</b> Primary energy storage buffer replacing consumable chemical batteries, enabling maintenance-free continuous operation.</div>
          <div class="arch-prop"><b>Operating Dynamic Span:</b> Cutoff voltage V_min = 2.2V to maximum charging voltage V_max = 5.0V.</div>
          <div class="arch-prop"><b>Usable Joules:</b> Provides E_usable = ½ C (V_max² - V_min²) = ½(2.0)(25.0 - 4.84) ≈ 20.16 Joules of usable energy.</div>
          <div class="arch-prop"><b>Endurance &amp; ESR:</b> Ultra-low Equivalent Series Resistance (ESR ≈ 0.15 Ω) limits internal voltage sag to ΔV &lt; 8 mV during 120 mW heater pulses. Virtually unlimited cycle endurance (&gt; 500,000 charge/discharge cycles).</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">📐 4. Real-Time V_cap Analog Sensing Line</span>
            <span class="arch-card-part">Blue Dashed Line · 12-bit ADC</span>
          </div>
          <div class="arch-prop"><b>Function:</b> Dedicated analog feedback sense line routing raw supercapacitor voltage (2.2V–5.0V) into an internal ADC channel of the STM32L4 MCU.</div>
          <div class="arch-prop"><b>Patent Eq. 1 Verification:</b> MCU continuously samples V_cap to verify Pre-Charge Assurance (E_stored ≥ E_task + E_margin) before every scheduling slot.</div>
          <div class="arch-prop"><b>Ultra-Low Leakage:</b> Sampled through a high-impedance (megaohm) precision resistive divider, keeping standby sensing leakage current below 25 nA.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_a2:
        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">🔌 5. Dual Power Rails &amp; Regulators</span>
            <span class="arch-card-part">1.8V LDO &amp; 3.3V LDO/Buck</span>
          </div>
          <div class="arch-prop"><b>1.8V LDO Rail:</b> Powers the STM32L4 MCU core and SHT40 temperature/humidity sensor. Operating at 1.8V drastically reduces dynamic CMOS power consumption (P ∝ C·V²·f) and supports sub-microamp deep-sleep modes.</div>
          <div class="arch-prop"><b>3.3V LDO/Buck Rail:</b> Supplies the LoRa wireless transceiver and provides clean voltage for analog front-ends and switched actuator domains.</div>
          <div class="arch-prop"><b>Decoupling Benefit:</b> Separating the 1.8V digital core from the 3.3V RF/actuator bus prevents high-current radio or heater transients from inducing brownout resets on the MCU.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">🧠 6. Ultra-Low-Power MCU</span>
            <span class="arch-card-part">STM32L4 (ARM Cortex-M4)</span>
          </div>
          <div class="arch-prop"><b>Role:</b> Central brain executing predictive ML inference and dynamic task arbitration.</div>
          <div class="arch-prop"><b>On-Node Neural Predictor:</b> Runs a compact 14-input, 12-neuron solar irradiance predictor in &lt; 1.2 ms with fixed-point arithmetic (&lt; 5 μJ energy per inference).</div>
          <div class="arch-prop"><b>LASF Scheduler:</b> Evaluates Age-of-Information (AoI), Age-Slack-Deadlines (ASD), and slack terms (Slack = ASD - A) every slot to dynamically prioritize Sensing vs Calibration tasks.</div>
          <div class="arch-prop"><b>Interfaces:</b> Dual I²C buses (SHT40 &amp; BH1750), 12-bit ADC (V_cap), GPIO (MOSFET gate control), and SPI/UART (LoRa module).</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">💨 7. MOX Gas Sensor &amp; MOSFET Load Switch</span>
            <span class="arch-card-part">TPS22918 + MQ-135 / SGP30</span>
          </div>
          <div class="arch-prop"><b>Sensing Physics:</b> Chemiresistive SnO₂ metal-oxide semiconductor detecting volatile organic compounds (VOCs) and CO₂ equivalents via surface oxygen chemisorption.</div>
          <div class="arch-prop"><b>Baseline Drift Challenge:</b> Moisture and ambient poisoning cause progressive baseline resistance drift (R₀ drift), causing severe measurement errors over time.</div>
          <div class="arch-prop"><b>Thermal Desorption (Calibration):</b> Micro-hotplate heated to 300°C (120 mW for 108 s = 12.96 J) desorbs contaminants, resetting baseline error back to zero.</div>
          <div class="arch-prop"><b>Hardware Power Gating:</b> An ultra-low-leakage N-channel MOSFET load switch (TPS22918) completely disconnects the heater during sleep/sensing (&lt; 10 nA leakage), energized strictly when authorized by the MCU.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="arch-card">
          <div class="arch-card-header">
            <span class="arch-card-title">📡 8. Environmental Sensors &amp; Telemetry</span>
            <span class="arch-card-part">SHT40 · BH1750 · Ra-02 LoRa</span>
          </div>
          <div class="arch-prop"><b>SHT40 (Sensirion):</b> Ultra-low-power I²C temperature (±0.2°C) and relative humidity (±1.8% RH) sensor (0.5 μW avg). Provides ambient compensation for gas readings.</div>
          <div class="arch-prop"><b>BH1750 (Rohm):</b> High-sensitivity I²C ambient illuminance sensor (1–65,535 lx) feeding live solar lux into the solar forecaster feature vector.</div>
          <div class="arch-prop"><b>Ra-02 LoRa (SX1278):</b> Long-range telemetry uplink operating at 433 MHz. Duty-cycled in brief bursts (&lt; 20 ms), transmitting telemetry data with zero impact on battery life.</div>
        </div>
        """, unsafe_allow_html=True)

    # Architectural Specifications Table
    st.markdown("<h3 style='margin:22px 0 10px; color:#172b43;'>📋 Subsystem Interconnect &amp; Electrical Specifications</h3>", unsafe_allow_html=True)
    
    spec_data = [
        {"Subsystem": "Solar Harvesting", "Component": "10 cm² Monocrystalline PV", "Power Rail": "0.5V – 5.0V DC", "Quiescent Power": "0 mW", "Peak Power": "150–200 mW", "Interface": "Analog DC", "Role": "Ambient solar photon-to-electron energy transducer"},
        {"Subsystem": "Energy Harvester PMIC", "Component": "TI BQ25570 MPPT PMIC", "Power Rail": "Raw Harvester Input", "Quiescent Power": "< 500 nA (330 mV cold start)", "Peak Power": "Self-powered (92% eff.)", "Interface": "Analog Boost", "Role": "Maximum Power Point Tracking & supercapacitor charging"},
        {"Subsystem": "Energy Reservoir", "Component": "Electric Double Layer (EDLC)", "Power Rail": "Raw V_cap (2.2V – 5.0V)", "Quiescent Power": "0.15 mW (leakage)", "Peak Power": "20.16 J usable capacity", "Interface": "Direct Power Rail", "Role": "Replaces battery; infinite cycle buffer (> 500k cycles)"},
        {"Subsystem": "V_cap Sensing", "Component": "Resistive Divider + 12-bit ADC", "Power Rail": "V_cap to MCU ADC", "Quiescent Power": "< 25 nA (high-Z divider)", "Peak Power": "< 0.05 mW", "Interface": "Analog ADC (Blue line)", "Role": "Real-time State-of-Charge feedback for Eq. 1 Pre-Charge Assurance"},
        {"Subsystem": "MCU Core Rail", "Component": "Ultra-Low-I_q 1.8V LDO", "Power Rail": "1.8V Regulated Rail", "Quiescent Power": "< 1 μA", "Peak Power": "15 mW", "Interface": "Regulated Rail", "Role": "Supplies STM32L4 MCU core & SHT40 with minimal P ∝ V²"},
        {"Subsystem": "Radio / Actuator Rail", "Component": "High-Efficiency 3.3V Buck", "Power Rail": "3.3V Regulated Rail", "Quiescent Power": "< 1.5 μA", "Peak Power": "60 mW", "Interface": "Regulated Rail", "Role": "Provides stable headroom for LoRa RF module & analog sensors"},
        {"Subsystem": "Microcontroller", "Component": "STM32L4 (ARM Cortex-M4)", "Power Rail": "1.8V LDO Rail", "Quiescent Power": "0.8 μW (Stop-2 sleep)", "Peak Power": "4.5 mW (active ML)", "Interface": "I²C, ADC, GPIO, SPI", "Role": "Central brain running NN solar forecaster & LASF scheduler"},
        {"Subsystem": "Temp / Humidity Sensor", "Component": "Sensirion SHT40", "Power Rail": "1.8V LDO Rail", "Quiescent Power": "0.08 μW", "Peak Power": "0.45 mW (12 ms measurement)", "Interface": "I²C (0x44)", "Role": "Precise ambient T & RH for cross-sensitivity compensation"},
        {"Subsystem": "Ambient Light Sensor", "Component": "Rohm BH1750 Photodiode", "Power Rail": "1.8V / 3.3V Rail", "Quiescent Power": "0.01 μW", "Peak Power": "0.6 mW", "Interface": "I²C (0x23)", "Role": "Measures ambient lux for solar horizon prediction feature vector"},
        {"Subsystem": "Power Gating Switch", "Component": "TI TPS22918 Load Switch", "Power Rail": "3.3V to MOX Heater", "Quiescent Power": "< 10 nA (off state)", "Peak Power": "0.02 mW (control)", "Interface": "GPIO (Gate ON/OFF)", "Role": "Completely isolates MOX heater to prevent parasitic leakage"},
        {"Subsystem": "MOX Gas Sensor", "Component": "MQ-135 / SGP30 SnO₂", "Power Rail": "Switched 3.3V Heater Rail", "Quiescent Power": "0 mW (when switch OFF)", "Peak Power": "120 mW (hotplate active)", "Interface": "Analog / I²C", "Role": "Chemiresistive gas detection; 300°C thermal drift reset"},
        {"Subsystem": "Wireless Telemetry", "Component": "Ra-02 SX1278 LoRa / BLE", "Power Rail": "3.3V Buck Rail", "Quiescent Power": "< 0.2 μA (deep sleep)", "Peak Power": "45 mW (TX burst)", "Interface": "SPI / UART", "Role": "Duty-cycled RF broadcast of environmental data & node telemetry"},
    ]
    st.dataframe(pd.DataFrame(spec_data), use_container_width=True, hide_index=True)

    # Brownout Prevention Architecture Flow
    st.markdown("""
    <div class="equation-box" style="margin-top:20px;">
      <h4 style="color:#176b55; font-size:1.05rem;">🛡️ How This Architecture Eliminates Brownouts (End-to-End Orchestration Flow)</h4>
      <p style="margin-bottom:8px;">
        Conventional fixed-timer nodes suffer repeated brownouts because they energize the 120 mW MOX heater unconditionally, crashing whenever sunlight dips. In our architecture, the hardware and software operate as a tightly coupled feedback loop:
      </p>
      <ol style="margin:0 0 10px 18px; padding:0; font-size:0.86rem; color:#475569; line-height:1.6;">
        <li><b>Continuous Harvesting:</b> The 10 cm² PV panel and BQ25570 MPPT PMIC charge the 2.0F supercapacitor reservoir whenever ambient photons are available.</li>
        <li><b>Live Voltage Monitoring:</b> The MCU samples the direct <i>V_cap Sense (ADC)</i> line to compute exact available energy <code>E_stored = ½ C (V_cap² - V_min²)</code>.</li>
        <li><b>Horizon Solar Forecasting:</b> The on-node neural network uses historical light readings (BH1750) and slot indices to forecast upcoming solar irradiance.</li>
        <li><b>Pre-Charge Assurance Gating (Eq. 1):</b> The MCU verifies that stored energy satisfies <code>E_stored ≥ E_task + E_margin</code> (where E_task = 12.96 J for calibration). If insufficient, the MOSFET load switch remains strictly locked OFF.</li>
        <li><b>Least-Age-of-Information-Slack-First (LASF) Arbitration:</b> If both sensing and calibration are viable, the scheduler arbitrates based on dynamic urgency (<code>Slack = ASD - Age</code>). Sensing operations (which consume only ~0.5 mJ) execute reliably without draining the supercapacitor.</li>
        <li><b>Protected Thermal Annealing:</b> When all conditions are satisfied, the MCU asserts the GPIO gate line, closing the TPS22918 load switch to deliver 120 mW to the MOX heater for 108 seconds, restoring pristine sensor calibration while supercapacitor voltage remains comfortably above cutoff.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)



# ==========================================================================
# TAB 2: LIVE SENSOR & CIRCUIT WORKBENCH (INSTANT PHYSICS EVALUATOR)
# ==========================================================================
with tab_bench:
    st.markdown("### 🔬 Instant Scientific Physics &amp; Sensor Evaluator")
    st.markdown("""
    Evaluate any arbitrary operating point with **100% scientific determinism**.
    Adjust the live sliders to test how variations in sunlight, capacitor voltage, and sensor age affect electrical power distribution, gas sensor drift, and LASF scheduler arbitration.
    """)

    w_col1, w_col2, w_col3, w_col4 = st.columns(4)
    with w_col1:
        test_sun = st.slider("☀️ Solar Irradiance G (W/m²)", 0, 1200, int(selected_trace["irradiance"]), step=20, key="bench_sun")
    with w_col2:
        test_vcap = st.slider("⚡ Capacitor Voltage V_cap (V)", float(v_min), float(v_max), float(selected_trace["v_cap"]), step=0.05, key="bench_v")
    with w_col3:
        test_calib_age = st.slider("⏳ Time Since Calibration (Hours)", 0.0, 72.0, float(selected_trace["calibration_age_h"]), step=1.0, key="bench_cage")
    with w_col4:
        test_hour = st.slider("🕐 Diurnal Hour of Day (0-24h)", 0.0, 24.0, float(time_in_day), step=0.5, key="bench_hour")

    # Evaluate instant physics
    pt = evaluate_instant_physics(
        irradiance_w_m2=float(test_sun),
        v_cap=float(test_vcap),
        calib_age_hours=float(test_calib_age),
        sensing_age_hours=1.0,
        cfg=cfg,
        hour_of_day=float(test_hour)
    )

    # 4 Detailed Subsystem Cards
    st.markdown("<div class='subsystem-grid'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="subsystem-card">
          <div class="subsystem-header">
            <span class="subsystem-title">☀️ Solar PV Harvester</span>
            <span class="status-pill pill-active">{pt['p_harvest_mw']:.1f} mW</span>
          </div>
          <div class="param-row"><span class="param-label">Input Irradiance G</span><span class="param-val">{pt['irradiance_w_m2']:.0f} W/m²</span></div>
          <div class="param-row"><span class="param-label">AM1.5 Illuminance</span><span class="param-val">{pt['lux']:,.0f} Lux</span></div>
          <div class="param-row"><span class="param-label">PV Current I_pv</span><span class="param-val">{pt['i_pv_ma']:.2f} mA</span></div>
          <div class="param-row"><span class="param-label">Charging Current I_charge</span><span class="param-val">{pt['i_charge_ma']:.2f} mA</span></div>
          <div class="param-row"><span class="param-label">MPPT Boost Efficiency</span><span class="param-val">92.0%</span></div>
          <div class="param-formula">P_harv = G · A_pv · η_pv · η_mppt</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="subsystem-card">
          <div class="subsystem-header">
            <span class="subsystem-title">⚡ Supercapacitor &amp; Rails</span>
            <span class="status-pill pill-active">{pt['soc_pct']:.1f}% SoC</span>
          </div>
          <div class="param-row"><span class="param-label">Capacitor Voltage</span><span class="param-val">{pt['v_cap']:.2f} V</span></div>
          <div class="param-row"><span class="param-label">Stored Usable Energy</span><span class="param-val">{pt['e_stored_j']:.2f} J</span></div>
          <div class="param-row"><span class="param-label">Internal ESR Drop</span><span class="param-val">Δ {pt['v_sag_mv']:.1f} mV</span></div>
          <div class="param-row"><span class="param-label">1.8V Rail (Always-On)</span><span class="param-val">{pt['rail_1v8_mw']:.2f} mW</span></div>
          <div class="param-row"><span class="param-label">3.3V Switched Heater</span><span class="param-val">{pt['mosfet_switch']}</span></div>
          <div class="param-formula">E_usable = ½ C (V_cap² - V_min²)</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="subsystem-card">
          <div class="subsystem-header">
            <span class="subsystem-title">💨 Sensors &amp; Drift</span>
            <span class="status-pill {'pill-active' if pt['hotplate_temp_c'] > 100 else 'pill-neutral'}">{'300°C Active' if pt['hotplate_temp_c'] > 100 else '25°C Standby'}</span>
          </div>
          <div class="param-row"><span class="param-label">SHT40 Temp / Humidity</span><span class="param-val">{pt['temp_c']:.1f} °C · {pt['humidity_pct']:.0f}% RH</span></div>
          <div class="param-row"><span class="param-label">True Ambient CO₂</span><span class="param-val">{pt['true_co2_ppm']:.0f} ppm</span></div>
          <div class="param-row"><span class="param-label">Calibrated Measured CO₂</span><span class="param-val" style="color:#176b55;">{pt['co2_measured_ppm']:.0f} ppm (Δ {pt['co2_error_ppm']:.1f})</span></div>
          <div class="param-row"><span class="param-label">Uncalibrated Drift CO₂</span><span class="param-val" style="color:#b91c1c;">{pt['co2_uncalibrated_ppm']:.0f} ppm (Δ {pt['co2_uncalib_error_ppm']:.1f})</span></div>
          <div class="param-row"><span class="param-label">Film Baseline R₀</span><span class="param-val">{pt['mox_r0_kohm']:.1f} kΩ</span></div>
          <div class="param-formula">R_s = R₀(t) · (C_gas / C₀)^(-β)</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        pre_status = "pill-active" if pt["precharge_calib_ok"] else "pill-danger"
        fore_status = "pill-active" if pt["forecast_gate_ok"] else "pill-warning"
        st.markdown(f"""
        <div class="subsystem-card">
          <div class="subsystem-header">
            <span class="subsystem-title">🧠 Orchestrator Decision</span>
            <span class="status-pill {pre_status}">{'PASS' if pt['precharge_calib_ok'] else 'LOCKED OUT'}</span>
          </div>
          <div class="param-row"><span class="param-label">Eq. 1 Pre-Charge Margin</span><span class="param-val">{pt['precharge_margin_j']:+.2f} J</span></div>
          <div class="param-row"><span class="param-label">Solar Peak Forecast Margin</span><span class="param-val">{pt['forecast_margin_w_m2']:+.0f} W/m²</span></div>
          <div class="param-row"><span class="param-label">Sensing LASF Slack</span><span class="param-val">{pt['slack_sensing']:.2f} h</span></div>
          <div class="param-row"><span class="param-label">Calibration LASF Slack</span><span class="param-val">{pt['slack_calib']:.2f} h</span></div>
          <div class="param-row"><span class="param-label">Active Node Task</span><span class="param-val">{pt['active_task']}</span></div>
          <div class="param-formula">Eq. 1: E_stored ≥ E_task | Eq. 2: Slack = ASD - A</div>
        </div>
        """, unsafe_allow_html=True)

    # Scientific Decision Summary Callout
    st.markdown(f"""
    <div class="equation-box">
      <h4>Mathematical Decision Rationale:</h4>
      <p><b>Adaptive Node Status:</b> {pt['decision_note']}</p>
      <p style="margin-top:6px;"><b>Baseline Comparison:</b> {pt['naive_outcome']}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================================
# TAB 3: COMPARATIVE ANALYSIS & OUTPUT IMPACT
# ==========================================================================
with tab_analysis:
    st.markdown("### 📊 System Resilience &amp; Measurement Accuracy Impact")
    st.caption("Side-by-side comparison of our patented predictive architecture versus conventional fixed-timer nodes under identical environmental conditions.")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Adaptive Node Brownouts", f"{summary['brownouts_this_design']}", delta="Zero Crashes", delta_color="normal")
    k2.metric("Fixed-Timer Brownouts", f"{summary['naive_brownouts']}", delta=f"{summary['naive_brownouts']} Crashes", delta_color="inverse")
    k3.metric("Avg CO₂ Error (Our Design)", f"{summary['avg_co2_error_ppm']:.1f} ppm", delta=f"Peak {summary['max_co2_error_ppm']:.1f} ppm")
    k4.metric("Avg CO₂ Error (Uncalibrated)", f"{summary['avg_uncalib_error_ppm']:.1f} ppm", delta=f"Peak {summary['max_uncalib_error_ppm']:.1f} ppm", delta_color="inverse")

    # CO2 Accuracy & Drift Plot
    st.markdown("<h4 style='margin:18px 0 6px;'>Sensor Output: Calibrated Accuracy vs Uncalibrated Drift</h4>", unsafe_allow_html=True)
    st.caption("Notice how thermal desorption pulses executed by our adaptive scheduler reset sensor drift back to zero, while the uncalibrated sensor error escalates continuously.")

    fig_co2 = go.Figure()
    fig_co2.add_trace(go.Scatter(x=df["hour"], y=df["true_co2_ppm"], name="True Ground Truth Ambient CO₂", line=dict(color="#10b981", width=2.4)))
    fig_co2.add_trace(go.Scatter(x=df["hour"], y=df["co2_measured_ppm"], name="Our Node (Drift Corrected via Timely Calibrations)", line=dict(color="#0284c7", width=2.2, dash="dash")))
    fig_co2.add_trace(go.Scatter(x=df["hour"], y=df["co2_uncalibrated_ppm"], name="Conventional Uncalibrated Sensor (Compounding Drift)", line=dict(color="#ef4444", width=1.8, dash="dot")))

    # Mark calibration executions
    calib_exec = events[(events.get("task", "") == "Calibration") & (events.get("event", "") == "executed")] if not events.empty else pd.DataFrame()
    if not calib_exec.empty:
        exec_hours = df.loc[calib_exec["slot"].values, "hour"].values
        fig_co2.add_trace(go.Scatter(
            x=exec_hours, y=[df["true_co2_ppm"].max() * 1.05] * len(exec_hours), mode="markers",
            marker=dict(symbol="triangle-down", size=13, color="#10b981", line=dict(color="black", width=1.0)),
            name="Calibration Pulse Executed (Drift Reset to Zero)"
        ))

    fig_co2.update_layout(
        height=380, template="plotly_white", xaxis_title="Simulation Time (Hours)", yaxis_title="CO₂ Concentration (ppm)",
        legend=dict(orientation="h", y=-0.2), margin=dict(t=20, b=20, l=45, r=15)
    )
    show_chart(fig_co2, use_container_width=True, theme=None)

    # Power Flow & Net Balance
    st.markdown("<h4 style='margin:18px 0 6px;'>Solar Energy Harvesting &amp; Power Demand</h4>", unsafe_allow_html=True)
    fig_power = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.10,
                              subplot_titles=["Harvested Solar Power (P_in) vs Total Operating Load (P_load)", "Net Power Balance (P_net = P_in - P_load)"])
    fig_power.add_trace(go.Scatter(x=df["hour"], y=df["p_harvest_mw"], name="Solar Harvest (mW)", line=dict(color="#f59e0b", width=2.0)), row=1, col=1)
    fig_power.add_trace(go.Scatter(x=df["hour"], y=df["p_load_mw"], name="Operating Load (mW)", line=dict(color="#ef4444", width=1.6)), row=1, col=1)
    fig_power.add_trace(go.Scatter(x=df["hour"], y=df["p_net_mw"], name="Net Surplus/Deficit (mW)", line=dict(color="#10b981", width=1.8), fill="tozeroy"), row=2, col=1)
    fig_power.add_hline(y=0, line_dash="dot", line_color="#94a3b8", row=2, col=1)
    fig_power.update_layout(height=420, template="plotly_white", margin=dict(t=30, b=20), legend=dict(orientation="h", y=-0.18))
    fig_power.update_yaxes(title_text="mW", row=1, col=1)
    fig_power.update_yaxes(title_text="Net mW", row=2, col=1)
    fig_power.update_xaxes(title_text="Simulation Time (Hours)", row=2, col=1)
    show_chart(fig_power, use_container_width=True, theme=None)

    # Task Timing & Age-of-Information (AoI)
    st.markdown("<h4 style='margin:18px 0 6px;'>Age-of-Information (AoI) Dynamics &amp; LASF Slack Terms</h4>", unsafe_allow_html=True)
    fig_aoi = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.10,
                            subplot_titles=["Age-of-Information (AoI) Sawtooth Curves", "LASF Dynamic Priority Slack (ASD - A)"])
    fig_aoi.add_trace(go.Scatter(x=df["hour"], y=df["sensing_age_h"], name="Sensing AoI (h)", line=dict(color="#0284c7")), row=1, col=1)
    fig_aoi.add_trace(go.Scatter(x=df["hour"], y=df["calibration_age_h"], name="Calibration AoI (h)", line=dict(color="#f97316")), row=1, col=1)
    fig_aoi.add_trace(go.Scatter(x=df["hour"], y=df["slack_sensing"], name="Sensing Slack", line=dict(color="#0284c7", dash="dot")), row=2, col=1)
    fig_aoi.add_trace(go.Scatter(x=df["hour"], y=df["slack_calibration"], name="Calibration Slack", line=dict(color="#f97316", dash="dot")), row=2, col=1)
    fig_aoi.update_layout(height=420, template="plotly_white", margin=dict(t=30, b=20), legend=dict(orientation="h", y=-0.18))
    fig_aoi.update_yaxes(title_text="Age (h)", row=1, col=1)
    fig_aoi.update_yaxes(title_text="Slack (h)", row=2, col=1)
    fig_aoi.update_xaxes(title_text="Simulation Time (Hours)", row=2, col=1)
    show_chart(fig_aoi, use_container_width=True, theme=None)

# ==========================================================================
# TAB 4: SCIENTIFIC PHYSICS & FORMULATIONS
# ==========================================================================
with tab_science:
    st.markdown("### 📐 Scientific Formulations &amp; Mathematical Derivations")
    st.markdown("""
    All physical processes in this simulation are derived from first-principles electromagnetic, thermodynamic, and semiconductor equations.
    Below are the explicit mathematical definitions implemented in `sensor_sim.py`.
    """)

    st.markdown(r"""
    #### 1. Solar Irradiance & Photovoltaic Harvesting
    Solar irradiance $G(t)$ follows the atmospheric optical air-mass transmission model (AM1.5 spectrum):
    $$G(t) = G_{peak} \cdot \left[\sin\left(\frac{\pi (t - 6)}{12}\right)\right]^{\alpha} \cdot (1 - \tau_{cloud})$$
    where $G_{peak}$ is the clear-sky noon flux ($\text{W/m}^2$), $\alpha \approx 1.0$ is the geometric optical exponent, and $\tau_{cloud} \in [0, 1]$ is the cloud attenuation fraction.
    
    The electrical power delivered into the energy storage capacitor via the MPPT boost converter is:
    $$P_{in}(t) = G(t) \cdot A_{pv} \cdot \eta_{pv} \cdot \eta_{mppt}$$
    where $A_{pv}$ is the active solar panel area ($\text{m}^2$), $\eta_{pv}$ is photovoltaic cell conversion efficiency, and $\eta_{mppt} \approx 0.92$ is boost tracking efficiency.

    ---
    #### 2. Supercapacitor Energy Storage & Voltage Dynamics
    The usable energy stored in a supercapacitor of capacitance $C$ (Farads) between operating voltage $V_{cap}(t)$ and cutoff threshold $V_{min}$ is:
    $$E_{usable}(t) = \frac{1}{2} C \left(V_{cap}(t)^2 - V_{min}^2\right) \quad [\text{Joules}]$$
    Inverting this equation yields the terminal capacitor voltage as a function of stored Joules:
    $$V_{cap}(E) = \sqrt{V_{min}^2 + \frac{2 E_{usable}}{C}}$$
    The continuous differential state equation governing capacitor energy under net power flow is:
    $$\frac{dE}{dt} = P_{in}(t) - P_{load}(t) - P_{leakage}(V_{cap})$$
    Internal equivalent series resistance ($ESR \approx 0.15\ \Omega$) causes an instantaneous voltage sag during high-current pulses:
    $$\Delta V_{sag} = I_{load} \cdot R_{esr} = \left(\frac{P_{load}}{V_{cap}}\right) \cdot R_{esr}$$

    ---
    #### 3. Chemiresistive MOX Gas Sensor Physics & Baseline Drift
    Metal-oxide semiconductor ($SnO_2$) sensors operate on the principle of surface oxygen ion chemisorption ($O_2^-$, $O^-$) that creates an electron depletion barrier. Reducing volatile gases ($VOC$, $CO$) react with surface oxygen, releasing conduction electrons and altering film resistance $R_s$:
    $$R_s(C) = R_0(t) \cdot A \cdot \left(\frac{C_{gas}}{C_0}\right)^{-\beta}$$
    Over time, irreversible adsorption of ambient moisture, siloxanes, and crystalline lattice relaxation cause continuous baseline resistance drift:
    $$R_0(t) = R_0(0) \cdot \left(1 + \alpha_{drift} \cdot t_{uncalibrated}\right) + \gamma_T \left(T_{amb} - 25^\circ\text{C}\right)$$
    Without recalibration, the estimated gas concentration drifts unbounded:
    $$CO_{2,uncalib}(t) = CO_{2,true}(t) \cdot (1 + \alpha_{drift} \cdot t_{uncalib}) + \gamma_T \Delta T$$
    
    **Thermal Desorption Pulse (Calibration):**
    When the MCU closes the TPS22918 load switch, $120\text{ mW}$ of power is delivered to the micro-hotplate for duration $C_{calib} = 108\text{ s}$, heating the sensing film to $300^\circ\text{C}$. This thermally desorbs poisoning adsorbates according to Arrhenius reaction kinetics, resetting $R_0 \to R_0(0)$ and restoring accuracy to $<\pm 15\text{ ppm}$.

    ---
    #### 4. Pre-Charge Assurance Inequality (Patent Claim 1)
    To guarantee that an expensive calibration cycle ($E_{calib} = 12.96\text{ J}$) can never discharge the supercapacitor below $V_{min}$ (avoiding brownout shutdown), the scheduler enforces:
    $$E_{stored}(t) \ge E_{task} + E_{margin}$$
    $$E_{task} = \int_0^{C_{calib}} P_{heater}(\tau) d\tau = P_{heater} \cdot C_{calib} = 0.12\text{ W} \times 108\text{ s} = 12.96\text{ Joules}$$

    ---
    #### 5. Least-Age-of-Information-Slack-First (LASF) Dynamic Priority (Patent Eq. 2 & 3)
    For each schedulable task $\tau_i$, its Age-Slack-Deadline ($ASD_i$) and instantaneous slack $Slack_i(t)$ are:
    $$ASD_i = U_{bound} \cdot MTA_i - C_i, \quad U_{bound} = \sum_{j} \frac{C_j}{MTA_j}$$
    $$Slack_i(t) = ASD_i - A_i(t)$$
    where $MTA_i$ is Maximum Tolerable Age, $C_i$ is worst-case execution time, and $A_i(t)$ is current Age of Information. Ready tasks are ordered such that lower slack receives higher execution priority:
    $$\tau^* = \arg\min_{\tau_i \in \text{Ready}} Slack_i(t)$$
    """)

# ==========================================================================
# TAB 5: FULL TELEMETRY DATA & CSV EXPORT
# ==========================================================================
with tab_data:
    st.markdown("### 📋 Full Simulation Telemetry Trace")
    st.caption("Inspect the complete slot-by-slot dataset or export as CSV.")
    st.dataframe(df, use_container_width=True, height=350)
    st.download_button(
        "📥 Download Trace as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="batteryless_sensor_node_trace.csv",
        mime="text/csv",
    )
