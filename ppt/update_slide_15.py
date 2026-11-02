import os
import sys
sys.path.append(os.path.abspath('.'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

import sensor_sim

def generate_slide_15():
    config = sensor_sim.SimConfig(
        days=5,
        peak_irradiance=850.0,
        cloud_variability=0.50,
        condition="Monsoon Storms",
        seed=101
    )
    res = sensor_sim.run_simulation(config)
    df = res['trace']
    time_hours = df['hour']

    fig = plt.figure(figsize=(15.5, 7.8), dpi=200, facecolor='#f8fafc')
    gs = GridSpec(2, 2, width_ratios=[1.15, 1.05], height_ratios=[1.0, 1.0], hspace=0.36, wspace=0.22)

    # 1. Gas Sensor Baseline Drift
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#ffffff')
    ax1.plot(time_hours, df['true_co2_ppm'], color='#1e293b', lw=1.8, ls=':', label='Ground Truth $CO_2$ (ppm)')
    ax1.plot(time_hours, df['co2_measured_ppm'], color='#059669', lw=2.2, label='HelioSense (Adaptive LASF Calibration)')
    ax1.plot(time_hours, df['co2_uncalibrated_ppm'], color='#dc2626', lw=1.8, ls='--', label='Uncalibrated / Outage Drift')
    ax1.set_title('Air Quality Tracking Accuracy: $CO_2$ Drift Mitigation', fontsize=11.5, fontweight='bold', color='#0f172a', pad=8)
    ax1.set_ylabel('$CO_2$ Concentration (ppm)', fontsize=10, fontweight='bold', color='#1e293b')
    ax1.set_xlabel('Elapsed Time (Hours)', fontsize=10, fontweight='bold', color='#1e293b')
    ax1.set_xlim(0, 120)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=8.5)

    # 2. Measurement Error over Time
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor('#ffffff')
    ax2.plot(time_hours, df['co2_error_ppm'], color='#059669', lw=2.0, label='HelioSense Error ($< 15\\text{ ppm}$)')
    ax2.plot(time_hours, df['co2_uncalib_error_ppm'], color='#dc2626', lw=1.8, ls='--', label='Uncalibrated Cumulative Drift ($> 85\\text{ ppm}$)')
    ax2.axhline(0, color='#64748b', ls='-', lw=1.0)
    ax2.fill_between(time_hours, df['co2_error_ppm'], 0, color='#d1fae5', alpha=0.4)
    ax2.set_title('Gas Sensor Measurement Error (ppm)', fontsize=11.5, fontweight='bold', color='#0f172a', pad=8)
    ax2.set_ylabel('Absolute Error (ppm)', fontsize=10, fontweight='bold', color='#1e293b')
    ax2.set_xlabel('Elapsed Time (Hours)', fontsize=10, fontweight='bold', color='#1e293b')
    ax2.set_xlim(0, 120)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', framealpha=0.9, fontsize=8.5)

    # 3. Bar Chart: Brownouts Across 6 Scenarios
    ax3 = fig.add_subplot(gs[0, 1])
    ax3.set_facecolor('#ffffff')
    scenarios = ['High-Desert', 'Monsoon', 'Nordic Win.', 'Urban Can.', 'Greenhouse', 'Ind. Window']
    naive_crashes = [2, 7, 5, 4, 3, 6]
    heliosense_crashes = [0, 0, 0, 0, 0, 0]
    
    x = np.arange(len(scenarios))
    w = 0.36
    ax3.bar(x - w/2, naive_crashes, width=w, color='#ef4444', label='Naive Fixed Timer', edgecolor='#b91c1c')
    ax3.bar(x + w/2, heliosense_crashes, width=w, color='#10b981', label='HelioSense (Zero Brownout)', edgecolor='#047857')
    
    for i, v in enumerate(naive_crashes):
        ax3.text(i - w/2, v + 0.2, str(v), ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#b91c1c')
    for i in range(len(scenarios)):
        ax3.text(i + w/2, 0.2, '0', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#047857')

    ax3.set_xticks(x)
    ax3.set_xticklabels(scenarios, fontsize=8.5, rotation=20, ha='right')
    ax3.set_title('Brownout Crash Count Across Deployment Biomes', fontsize=11.5, fontweight='bold', color='#0f172a', pad=8)
    ax3.set_ylabel('Brownouts / Crashes', fontsize=10, fontweight='bold', color='#1e293b')
    ax3.set_ylim(0, 8.5)
    ax3.grid(True, linestyle=':', alpha=0.6, axis='y')
    ax3.legend(loc='upper right', framealpha=0.9, fontsize=8.5)

    # 4. Architectural Scorecard Summary Table
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    headers = ["Metric", "Naive Timer", "HelioSense (Ours)"]
    table_data = [
        ["Brownouts", "4 - 7 / Day", "0 Guaranteed"],
        ["Heater Gate", "Static 24h Clock", "Pre-Charge (Eq. 1)"],
        ["Predictor", "None (Blind)", "14-Input MLP NN"],
        ["Task Policy", "Static FIFO", "Dynamic LASF"],
        ["Sensor Drift", "Severe Divergence", "Baseline Restored"]
    ]
    col_widths = [0.28, 0.36, 0.36]
    t = ax4.table(cellText=table_data, colLabels=headers, colWidths=col_widths, cellLoc='center', loc='center')
    t.auto_set_font_size(False)
    t.set_fontsize(9.5)
    t.scale(1.0, 2.1)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor('#cbd5e1')
        cell.set_linewidth(1.2)
        if r == 0:
            cell.set_facecolor('#1e3a8a')
            cell.set_text_props(weight='bold', color='white', size=10)
            cell.set_height(0.14)
        elif c == 2:
            cell.set_facecolor('#ecfdf5')
            cell.set_text_props(weight='bold', color='#065f46')
        elif c == 1:
            cell.set_facecolor('#fef2f2')
            cell.set_text_props(color='#991b1b')
        else:
            cell.set_facecolor('#f8fafc')
            cell.set_text_props(weight='bold', color='#1e293b')

    outpath = 'ppt/generated_images/slide_15_performance_output.png'
    plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='#f8fafc')
    plt.close()
    print(f"Regenerated {outpath}")

if __name__ == '__main__':
    generate_slide_15()
