import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('ppt/generated_images', exist_ok=True)

def generate_slide_13_rich():
    fig = plt.figure(figsize=(16.0, 7.8), dpi=200, facecolor='#0b111e')
    
    # 2-column layout matching reference slide 13
    ax1 = fig.add_axes([0.04, 0.08, 0.58, 0.84]) # Left: 3D Viewport
    ax2 = fig.add_axes([0.65, 0.08, 0.31, 0.84]) # Right: Telemetry HUD
    
    # Style 3D Viewport
    ax1.set_facecolor('#0f172a')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    
    # Border with rounded look
    border = patches.FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=1.5",
                                    facecolor='#0f1a2e', edgecolor='#1e293b', lw=2)
    ax1.add_patch(border)
    
    # Header tag
    ax1.add_patch(patches.FancyBboxPatch((4, 91), 32, 6, boxstyle="round,pad=0.5",
                                         facecolor='#16253d', edgecolor='#2563eb', lw=1.2))
    ax1.text(6, 94, "● LIVE 3D DIGITAL-TWIN SIMULATION", color='#60a5fa', fontsize=9.5, fontweight='bold', va='center')
    
    # Sun and harvest beam
    ax1.add_patch(patches.Circle((20, 78), 7, facecolor='#f59e0b', edgecolor='#fef08a', lw=2, alpha=0.9))
    ax1.text(20, 78, "☀️\nAM 1.5", color='#451a03', fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Sunlight rays down to solar panel
    for sx, ex in zip([16, 20, 24], [30, 45, 60]):
        ax1.annotate('', xy=(ex, 48), xytext=(sx, 72),
                     arrowprops=dict(arrowstyle="-|>", color='#fbbf24', lw=2, ls='--', mutation_scale=12))

    # 3D Node Enclosure (Isometric Perspective Box)
    # Bottom PCB base
    pcb = patches.Polygon([[25, 20], [75, 20], [88, 38], [38, 38]], closed=True,
                          facecolor='#064e3b', edgecolor='#10b981', lw=2.2)
    ax1.add_patch(pcb)
    ax1.text(56, 24, "Dual-Rail PCB Substrate (STM32L4 + PMIC)", color='#a7f3d0', fontsize=9, fontweight='bold')

    # Solar PV Module on top
    pv_panel = patches.Polygon([[30, 48], [70, 48], [80, 62], [40, 62]], closed=True,
                               facecolor='#1e3a8a', edgecolor='#38bdf8', lw=2.5)
    ax1.add_patch(pv_panel)
    ax1.text(55, 55, "10 cm² Monocrystalline PV Panel\n(18% Efficiency / MPPT Boost)",
             color='#ffffff', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Supercapacitor 3D cylinder representation
    cap_body = patches.Rectangle((28, 26), 18, 9, facecolor='#1d4ed8', edgecolor='#60a5fa', lw=1.5)
    ax1.add_patch(cap_body)
    ax1.text(37, 30.5, "2.0F / 5.0V\nSupercap", color='#ffffff', fontsize=8, fontweight='bold', ha='center', va='center')

    # MOX Gas Sensor Chamber (MQ-135 / SGP40)
    mox_circle = patches.Circle((72, 30), 5.5, facecolor='#b91c1c', edgecolor='#f87171', lw=1.8)
    ax1.add_patch(mox_circle)
    ax1.text(72, 30, "MOX\n120mW", color='#ffffff', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # Antenna / BLE LoRa
    ax1.plot([82, 82], [32, 46], color='#a855f7', lw=3)
    ax1.add_patch(patches.Circle((82, 47), 1.8, facecolor='#c084fc'))
    ax1.text(82, 50, "LoRa / BLE", color='#c084fc', fontsize=7.5, fontweight='bold', ha='center')

    # Controls HUD overlay inside 3D
    ax1.add_patch(patches.FancyBboxPatch((4, 4), 54, 11, boxstyle="round,pad=0.5",
                                         facecolor='#0b1324', edgecolor='#334155', lw=1.2))
    ax1.text(6, 11, "ENVIRONMENT PRESET: MONSOON STRESS (750 W/m² | Cloud Var: 0.85)",
             color='#cbd5e1', fontsize=8, fontweight='bold')
    ax1.text(6, 6.5, "PRE-CHARGE ASSURANCE: ENFORCED  |  LASF SCHEDULER: RUNNING",
             color='#34d399', fontsize=7.5)

    # -------------------------------------------------------------
    # Right Column: Telemetry & Eco Analytics Dashboard
    # -------------------------------------------------------------
    ax2.set_facecolor('#0f172a')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    
    border2 = patches.FancyBboxPatch((0, 0), 100, 100, boxstyle="round,pad=1.5",
                                     facecolor='#0f1a2e', edgecolor='#1e293b', lw=2)
    ax2.add_patch(border2)

    # Telemetry title
    ax2.text(8, 93, "01 / NODE TELEMETRY & HEALTH", color='#94a3b8', fontsize=9.5, fontweight='bold')
    ax2.text(88, 93, "ONLINE", color='#10b981', fontsize=9.5, fontweight='bold', ha='right')

    cards = [
        ("SOLAR IRRADIANCE", "850 W/m²", "#f59e0b", "Incident AM1.5 Flux"),
        ("CAPACITOR VOLTAGE", "4.65 V", "#38bdf8", "Safe SoC (2.2V - 5.0V)"),
        ("STORED ENERGY", "16.84 J", "#10b981", "Usable Buffer (>12.96 J Eq. 1)"),
        ("MOX HEATER STATE", "STANDBY (0 mW)", "#a855f7", "Power-Gated MOSFET Rail"),
        ("LASF DISPATCH QUEUE", "Cold Sensing: Ready", "#ec4899", "Dynamic Slack: 14.2 min"),
        ("BROWNOUT CRASHES", "0 CRASHES", "#34d399", "100% Guaranteed Uptime")
    ]

    y_start = 82
    for label, val, color, sub in cards:
        card_box = patches.FancyBboxPatch((6, y_start - 9.5), 88, 11.5, boxstyle="round,pad=0.8",
                                          facecolor='#090d16', edgecolor='#1e293b', lw=1.2)
        ax2.add_patch(card_box)
        ax2.text(11, y_start, label, color='#94a3b8', fontsize=8, fontweight='bold')
        ax2.text(89, y_start, val, color=color, fontsize=10.5, fontweight='bold', ha='right')
        ax2.text(11, y_start - 6, sub, color='#64748b', fontsize=7.5)
        y_start -= 14.5

    outpath = 'ppt/generated_images/slide_13_3d_output.png'
    plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='#0b111e')
    plt.close()
    print(f"Generated {outpath}")

generate_slide_13_rich()
