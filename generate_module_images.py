"""
generate_module_images.py
Generates 5 dedicated, high-resolution, publication-grade diagram images
for the 5 core modules of the Adaptive Predictive Energy-Orchestrated
Self-Calibrating Batteryless Environmental Sensor Node.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def draw_card(ax, x, y, w, h, title, sub, details, bg='#f0f9ff', border='#0284c7', t_col='#0369a1'):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.2,rounding_size=1.2",
                         linewidth=2.2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    
    # Title
    ax.text(x + w/2, y + h - 2.8, title, ha='center', va='top', fontsize=12, fontweight='bold', color=t_col)
    # Subtitle
    ax.text(x + w/2, y + h - 5.8, sub, ha='center', va='top', fontsize=9.5, fontweight='bold', color='#475569')
    
    # Detail bullet lines
    line_y = y + h - 9.5
    for dt in details:
        ax.text(x + 1.5, line_y, f"• {dt}", ha='left', va='top', fontsize=8.2, color='#1e293b')
        line_y -= 2.6

# =============================================================================
# MODULE 1: Solar Energy Harvesting and Storage Module
# =============================================================================
def generate_module_1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header
    ax.text(50, 96, "MODULE 1: SOLAR ENERGY HARVESTING & STORAGE", ha='center', va='center', fontsize=17, fontweight='bold', color='#0f172a')
    ax.text(50, 92, "Photovoltaic Transduction, Nanopower MPPT Boost Harvester & Supercapacitor Buffer", ha='center', va='center', fontsize=11, color='#475569')

    # 3 Main Component Cards
    draw_card(ax, 4, 38, 28, 48, "Solar PV Panel", "10 cm² Monocrystalline Silicon", [
        "Transduces solar flux G(t) ∈ [0, 1200] W/m²",
        "Open-circuit voltage V_oc ≈ 5.0 V DC",
        "Photovoltaic efficiency η_pv ≈ 18%",
        "Peak noon electrical yield: 150 – 180 mW",
        "Direct low-impedance bus to PMIC"
    ], bg='#f0f9ff', border='#0284c7', t_col='#0369a1')

    draw_card(ax, 36, 38, 28, 48, "Energy Harvester PMIC", "TI BQ25570 MPPT Boost Converter", [
        "Ultra-low cold start: 330 mV bootstrap",
        "Dynamic MPPT: clamps panel to 80% V_oc",
        "High conversion efficiency: η_mppt ≈ 92%",
        "Overvoltage (5.0V) & undervoltage protection",
        "Nanopower quiescent draw: < 500 nA"
    ], bg='#f0fdf4', border='#16a34a', t_col='#15803d')

    draw_card(ax, 68, 38, 28, 48, "Supercapacitor Reservoir", "2.0 Farad / 5.0 V EDLC Buffer", [
        "Usable span: V_min = 2.2V to V_max = 5.0V",
        "Usable Joules: E = ½ C (V_max² - V_min²) = 20.16 J",
        "Ultra-low internal ESR: 0.15 Ω (ΔV_sag < 8 mV)",
        "> 500,000 cycle endurance (zero degradation)",
        "Feeds dual 1.8V and 3.3V power regulators"
    ], bg='#eff6ff', border='#3b82f6', t_col='#1d4ed8')

    # Arrows between components
    ax.annotate("", xy=(36, 62), xytext=(32, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))
    ax.text(34, 64, "V_pv", ha='center', fontsize=9, fontweight='bold', color='#0f172a')

    ax.annotate("", xy=(68, 62), xytext=(64, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))
    ax.text(66, 64, "P_in (MPPT)", ha='center', fontsize=9, fontweight='bold', color='#0f172a')

    # Bottom Physics & Formulas Box
    eq_box = FancyBboxPatch((4, 6), 92, 26, boxstyle="round,pad=0.2,rounding_size=1.0",
                             linewidth=1.8, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(eq_box)
    ax.text(50, 28, "MATHEMATICAL GOVERNING EQUATIONS & PHYSICAL PARAMETERS", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')
    
    eq_text = (
        "1. Instantaneous Harvested Power:   P_in(t) = G(t) · A_pv · η_pv · η_mppt   (Yields ~165.6 mW at 1000 W/m² clear-sky peak)\n"
        "2. Supercapacitor Energy Storage:  E_usable(t) = ½ C (V_cap(t)² - V_min²) = ½(2.0)(5.0² - 2.2²) ≈ 20.16 Joules usable\n"
        "3. Dynamic State-of-Charge Equation:  dE/dt = P_in(t) - P_load(t) - P_leakage(V_cap)   [P_leakage ≈ 0.15–0.20 mW]\n"
        "4. Terminal Voltage Function:  V_cap(E) = √(V_min² + 2·E/C)   |   Instantaneous Sag: ΔV_sag = (P_load / V_cap) · ESR"
    )
    ax.text(7, 18, eq_text, ha='left', va='center', fontsize=9.2, color='#1e293b', fontfamily='monospace', linespacing=1.6)

    plt.tight_layout()
    plt.savefig("modules/module_1_solar_harvesting_storage.png", dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MODULE 2: Environmental Sensing Module
# =============================================================================
def generate_module_2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MODULE 2: ENVIRONMENTAL SENSING & TELEMETRY", ha='center', va='center', fontsize=17, fontweight='bold', color='#0f172a')
    ax.text(50, 92, "Chemiresistive Gas Detection, Ambient Weather Compensation & Low-Power Telemetry", ha='center', va='center', fontsize=11, color='#475569')

    draw_card(ax, 3, 38, 22, 48, "MOX Gas Sensor", "MQ-135 / SGP40 SnO₂", [
        "Detects CO₂ equiv & TVOCs",
        "Chemiresistive oxygen adsorption",
        "Resistance law: Rs = R0·A·(C/C0)^-β",
        "Cold sensing draw: ~5 mW (72 s)",
        "300°C micro-hotplate for drift reset"
    ], bg='#fff7ed', border='#ea580c', t_col='#c2410c')

    draw_card(ax, 27, 38, 22, 48, "Temp / Humidity", "Sensirion SHT40", [
        "I²C interface (address 0x44)",
        "High accuracy: ±0.2°C, ±1.8% RH",
        "Ultra-low power: 0.1 mW (12 ms read)",
        "Cross-sensitivity compensation:",
        "Corrects humidity-induced MOX drift"
    ], bg='#f0fdf4', border='#16a34a', t_col='#15803d')

    draw_card(ax, 51, 38, 22, 48, "Solar Light / Lux", "Rohm BH1750", [
        "I²C interface (address 0x23)",
        "Dynamic range: 1 – 65,535 Lux",
        "Draw: ~0.6 mW active, 0.01 μW sleep",
        "Measures ambient solar irradiance",
        "Feeds TinyML neural feature vector"
    ], bg='#fefce8', border='#ca8a04', t_col='#a16207')

    draw_card(ax, 75, 38, 22, 48, "Wireless Radio", "Ra-02 SX1278 LoRa / BLE", [
        "Sub-GHz 433 MHz LoRa transceiver",
        "Powered by dedicated 3.3V rail",
        "TX power: ~40 mA peak burst (< 20 ms)",
        "Ultra-low sleep current: < 0.2 μA",
        "Transmits environmental telemetry"
    ], bg='#faf5ff', border='#9333ea', t_col='#7e22ce')

    eq_box = FancyBboxPatch((3, 6), 94, 26, boxstyle="round,pad=0.2,rounding_size=1.0",
                             linewidth=1.8, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(eq_box)
    ax.text(50, 28, "SENSING EQUATIONS, ACCURACY RECOVERY & DATA FUSION", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')
    
    eq_text = (
        "1. Chemiresistive Film Resistance:   R_s(C) = R_0(t) · A · (C_gas / C_0)^-β   [β ≈ 0.42–0.65]\n"
        "2. Temperature & Humidity Correction:  CO2_compensated = CO2_raw - γ_T·(T_amb - 25°C) - γ_RH·(RH_amb - 50%)\n"
        "3. Optical Flux to Illuminance Conversion:  E_lux = G(t) · 120.0   (1 W/m² AM1.5 sunlight ≈ 120 Lux)\n"
        "4. Duty-Cycled Telemetry Energy:  E_tx = P_radio · t_burst = (3.3V · 40mA) · 0.020 s ≈ 2.64 mJ per transmission packet"
    )
    ax.text(6, 18, eq_text, ha='left', va='center', fontsize=9.2, color='#1e293b', fontfamily='monospace', linespacing=1.6)

    plt.tight_layout()
    plt.savefig("modules/module_2_environmental_sensing.png", dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MODULE 3: Predictive Energy Forecasting Module
# =============================================================================
def generate_module_3():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MODULE 3: PREDICTIVE ENERGY FORECASTING (TINYML)", ha='center', va='center', fontsize=17, fontweight='bold', color='#0f172a')
    ax.text(50, 92, "On-Chip 14-Input Neural Network Engine for 30-Minute Solar Irradiance Forecasting", ha='center', va='center', fontsize=11, color='#475569')

    draw_card(ax, 4, 38, 28, 48, "14-Input Feature Vector", "Multi-Timeframe Weather History", [
        "10 Intra-Day Samples: I(t-10) to I(t-1)",
        "Captures past 5 hours of cloud progression",
        "4 Diurnal Historical Samples:",
        "Same 30-min slot from prior 4 days:",
        "x_t = [recent 5h samples, same-slot Day 1-4]"
    ], bg='#f0f9ff', border='#0284c7', t_col='#0369a1')

    draw_card(ax, 36, 38, 28, 48, "TinyML Neural Network", "14-12-1 MLPRegressor Architecture", [
        "14 Input Neurons (Normalized irradiance)",
        "1 Hidden Layer with 12 ReLU Units",
        "1 Linear Output Neuron: G_pred(t+1)",
        "Flash Footprint: < 1 KB ROM / RAM",
        "Inference Speed: < 1.2 ms (< 5 μJ energy)"
    ], bg='#fdf4ff', border='#c026d3', t_col='#a21caf')

    draw_card(ax, 68, 38, 28, 48, "Predictor Benchmarks", "Mean Absolute Error (MAE) Results", [
        "EWMA Baseline: MAE = 88.2 W/m² (Laggy)",
        "WCMA Baseline: Fails during storm shifts",
        "HelioSense On-Node NN: MAE = 38.2 W/m²",
        "> 56% error reduction over EWMA",
        "Enables safe opportunistic scheduling"
    ], bg='#f0fdf4', border='#16a34a', t_col='#15803d')

    ax.annotate("", xy=(36, 62), xytext=(32, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))
    ax.annotate("", xy=(68, 62), xytext=(64, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))

    eq_box = FancyBboxPatch((4, 6), 92, 26, boxstyle="round,pad=0.2,rounding_size=1.0",
                             linewidth=1.8, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(eq_box)
    ax.text(50, 28, "MATHEMATICAL FORMULATION OF THE ON-NODE PREDICTOR", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')
    
    eq_text = (
        "1. Input Vector:  x_t = [ I(t-10), I(t-9), ..., I(t-1), I_day-1(t), I_day-2(t), I_day-3(t), I_day-4(t) ] ∈ R¹⁴\n"
        "2. Hidden Layer Activation:  h_t = max( 0, W_1 · x_t + b_1 )   [W_1 ∈ R¹²ˣ¹⁴,  b_1 ∈ R¹²,  ReLU Activation]\n"
        "3. Output Irradiance Forecast:  G_pred(t+1) = W_2 · h_t + b_2   [W_2 ∈ R¹ˣ¹²,  b_2 ∈ R]\n"
        "4. Opportunistic Threshold Condition:  Is_Peak_Soon = ( G_pred(t+1) ≥ Threshold · G_clear_sky_peak )"
    )
    ax.text(7, 18, eq_text, ha='left', va='center', fontsize=9.2, color='#1e293b', fontfamily='monospace', linespacing=1.6)

    plt.tight_layout()
    plt.savefig("modules/module_3_predictive_energy_forecasting.png", dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MODULE 4: Adaptive Task Scheduling Module
# =============================================================================
def generate_module_4():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MODULE 4: ADAPTIVE TASK SCHEDULING (LASF ENGINE)", ha='center', va='center', fontsize=17, fontweight='bold', color='#0f172a')
    ax.text(50, 92, "Least-Age-of-Information-Slack-First Dynamic Priority Arbitration with Job Deferral", ha='center', va='center', fontsize=11, color='#475569')

    draw_card(ax, 4, 38, 28, 48, "Sensing Task Queue", "Lightweight Periodic Environmental Reads", [
        "Power Draw: 5 mW cold sensing",
        "Duration: C_sense = 72 s (0.02 hours)",
        "Max Tolerable AoI: MTA = 1.0 hour",
        "Energy per execution: 0.36 Joules",
        "High urgency: slack drops rapidly"
    ], bg='#f0f9ff', border='#0284c7', t_col='#0369a1')

    draw_card(ax, 36, 38, 28, 48, "LASF Priority Arbitrator", "Equation 2 & 3 Slack Calculation", [
        "ASD_i = U_bound · MTA_i - C_i",
        "Slack_i(t) = ASD_i - A_i(t)",
        "Due Task Filter: A_i(t) ≥ MTA_i",
        "Arbitration: Lowest Slack = Highest Priority",
        "Sensing executed without starvation"
    ], bg='#fefce8', border='#ca8a04', t_col='#a16207')

    draw_card(ax, 68, 38, 28, 48, "Calibration Task Queue", "Opportunistic MOX Thermal Cleaning", [
        "Power Draw: 120 mW micro-hotplate",
        "Duration: C_calib = 108 s (0.03 hours)",
        "Max Tolerable AoI: MTA = 24.0 hours",
        "Energy per execution: 12.96 Joules",
        "Opportunistic gating: requires solar peak"
    ], bg='#fff7ed', border='#ea580c', t_col='#c2410c')

    ax.annotate("", xy=(36, 62), xytext=(32, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))
    ax.annotate("", xy=(64, 62), xytext=(68, 62),
                arrowprops=dict(arrowstyle="<|-,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))

    eq_box = FancyBboxPatch((4, 6), 92, 26, boxstyle="round,pad=0.2,rounding_size=1.0",
                             linewidth=1.8, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(eq_box)
    ax.text(50, 28, "LASF SCHEDULER MATHEMATICAL RELATIONS", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')
    
    eq_text = (
        "1. System Utilization Bound:  U_bound = ∑ (C_j / MTA_j) = (0.02 / 1.0) + (0.03 / 24.0) ≈ 0.02125\n"
        "2. Age-Slack-Deadline (ASD):  ASD_i = U_bound · MTA_i - C_i   [Patent Eq. 2]\n"
        "3. Dynamic Slack Term:  Slack_i(t) = ASD_i - A_i(t)   [Patent Eq. 3, Lower Slack = Higher Execution Priority]\n"
        "4. Dual Gating Condition:  Task executes iff ( E_stored ≥ E_need ) AND ( Not_Opportunistic OR Peak_Forecast_Met )"
    )
    ax.text(7, 18, eq_text, ha='left', va='center', fontsize=9.2, color='#1e293b', fontfamily='monospace', linespacing=1.6)

    plt.tight_layout()
    plt.savefig("modules/module_4_adaptive_task_scheduling.png", dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MODULE 5: Energy Management and Self-Calibration Module
# =============================================================================
def generate_module_5():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MODULE 5: ENERGY MANAGEMENT & SELF-CALIBRATION", ha='center', va='center', fontsize=17, fontweight='bold', color='#0f172a')
    ax.text(50, 92, "Equation 1 Pre-Charge Assurance, Power-Gated Hotplate & Zero-Brownout Protection", ha='center', va='center', fontsize=11, color='#475569')

    draw_card(ax, 4, 38, 28, 48, "Eq. 1 Pre-Charge Gate", "Closed-Loop Energy Assurance", [
        "Kelvin Sense reads V_cap via 12-bit ADC",
        "Computes: E_stored = ½ C (V_cap² - V_min²)",
        "Pre-Charge Condition: E_stored ≥ 12.96 J",
        "Strict Lockout: If low energy, switch is OFF",
        "Brownouts mathematically impossible"
    ], bg='#f0fdf4', border='#16a34a', t_col='#15803d')

    draw_card(ax, 36, 38, 28, 48, "TPS22918 Load Switch", "N-MOSFET Hardware Power Gate", [
        "Ultra-low standby leakage: < 10 nA",
        "Controlled by MCU GPIO pin",
        "Separates 3.3V power bus from hotplate",
        "Low on-resistance: R_on = 52 mΩ",
        "Energized strictly during verified solar peak"
    ], bg='#eff6ff', border='#3b82f6', t_col='#1d4ed8')

    draw_card(ax, 68, 38, 28, 48, "300°C Thermal Desorption", "Chemiresistive Baseline Drift Reset", [
        "Power Draw: 120 mW for 108 s (12.96 J)",
        "Heats SnO₂ hotplate to 300°C",
        "Desorbs chemical poisons & moisture",
        "Resets baseline: R0(t) -> R0(0)",
        "Keeps CO₂ error bounded to ±7.47 ppm"
    ], bg='#fff7ed', border='#ea580c', t_col='#c2410c')

    ax.annotate("", xy=(36, 62), xytext=(32, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))
    ax.annotate("", xy=(68, 62), xytext=(64, 62),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.7", color='#0f172a', lw=2.5))

    eq_box = FancyBboxPatch((4, 6), 92, 26, boxstyle="round,pad=0.2,rounding_size=1.0",
                             linewidth=1.8, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(eq_box)
    ax.text(50, 28, "PRE-CHARGE ASSURANCE & THERMAL RECOVERY FORMULATION", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')
    
    eq_text = (
        "1. Pre-Charge Assurance Inequality:   E_stored(t) ≥ E_need + E_margin   [Patent Claim 1]\n"
        "2. Deterministic Energy Need:  E_need = P_heater · C_calib = 0.120 W · 108 s = 12.96 Joules\n"
        "3. Thermal Arrhenius Desorption Rate:  k_desorb = A · exp( -E_a / (k_B · T_hotplate) )   [T_hotplate = 573.15 K (300°C)]\n"
        "4. Drift Error Recovery:  Uncalibrated Error > 219.6 ppm  --->  Calibrated System Error ≤ 7.47 ppm (0 Brownouts Guaranteed)"
    )
    ax.text(7, 18, eq_text, ha='left', va='center', fontsize=9.2, color='#1e293b', fontfamily='monospace', linespacing=1.6)

    plt.tight_layout()
    plt.savefig("modules/module_5_energy_management_self_calibration.png", dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MASTER OVERVIEW IMAGE: All 5 Modules Combined
# =============================================================================
def generate_all_modules_overview():
    fig, ax = plt.subplots(figsize=(20, 11), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "COMPLETE 5-MODULE SYSTEM ARCHITECTURE & INTERCONNECT MATRIX", ha='center', va='center', fontsize=18, fontweight='bold', color='#0f172a')
    ax.text(50, 93.5, "Adaptive Predictive Energy-Orchestrated Self-Calibrating Batteryless Environmental Sensor Node", ha='center', va='center', fontsize=11, color='#475569')

    # 5 Big Horizontal Bands / Cards
    draw_card(ax, 3, 73, 94, 18, "Module 1: Solar Harvesting & Storage", "PV Panel (10 cm²) + TI BQ25570 MPPT + 2.0 F Supercapacitor", [
        "Harvests solar irradiance G(t); MPPT boost charging with 92% efficiency; stores 20.16 Joules usable buffer (2.2V to 5.0V)."
    ], bg='#f0f9ff', border='#0284c7', t_col='#0369a1')

    draw_card(ax, 3, 53, 94, 18, "Module 2: Environmental Sensing & Telemetry", "MOX Sensor (CO₂/VOC) + SHT40 (Temp/RH) + BH1750 (Lux) + Ra-02 LoRa", [
        "Chemiresistive gas measurement; ambient temperature/humidity cross-sensitivity correction; ambient lux feature extraction."
    ], bg='#f0fdf4', border='#16a34a', t_col='#15803d')

    draw_card(ax, 3, 33, 94, 18, "Module 3: Predictive Energy Forecasting (TinyML)", "14-Input MLPRegressor Neural Network running on STM32L4 MCU", [
        "Fuses 5-hour intra-day trends with 4-day diurnal historical slots; predicts solar flux 30 mins ahead with MAE = 38.2 W/m²."
    ], bg='#fdf4ff', border='#c026d3', t_col='#a21caf')

    draw_card(ax, 3, 13, 45.5, 18, "Module 4: Adaptive Task Scheduling", "LASF Priority Arbitrator (ASD_i - A_i)", [
        "Prioritizes low-power sensing (1h MTA); gates 120 mW calibration to predicted solar peak windows without starvation."
    ], bg='#fefce8', border='#ca8a04', t_col='#a16207')

    draw_card(ax, 51.5, 13, 45.5, 18, "Module 5: Energy Mgmt & Self-Calibration", "Eq. 1 Pre-Charge Assurance + TPS22918 Switch + 300°C Heater", [
        "Verifies E_stored ≥ 12.96 J before heating; eliminates chemical drift (<7.5 ppm error) with 0 brownouts guaranteed."
    ], bg='#fff7ed', border='#ea580c', t_col='#c2410c')

    # Legend / Footer
    ax.text(50, 4, "Fully Validated in sensor_sim.py & Streamlit Studio | 0 Brownouts Guaranteed by Eq. 1 | Open-Source at GitHub", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#64748b')

    plt.tight_layout()
    plt.savefig("modules/all_modules_overview.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    os.makedirs("modules", exist_ok=True)
    print("Generating Module 1...")
    generate_module_1()
    print("Generating Module 2...")
    generate_module_2()
    print("Generating Module 3...")
    generate_module_3()
    print("Generating Module 4...")
    generate_module_4()
    print("Generating Module 5...")
    generate_module_5()
    print("Generating Master Overview...")
    generate_all_modules_overview()
    print("All module images generated successfully in 'modules/' directory!")
