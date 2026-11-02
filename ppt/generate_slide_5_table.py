import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs('ppt/generated_images', exist_ok=True)

def generate_slide_5_table():
    fig, ax = plt.subplots(figsize=(14.0, 7.8), dpi=200)
    ax.axis('off')
    
    headers = ["Paper", "Title", "Authors", "Key Features / Discussion", "Limitations"]
    data = [
        [
            "1",
            "Energy-Harvesting Batteryless IoT:\nChallenges and Directions",
            "S. Sudevalayam et al.\n(2021)",
            "Comprehensive review of ambient solar, RF,\nand thermal harvesting architectures with\nsupercapacitor storage for intermittent nodes.",
            "Evaluates static threshold charging;\nlacks dynamic neural prediction for\nscheduling multi-watt pulsed loads."
        ],
        [
            "2",
            "Low-Power Metal Oxide Gas Sensors:\nOperation Modes & Power Reduction",
            "N. Barsan et al.\n(2022)",
            "Investigates pulsed-temperature operation\nof MOX gas sensors for air quality & VOC\ndetection to curtail continuous power.",
            "Requires fixed-interval heating pulses\nwithout energy-state feedback, triggering\nbrownouts on batteryless buffers."
        ],
        [
            "3",
            "Age of Information in Energy\nHarvesting Sensor Networks",
            "R. Yates et al.\n(2023)",
            "Mathematical formulation of Age-of-Information\n(AoI) metrics to quantify data freshness in\nintermittent renewable monitoring nodes.",
            "Focuses on communication uplink\nwithout multi-task scheduling across\ndiverse power profiles (0.1 mW vs 120 mW)."
        ],
        [
            "4",
            "TinyML on Intermittent Systems:\nOn-Device Solar Forecasting",
            "H. Sharma et al.\n(2025)",
            "Employs ultra-compact neural networks on\nCortex-M microcontrollers to predict short-term\nsolar irradiance from historical trend features.",
            "Lacks integrated closed-loop hardware\ngating and dual-rail distribution for\nhigh-drain thermal recalibration."
        ]
    ]

    col_widths = [0.06, 0.25, 0.16, 0.28, 0.25]
    table = ax.table(cellText=data, colLabels=headers, colWidths=col_widths, cellLoc='left', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1.0, 3.4)

    header_color = '#3366cc'
    alt_color_1 = '#f0f4fa'
    alt_color_2 = '#ffffff'

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#b8cbe6')
        cell.set_linewidth(1.2)
        if row == 0:
            cell.set_text_props(weight='bold', color='white', size=11.5, ha='center', va='center')
            cell.set_facecolor(header_color)
            cell.set_height(0.12)
        else:
            cell.set_height(0.20)
            bg = alt_color_1 if row % 2 == 1 else alt_color_2
            cell.set_facecolor(bg)
            if col == 0:
                cell.set_text_props(weight='bold', color='#1a3a6c', size=12, ha='center', va='center')
            elif col == 1:
                cell.set_text_props(weight='bold', color='#111827', size=10.5, va='center')
            elif col == 2:
                cell.set_text_props(color='#1f2937', size=10, va='center')
            else:
                cell.set_text_props(color='#374151', size=9.8, va='center')

    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    output_path = 'ppt/generated_images/slide_5_table.png'
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.1)
    plt.close()
    print(f"Regenerated {output_path}")

generate_slide_5_table()
