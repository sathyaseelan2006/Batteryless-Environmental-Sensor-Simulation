"""
generate_architecture_diagram.py
Generates a publication-grade, ultra-high-resolution architecture diagram image (PNG)
matching the exact layout, styling, and color scheme of the project reference architecture.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def create_diagram():
    # 16:9 canvas at 300 DPI (5700 x 3000 pixels)
    fig, ax = plt.subplots(figsize=(19, 10), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Coordinate system: [0, 100] x [0, 100]
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette matching user's reference diagram
    BOX_BG = '#f0f9ff'          # Light cyan-blue fill
    BOX_BORDER = '#0284c7'      # Vibrant azure border
    TITLE_COLOR = '#0369a1'     # Deep cyan-blue text
    SUB_COLOR = '#334155'       # Dark slate text
    
    MCU_BG = '#e0f2fe'          # Highlighted MCU fill
    MCU_BORDER = '#0284c7'
    
    HOT_BG = '#fff7ed'          # Warm amber for heater
    HOT_BORDER = '#ea580c'
    HOT_TITLE = '#c2410c'

    LINE_POWER = '#0284c7'      # Blue power lines
    LINE_CONTROL = '#16a34a'    # Green GPIO control line
    LINE_DATA = '#9333ea'       # Purple data line
    LINE_ADC = '#ca8a04'        # Gold Kelvin sense line

    def draw_box(x, y, w, h, title, sub, bg=BOX_BG, border=BOX_BORDER, t_col=TITLE_COLOR, s_col=SUB_COLOR, title_size=10.5, sub_size=8.5):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.2,rounding_size=1.2",
                             linewidth=2.0, edgecolor=border, facecolor=bg)
        ax.add_patch(box)
        
        # Title
        ax.text(x + w/2, y + h*0.65, title,
                ha='center', va='center', fontsize=title_size, fontweight='bold', color=t_col,
                fontfamily='sans-serif')
        
        # Subtitle
        ax.text(x + w/2, y + h*0.32, sub,
                ha='center', va='center', fontsize=sub_size, fontweight='normal', color=s_col,
                fontfamily='sans-serif')
        return (x, y, w, h)

    # =========================================================================
    # 1. MAIN LINEAR HARVESTING CHAIN (Left to Center)
    # =========================================================================
    draw_box(2.5, 47, 9.5, 11, "Sunlight", "0 – 1200 W/m²")
    draw_box(15.0, 47, 9.5, 11, "Solar PV", "10 cm² panel")
    draw_box(27.5, 46, 12.0, 13, "Energy PMIC", "TI BQ25570 MPPT\nBoost Converter")
    draw_box(42.5, 45.5, 12.0, 14, "Supercapacitor", "2.0 F / 5.0 V\n20.16 J Buffer")

    # Arrows: Sun -> PV -> PMIC -> Supercap
    ax.annotate("", xy=(15.0, 52.5), xytext=(12.0, 52.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))
    ax.annotate("", xy=(27.5, 52.5), xytext=(24.5, 52.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))
    ax.annotate("", xy=(42.5, 52.5), xytext=(39.5, 52.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))

    # =========================================================================
    # 2. DUAL POWER REGULATION (Branching from Supercapacitor)
    # =========================================================================
    # Upper Branch: 1.8V Low-Iq LDO
    draw_box(57.5, 68, 11.5, 11, "1.8V Low-Iq LDO", "Always-On Rail")
    # Lower Branch: 3.3V Buck / LDO
    draw_box(57.5, 26, 11.5, 11, "3.3V Buck / LDO", "Actuator Rail")

    # Routing lines from Supercap -> Regulators
    ax.plot([54.5, 56.0, 56.0], [52.5, 52.5, 73.5], color='#1e293b', lw=2.0)
    ax.annotate("", xy=(57.5, 73.5), xytext=(56.0, 73.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))

    ax.plot([54.5, 56.0, 56.0], [52.5, 52.5, 31.5], color='#1e293b', lw=2.0)
    ax.annotate("", xy=(57.5, 31.5), xytext=(56.0, 31.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))

    # =========================================================================
    # 3. PROCESSING CORE: MCU (Upper Center-Right)
    # =========================================================================
    draw_box(72.0, 64, 13.5, 19, "Ultra-Low-Power MCU", 
             "STM32L476RG with\nNeural Network Engine\n& LASF Scheduler",
             bg=MCU_BG, border=MCU_BORDER, title_size=10.0, sub_size=8.0)

    # 1.8V LDO -> MCU
    ax.annotate("", xy=(72.0, 73.5), xytext=(69.0, 73.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))

    # =========================================================================
    # 4. SENSORS & TELEMETRY (Right Column)
    # =========================================================================
    draw_box(89.0, 79, 9.5, 10, "Temp / Humidity", "SHT40 (I²C)")
    draw_box(89.0, 66, 9.5, 10, "Solar Light / Lux", "BH1750 (I²C)")
    draw_box(89.0, 53, 9.5, 10, "Wireless Radio", "Ra-02 LoRa / BLE\n3.3V Powered")

    # Lines from MCU -> Sensors
    ax.plot([85.5, 87.2, 87.2], [74, 74, 84], color='#1e293b', lw=1.8)
    ax.annotate("", xy=(89.0, 84), xytext=(87.2, 84),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", color='#1e293b', lw=1.8))

    ax.annotate("", xy=(89.0, 71), xytext=(85.5, 71),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", color='#1e293b', lw=1.8))

    ax.plot([85.5, 87.2, 87.2], [68, 68, 58], color='#1e293b', lw=1.8)
    ax.annotate("", xy=(89.0, 58), xytext=(87.2, 58),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", color='#1e293b', lw=1.8))

    # =========================================================================
    # 5. ACTUATION CHAIN: TPS22918 + MOX SENSOR (Lower Branch)
    # =========================================================================
    draw_box(72.5, 26, 12.5, 11, "TPS22918 Load SW", "MOSFET Gate\nLeakage < 10 nA")
    draw_box(88.0, 25, 10.5, 13, "MOX Gas Sensor", "300°C Hotplate\n120 mW Burst\n(CO₂ & VOCs)",
             bg=HOT_BG, border=HOT_BORDER, t_col=HOT_TITLE, title_size=10.0, sub_size=8.0)

    # 3.3V Buck -> TPS22918
    ax.annotate("", xy=(72.5, 31.5), xytext=(69.0, 31.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color='#1e293b', lw=2.0))

    # TPS22918 -> MOX Hotplate
    ax.annotate("", xy=(88.0, 31.5), xytext=(85.0, 31.5),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color=HOT_BORDER, lw=2.2))
    ax.text(86.5, 33.2, "120 mW", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=HOT_TITLE)

    # =========================================================================
    # 6. CRITICAL SIGNAL CORRECTIONS (The 3 Reviewer-Proof Lines)
    # =========================================================================

    # [CORRECTION 1]: GPIO Control Line (MCU -> TPS22918 Load SW)
    ax.plot([78.5, 78.5], [64.0, 37.0], color=LINE_CONTROL, lw=2.0, linestyle='--')
    ax.annotate("", xy=(78.5, 37.0), xytext=(78.5, 40.0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color=LINE_CONTROL, lw=2.0))
    ax.text(77.5, 50.5, "GPIO Gate Control\n(LASF Solar Peak Gate)", ha='right', va='center',
            fontsize=8.0, fontweight='bold', color=LINE_CONTROL,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0fdf4", edgecolor=LINE_CONTROL, lw=1))

    # [CORRECTION 2]: Gas Sensor Data Readout (MOX -> MCU)
    ax.plot([93.5, 93.5, 85.5], [38.0, 48.0, 48.0], color=LINE_DATA, lw=2.0, linestyle='--')
    ax.plot([85.5, 80.0, 80.0], [48.0, 48.0, 64.0], color=LINE_DATA, lw=2.0, linestyle='--')
    ax.annotate("", xy=(80.0, 64.0), xytext=(80.0, 61.0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color=LINE_DATA, lw=2.0))
    ax.text(87.0, 46.5, "Gas Readout (Analog / I²C)", ha='center', va='top',
            fontsize=8.0, fontweight='bold', color=LINE_DATA,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#faf5ff", edgecolor=LINE_DATA, lw=1))

    # [CORRECTION 3]: 3.3V Power Line to Ra-02 Wireless Radio
    ax.plot([63.25, 63.25, 87.0], [26.0, 18.0, 18.0], color=LINE_POWER, lw=1.8)
    ax.plot([87.0, 87.0, 89.0], [18.0, 55.0, 55.0], color=LINE_POWER, lw=1.8)
    ax.annotate("", xy=(89.0, 55.0), xytext=(87.0, 55.0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", color=LINE_POWER, lw=1.8))
    ax.text(75.0, 16.5, "3.3V Power Bus to Radio (LoRa 40 mA TX)", ha='center', va='top',
            fontsize=8.0, fontweight='bold', color=LINE_POWER,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0f9ff", edgecolor=LINE_POWER, lw=1))

    # [KELVIN SENSE LINE]: Supercapacitor -> MCU 12-bit ADC
    ax.plot([48.5, 48.5, 74.0, 74.0], [59.5, 88.5, 88.5, 83.0], color=LINE_ADC, lw=2.0, linestyle='--')
    ax.annotate("", xy=(74.0, 83.0), xytext=(74.0, 85.0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color=LINE_ADC, lw=2.0))
    ax.text(61.0, 90.0, "V_cap Kelvin Sense (12-bit ADC Feedback for Eq. 1 Pre-Charge Assurance)",
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=LINE_ADC,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#fefce8", edgecolor=LINE_ADC, lw=1))

    # =========================================================================
    # 7. TITLES & HEADER
    # =========================================================================
    ax.text(50, 98.0, "ADAPTIVE PREDICTIVE ENERGY-ORCHESTRATED BATTERYLESS SENSOR NODE",
            ha='center', va='center', fontsize=14.5, fontweight='bold', color='#0f172a', fontfamily='sans-serif')
    ax.text(50, 95.0, "Complete System Hardware Architecture: Power Routing, Dual-Rail Regulation & Closed-Loop Control",
            ha='center', va='center', fontsize=10.0, fontweight='normal', color='#475569', fontfamily='sans-serif')

    # =========================================================================
    # 8. LEGEND BOX AT BOTTOM
    # =========================================================================
    leg_box = FancyBboxPatch((14.0, 3.5), 72.0, 5.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                             linewidth=1.2, edgecolor='#cbd5e1', facecolor='#f8fafc')
    ax.add_patch(leg_box)

    leg_y = 6.0
    # Continuous Power
    ax.plot([16.5, 19.5], [leg_y, leg_y], color='#1e293b', lw=2.0)
    ax.text(20.5, leg_y, "Power Distribution (DC Rails)", va='center', fontsize=8.0, color='#1e293b', fontweight='bold')

    # Switched Heater Rail
    ax.plot([38.5, 41.5], [leg_y, leg_y], color=HOT_BORDER, lw=2.2)
    ax.text(42.5, leg_y, "Switched Hotplate Rail (120 mW)", va='center', fontsize=8.0, color=HOT_TITLE, fontweight='bold')

    # Kelvin Sense
    ax.plot([59.0, 62.0], [leg_y, leg_y], color=LINE_ADC, lw=2.0, linestyle='--')
    ax.text(63.0, leg_y, "12-bit ADC Kelvin Sense (Eq. 1)", va='center', fontsize=8.0, color=LINE_ADC, fontweight='bold')

    # GPIO Control
    ax.plot([77.5, 80.5], [leg_y, leg_y], color=LINE_CONTROL, lw=2.0, linestyle='--')
    ax.text(81.5, leg_y, "GPIO Gate Control (LASF)", va='center', fontsize=8.0, color=LINE_CONTROL, fontweight='bold')

    plt.tight_layout()
    output_path = "system_architecture_diagram.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"High-resolution diagram successfully saved to: {output_path}")

if __name__ == "__main__":
    create_diagram()
