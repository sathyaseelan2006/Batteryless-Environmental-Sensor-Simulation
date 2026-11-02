# ☀️ HelioSense — Batteryless Environmental Sensor Node Simulation

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-heliosense.streamlit.app-FF4B4B.svg?logo=streamlit&logoColor=white)](https://heliosense.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Brownouts](https://img.shields.io/badge/Brownouts-0%20(Guaranteed)-success.svg)](#pre-charge-assurance)
[![Edge AI](https://img.shields.io/badge/TinyML-On--Chip%20MLP-orange.svg)](#on-chip-neural-network-predictor)

> **An end-to-end physical simulation of a perpetual, battery-free environmental air quality sensor node ($CO_2$, VOCs) powered exclusively by ambient solar harvesting, featuring on-chip neural weather forecasting, mathematical pre-charge guarantees, and Age-of-Information (LASF) scheduling.**
> 
> 🌐 **Try the Live Simulation:** [https://heliosense.streamlit.app/](https://heliosense.streamlit.app/)

---

## 📌 Executive Summary

Traditional batteryless IoT devices suffer from frequent brownout crashes when executing power-intensive operations—such as heating a metal-oxide (MOX) gas sensor ($120\text{ mW}$) from a tiny supercapacitor. Running these high-power jobs on fixed timers invariably crashes the device during cloudy or nighttime periods.

This project simulates a **predictive, energy-orchestrated architecture** that overcomes the **240× peak-to-average power paradox**:
1. **Tiny On-Chip Neural Network:** Predicts incoming solar irradiance $30\text{ minutes}$ ahead using intra-day and diurnal historical features.
2. **Mathematical Pre-Charge Assurance:** Deterministically verifies that stored energy covers the entire task demand before closing the power switch ($E_{\text{stored}} \ge E_{\text{task}}$), guaranteeing **zero brownout crashes**.
3. **Opportunistic LASF Scheduling:** Prioritizes low-power environmental monitoring and defers heavy thermal recalibration cycles to forecasted solar peaks, eliminating sensor drift without depleting stored reserves.

---

## 🏛️ System Architecture

![System Architecture Diagram](system_architecture_diagram.png)

### Hardware & Power Distribution Block Diagram

```mermaid
flowchart TD
    subgraph Harvesting ["☀️ Solar Harvesting Subsystem"]
        Sun["☀️ Ambient Sunlight"] --> PV["Solar PV Cell (10 cm²)"]
        PV --> PMIC["MPPT Boost PMIC\n(e.g., BQ25570 / AEM10941)"]
    end

    subgraph Storage ["🔋 Energy Buffer Subsystem"]
        PMIC --> SuperCap["Supercapacitor Bank\n(2.0 F / 5.0 V Usable Buffer)"]
    end

    subgraph Regulation ["⚡ Dual-Rail Power Distribution"]
        SuperCap --> Reg1["Buck / LDO Reg 1\n(Always-On 1.8 V Rail)"]
        SuperCap --> Reg2["Buck / LDO Reg 2\n(Switched 3.3 V Rail)"]
        SuperCap -.->|Voltage Feedback V_cap| ADC["ADC Voltage Monitor\n(Eq. 1 Safety Gate)"]
    end

    subgraph Compute ["🧠 Edge Intelligence (Ultra-Low-Power MCU)"]
        Reg1 --> MCU["ARM Cortex-M MCU"]
        ADC --> MCU
        MCU --- TinyML["On-Chip MLP Solar Predictor\n(14 inputs -> 12 hidden -> 1 output)"]
        MCU --- Scheduler["LASF Dynamic Scheduler\n(Least Slack First)"]
    end

    subgraph Peripherals ["📡 Sensing & Actuation Peripherals"]
        Reg1 --> TempHum["SHT40 Temp / RH Sensor\n(~0.1 mW)"]
        Reg1 --> Photo["OPT3001 Solar Flux Sensor\n(~0.05 mW)"]
        Reg1 --> BLE["BLE / LoRa Transceiver\n(Periodic Bursts)"]
        
        Reg2 --> MOSFET["MOSFET Power Switch\n(Power Gated)"]
        MCU -->|GPIO Gate Control| MOSFET
        MOSFET --> MOX["MOX Gas Sensor Micro-Heater\n(120 mW Hotplate: CO₂ & VOCs)"]
    end
```

---

## ⚡ AI-Driven Energy Management & Closed-Loop Self-Calibration

![AI-Driven Energy Management & Closed-Loop Self-Calibration](modules/ai_energy_self_calibration_diagram.png)

### 1. Where AI is Used (Physical Architecture & Hardware Placement)

The AI engine is hosted **directly on-chip** within the ultra-low-power **STM32L476 (ARM Cortex-M4)** microcontroller operating at a regulated 1.8 V rail:

```mermaid
flowchart LR
    subgraph Inputs ["Sensory Feedback Inputs"]
        Cap["Supercapacitor
(2.0 F / 5.0 V)"] -->|Kelvin Sense Line| ADC["12-bit ADC Channel
(V_cap Sampling)"]
        Light["BH1750 / OPT3001
Solar Lux Sensor"] -->|I²C Digital Bus| Hist["14-Sample Feature Buffer
(10 Trends + 4 Diurnal)"]
    end

    subgraph EdgeAI ["🧠 Central Edge AI Core (STM32L4 MCU)"]
        ADC --> State["Instantaneous Energy Calculation
E_stored = ½ C (V_cap² - V_min²)"]
        Hist --> NN["On-Chip TinyML MLP Predictor
(14 Inputs -> 12 ReLU -> 1 Output)
Forecasts Irradiance Ĝ(t+30m)"]
        State --> Logic{"Closed-Loop Pre-Charge & Peak Gate:
1. E_stored ≥ 12.96 J (Eq. 1)
2. Ĝ(t+30m) ≥ Peak Threshold"}
        NN --> Logic
    end

    subgraph Actuation ["Power Gating & Actuation"]
        Logic -- "PASS" --> GPIO["MCU GPIO Assert (HIGH)"]
        Logic -- "FAIL" --> Lockout["Switch Locked OFF
(Brownout Prevented)"]
        GPIO --> MOSFET["TPS22918 N-MOSFET Load Switch
(Leakage < 10 nA)"]
        MOSFET --> Rail["Switched 3.3 V Power Rail
(120 mW Switched Burst)"]
        Rail --> MOX["MOX Gas Sensor Micro-Heater
(300°C Thermal Desorption for 108 s)
Resets Chemical Baseline Drift R₀"]
    end
```

* **Hardware Placement:** Sits at the critical boundary between the analog energy buffer monitor (Kelvin-sensing ADC) and the power-gated actuator domain.
* **Standby Footprint:** Consumes `< 0.2 mW` in deep sleep (Stop-2) and `< 5 μJ` per inference execution (`< 1.2 ms` compute burst at 80 MHz).
* **Isolation Guarantee:** Separating the 1.8 V MCU core from the 3.3 V actuator rail prevents high-current heater pulses from inducing transient brownout glitches on the processor.

---

### 2. How AI is Used to Self-Calibrate Energy and Sensors

The node implements a four-stage **closed-loop self-calibration mechanism**:

#### Stage 1: Solar Harvest Energy Forecasting ($\hat{E}_{	ext{harvest}}$)
The 14-input TinyML neural network ingests 5 hours of immediate localized weather dynamics ($I_{t-10} \dots I_{t-1}$) and diurnal cyclical history from the past 4 days ($I_t^{	ext{day}-1} \dots I_t^{	ext{day}-4}$) to project incoming irradiance $\hat{G}(t + 30	ext{m})$ with an accuracy of $	ext{MAE} = 38.2	ext{ W/m}^2$.

#### Stage 2: Closed-Loop Pre-Charge Energy Assurance (Equation 1)
Before authorizing the energy-intensive $120	ext{ mW}$ thermal cycle, the controller reads terminal capacitor voltage via the Kelvin ADC line and calculates available usable Joules:
$$E_{	ext{stored}}(t) = rac{1}{2} C \left(V_{	ext{cap}}(t)^2 - V_{	ext{min}}^2ight)$$
It verifies:
$$E_{	ext{stored}}(t) \ge E_{	ext{need}} + E_{	ext{margin}}(	ext{AI})$$
where $E_{	ext{need}} = 120	ext{ mW} 	imes 108	ext{ s} = 12.96	ext{ Joules}$. If stored energy is insufficient or if approaching night/storm is predicted, the MOSFET gate is strictly locked **OFF**, mathematically guaranteeing **zero brownouts**.

#### Stage 3: Chemiresistive Baseline Drift Self-Calibration (Thermal Desorption)
Chemiresistive metal-oxide gas sensors ($SnO_2$) undergo progressive surface contamination from ambient moisture, siloxanes, and volatile poisons, causing severe baseline resistance drift ($R_0(t)$) exceeding $200+	ext{ ppm}$ of measurement error over days.
* When the AI forecasts an upcoming solar abundance peak ($\hat{G} \ge 450	ext{ W/m}^2$) **and** confirms pre-charge compliance, it commands the TPS22918 switch to heat the micro-hotplate to **$300^\circ	ext{C}$ for $108	ext{ seconds}$**.
* High thermal energy accelerates Arrhenius desorption kinetics:
  $$k_{	ext{desorb}} = A \exp\left(-rac{E_a}{k_B T_{	ext{hotplate}}}ight) \quad [T = 573.15	ext{ K}]$$
* This completely burns off poisoning adsorbates, restoring baseline resistance to nominal ($R_0 	o R_0(0)$) and resetting measurement error from $>220	ext{ ppm}$ down to $<\pm 7.5	ext{ ppm}$.

#### Stage 4: Dynamic Energy Allocation & Task Throttling (LASF)
When sunlight dips below harvesting thresholds, the AI self-calibrates the node's power budget:
* The $120	ext{ mW}$ thermal heater is safely deferred.
* Sub-milliwatt continuous environmental sensing (SHT40 Temp/RH at $<0.1	ext{ mW}$) is prioritized via dynamic Least-Age-of-Information-Slack-First ($	ext{Slack} = 	ext{ASD} - 	ext{Age}$), maintaining uninterrupted telemetry.

---

## 🔄 Decision Logic & Task Scheduling Flowchart

The system runs a **discrete-time scheduling loop** ($T_{\text{adapt}} = 30\text{ mins}$) arbitrating between lightweight continuous sensing and heavy thermal calibration:

```mermaid
flowchart TD
    Start(["⏰ Slot Wakeup (Every 30 Minutes)"]) --> SampleHarvest["Measure Harvested Solar Energy & Update Capacitor SoC"]
    SampleHarvest --> Predict["Run On-Chip NN Solar Predictor\n(Forecast Irradiance for Next Slot)"]
    Predict --> UpdateAoI["Increment Age-of-Information (AoI)\nfor All Tasks"]
    UpdateAoI --> FilterDue{"Are any tasks due?\n(AoI >= MTA)"}

    FilterDue -- No --> Sleep(["💤 Enter Deep Sleep (0.2 mW)"])
    FilterDue -- Yes --> SortTasks["Calculate Slack: ASD_i - A_i\nSort Due Tasks by Least Slack (LASF)"]

    SortTasks --> SelectTask["Pick Highest Priority Task"]
    SelectTask --> CheckPrecharge{"Equation 1 Check:\nIs E_stored >= E_task?"}

    CheckPrecharge -- No --> DeferEnergy["❌ Defer Task: Insufficient Energy\nLog Event: deferred:low_energy"]
    CheckPrecharge -- Yes --> CheckOpportunistic{"Is Task Opportunistic\n(Heater Calibration)?"}

    CheckOpportunistic -- No --> ExecuteTask["⚡ Fire Task (e.g., Cold Sensing)\nReset Task AoI to 0\nDeduct Energy from Capacitor"]
    
    CheckOpportunistic -- Yes --> CheckPeakForecast{"Is Forecast Irradiance >= Threshold\n(Upcoming Solar Peak)?"}
    
    CheckPeakForecast -- No --> DeferPeak["⏳ Defer Task: Waiting for Peak\nLog Event: deferred:waiting_for_peak"]
    CheckPeakForecast -- Yes --> FireHeater["🔥 Close MOSFET Switch\nExecute 120 mW MOX Calibration\nReset Calibration AoI to 0\nDeduct 12.96 J from Capacitor"]

    ExecuteTask --> CheckMore{"More Ready Tasks in Slot?"}
    DeferEnergy --> CheckMore
    DeferPeak --> CheckMore
    FireHeater --> CheckMore

    CheckMore -- Yes --> SelectTask
    CheckMore -- No --> Sleep
```

---

## 🔬 Sensor Suite & Subsystem Specifications

| # | Sensor Subsystem | Model / Type | Target Parameters | Power Profile | Placement & Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | **MOX Gas Sensor** | SGP40 / BME688 | $CO_2$ equiv, TVOCs | **$120\text{ mW}$ Heater**<br>$5\text{ mW}$ Cold Read | Exposed to ambient airflow; micro-hotplate burns off surface drift and restores baseline accuracy. |
| **2** | **Temp & Humidity** | SHT40 / SHTC3 | Temperature, $\% \text{RH}$ | **$< 0.10\text{ mW}$** | Isolated in airflow channel; dynamic cross-sensitivity compensation for humidity-dependent gas resistance. |
| **3** | **Solar Light / Flux** | OPT3001 / Photodiode | Irradiance ($W/m^2$), Lux | **$< 0.05\text{ mW}$** | Top surface co-located with PV cell; samples 30-min solar irradiance inputs for the neural predictor. |
| **4** | **Capacitor Monitor** | Internal MCU ADC | Voltage $V_{\text{cap}}$ ($2.2\text{V} - 5.0\text{V}$) | **$< 0.01\text{ mW}$** | Direct Kelvin-sensing connection across supercapacitor terminals to enforce Equation 1 safety gating. |
| **5** | **Radio Transceiver** | BLE / Sub-GHz LoRa | Telemetry & Alerts | **$\sim 30\text{ mW}$ (TX burst)** | Architecture-ready uplink for aggregated environmental and node health metrics. |

---

## ⚡ The Peak-to-Average Power Paradox

$$\text{Peak-to-Average Ratio} = \frac{\text{Peak Heater Power (120 mW)}}{\text{Average Continuous Draw (0.5 mW)}} = \mathbf{240\times}$$

* **Continuous Average Budget:** $\approx 0.45 - 0.55\text{ mW}$ (MCU deep sleep at $0.2\text{ mW}$, intermittent sensing at $5\text{ mW}$, and amortized daily calibration).
* **Instantaneous Heater Pulse:** **$120\text{ mW}$ for $1.8\text{ minutes}$** ($12.96\text{ Joules}$).
* **Why Fixed Timers Fail:** If a fixed $24\text{h}$ timer triggers the heater during cloud cover or twilight, the supercapacitor discharges past $V_{\text{min}}$ ($2.2\text{V}$), plunging the node into an unrecoverable **brownout reboot**.

---

## 📐 Mathematical Formulation

### 1. Supercapacitor Usable Energy Buffer
The usable energy $E_{\text{usable}}$ stored between operational maximum $V_{\text{max}}$ and brownout cutoff $V_{\text{min}}$:
$$E_{\text{usable}} = \frac{1}{2} C \left(V_{\text{max}}^2 - V_{\text{min}}^2\right)$$
For $C = 2.0\text{ F}$, $V_{\text{max}} = 5.0\text{ V}$, and $V_{\text{min}} = 2.2\text{ V}$:
$$E_{\text{usable}} = \frac{1}{2} (2.0) \left(5.0^2 - 2.2^2\right) = 25.0 - 4.84 = \mathbf{20.16\text{ Joules}}$$

### 2. Pre-Charge Assurance Check (Equation 1)
Before actuating any high-power task $i$, the controller evaluates:
$$E_{\text{stored}}(t) \ge E_{\text{need}, i} + E_{\text{margin}}$$
where $E_{\text{need}, i} = P_i \times D_i$. For the MOX heater ($120\text{ mW} \times 108\text{ s} = 12.96\text{ J}$), execution is strictly prohibited unless $E_{\text{stored}} \ge 12.96\text{ J}$.

### 3. Least-Age-of-Information-Slack-First (LASF) Scheduling
Dynamic slack $S_i(t)$ represents the urgency before data freshness expires:
$$S_i(t) = \text{ASD}_i - A_i(t)$$
$$\text{ASD}_i = U_l \cdot \text{MTA}_i - C_i$$
* $A_i(t)$: Current Age of Information (elapsed time since last execution).
* $\text{MTA}_i$: Maximum Tolerable Age of Information.
* $C_i$: Worst-case execution duration.
* $U_l$: Utilization bound factor.
Lower slack translates to higher dispatch priority among due tasks.

### 4. On-Chip Neural Network Predictor (TinyML)
* **Architecture:** Multi-Layer Perceptron (14 inputs $\to$ 12 ReLU hidden units $\to$ 1 linear output).
* **Input Feature Vector $\mathbf{x}_t \in \mathbb{R}^{14}$:**
  $$\mathbf{x}_t = \left[ I_{t-10}, I_{t-9}, \dots, I_{t-1}, I_{t}^{\text{day}-1}, I_{t}^{\text{day}-2}, I_{t}^{\text{day}-3}, I_{t}^{\text{day}-4} \right]$$
  Combining **immediate 5-hour weather trends** with **diurnal historical cycles**.

---

## 🧪 Environmental Test Scenarios

The simulator includes **6 built-in deployment presets** accessible with 1 click:

| Preset Scenario | Solar Flux ($W/m^2$) | Cloud Variability | Capacitor | Benchmark Focus |
| :--- | :---: | :---: | :---: | :--- |
| **☀️ 1. High-Desert** | $1100$ | $0.05$ (Clear) | $2.0\text{ F}$ | Ultra-fast solar charging (~2.1h to full); nominal noon calibration. |
| **⛈️ 2. Monsoon Storms** | $750$ | $0.85$ (Violent) | $0.8\text{ F}$ | **Stress Test:** Naive timer crashes 4–7 times; adaptive design maintains **0 brownouts**. |
| **❄️ 3. Nordic Winter** | $420$ | $0.30$ (Diffused) | $2.2\text{ F}$ | Extreme energy scarcity; LASF preserves sensing while deferring calibration safely. |
| **🏙️ 4. Urban Canyon** | $750$ | $0.60$ (Step-like) | $1.5\text{ F}$ | Tests neural memory against sharp, recurring morning & evening building shadows. |
| **🌱 5. Greenhouse** | $950$ | $0.20$ (Humid) | $3.0\text{ F}$ | High duty-cycle calibration (every 12h) under aggressive $140\text{ mW}$ load. |
| **🪟 6. Indoor Window** | $280$ | $0.15$ (Low light) | $2.0\text{ F}$ | Sub-milliwatt micro-harvesting survival with throttled actuation. |

---

## 📊 Performance Comparison: Our Design vs. Naive Baseline

| Metric | Traditional Fixed-Timer | Adaptive Predictive Architecture (This Work) |
| :--- | :---: | :---: |
| **Brownout Crashes (Storms)** | **4 to 7 Crashes** | **0 Crashes (Mathematically Guaranteed)** |
| **Heater Activation Policy** | Blind Periodic Clock ($24\text{h}$) | Opportunistic Peak-Forecast Gating |
| **Energy Awareness** | None (Executes regardless of SoC) | Closed-Loop Pre-Charge Verification (Eq. 1) |
| **Task Prioritization** | FIFO / Static Priority | Least-Age-of-Information-Slack-First (LASF) |
| **Predictor Engine** | None / Static EWMA | 14-Input Diurnal-Trend Neural Network |
| **Sensor Measurement Drift** | Prone to complete outage resets | Stable, Continuous Baseline Correction |

---

## 🚀 Installation & Quickstart

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13
* Git

### 1. Clone the Repository
```bash
git clone https://github.com/sathyaseelan2006/Batteryless-Environmental-Sensor-Simulation.git
cd Batteryless-Environmental-Sensor-Simulation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Simulation App
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`** (or port specified in terminal).

---

## 📂 Repository Structure

```
Batteryless-Environmental-Sensor-Simulation/
├── app.py                         # Interactive Streamlit dashboard & analytics UI
├── sensor_sim.py                  # Standalone physical simulation engine & TinyML model
├── requirements.txt               # Project dependencies (streamlit, scikit-learn, plotly, etc.)
├── architecture_reference.png     # High-resolution hardware architecture schematic
├── batteryless_node_3d.html       # Embedded interactive 3D digital-twin visualizer
├── batteryless_simulation.js      # Simulation-to-3D bridge script
├── solar_panel_fbx.glb            # 3D glTF model of harvesting hardware
├── BatterylessNodeUnity/           # Unity 3D demonstration project & scripts
│   ├── Assets/                    # Unity C# controller & orbit scripts
│   ├── Packages/                  # Unity package manifest
│   └── ProjectSettings/           # Unity version configuration
└── README.md                      # Comprehensive project documentation
```

---

## 📜 Citation & Attribution

If you utilize this simulation engine, scheduling formulations, or architecture models in academic research or patent references, please cite:

```bibtex
@misc{batteryless_sensor_sim_2026,
  author = {Sathyaseelan, K, Sasikumar S , NandhaKumar S},
  title = {Adaptive Predictive Energy-Orchestrated Batteryless Environmental Sensor Node Simulation},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/sathyaseelan2006/Batteryless-Environmental-Sensor-Simulation}}
}
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
