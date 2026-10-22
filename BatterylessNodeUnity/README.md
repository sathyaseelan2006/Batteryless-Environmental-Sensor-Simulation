# Batteryless Sensor Node · Unity 3D Walkthrough

An interactive, explorable Unity scene for the batteryless solar-powered environmental sensor architecture. The scene is generated inside Unity from primitives and labels, so it needs no downloaded models or external packages.

## Open and build the scene

1. Open `BatterylessNodeUnity` in Unity Editor 6 (6000.0 or newer).
2. In the Unity menu, choose **Batteryless Node → Build Interactive Demo Scene**.
3. Press **Play**. The saved scene is `Assets/Scenes/BatterylessNodeDemo.unity`.

The Editor is not installed in the current environment, so the scene has been provided as a native Unity scene builder and must be generated once in the Editor.

## Explore

- Drag in the Game view to orbit; use the mouse wheel to zoom.
- The scene rotates slowly on its own. Pause energy flow or stop orbit with the overlay buttons.
- Adjust sunlight and capacitor charge in the overlay. The MOX heater energy packet appears only when the simulated capacitor is at least 50% charged and irradiance is at least 360 W/m². Lower charge or sunlight to observe the pre-charge gate defer calibration.
- Animated packets trace PV → MPPT harvester → supercapacitor → regulated rails. Separate paths show always-on sensing, MCU control, heater switching, capacitor feedback, and wireless transmission.

Component geometry, wiring routes, and trigger thresholds are illustrative system-architecture visuals, not a PCB design or validated electrical model. The companion Python simulator remains the source for the project's slot-based quantitative simulation.
