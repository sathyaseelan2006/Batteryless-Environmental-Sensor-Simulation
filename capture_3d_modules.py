import asyncio
import os
import zendriver as zd
from PIL import Image

async def capture_all_modules():
    c = zd.Config()
    c.add_argument('--window-size=1920,1080')
    c.add_argument('--force-device-scale-factor=1.5')
    c.add_argument('--hide-scrollbars')
    browser = await zd.start(headless=True, config=c)
    
    file_path = os.path.abspath('batteryless_node_3d.html').replace('\\', '/')
    url = f'file:///{file_path}'
    page = await browser.get(url)
    await page.sleep(2)
    
    os.makedirs('modules', exist_ok=True)
    os.makedirs('ppt/generated_images', exist_ok=True)
    
    # 5 Modules Configuration
    modules_config = [
        {
            "id": 1,
            "title": "Module 1: Solar Energy Harvesting and Storage Module",
            "base_name": "module_1_solar_harvesting_storage.png",
            "full_name": "module_1_solar_harvesting_storage_3d_full.png",
            "viewport_name": "module_1_solar_harvesting_storage_3d_viewport.png",
            "step_index": 0,
            "component": "pv",
            "sun": 920,
            "charge": 88
        },
        {
            "id": 2,
            "title": "Module 2: Environmental Sensing Module",
            "base_name": "module_2_environmental_sensing.png",
            "full_name": "module_2_environmental_sensing_3d_full.png",
            "viewport_name": "module_2_environmental_sensing_3d_viewport.png",
            "step_index": 1,
            "component": "th",
            "sun": 680,
            "charge": 76
        },
        {
            "id": 3,
            "title": "Module 3: Predictive Energy Forecasting Module",
            "base_name": "module_3_predictive_energy_forecasting.png",
            "full_name": "module_3_predictive_energy_forecasting_3d_full.png",
            "viewport_name": "module_3_predictive_energy_forecasting_3d_viewport.png",
            "step_index": 2,
            "component": "mcu",
            "sun": 740,
            "charge": 82
        },
        {
            "id": 4,
            "title": "Module 4: Adaptive Task Scheduling Module",
            "base_name": "module_4_adaptive_task_scheduling.png",
            "full_name": "module_4_adaptive_task_scheduling_3d_full.png",
            "viewport_name": "module_4_adaptive_task_scheduling_3d_viewport.png",
            "step_index": 3,
            "component": "mcu",
            "sun": 520,
            "charge": 68
        },
        {
            "id": 5,
            "title": "Module 5: Energy Management and Self-Calibration Module",
            "base_name": "module_5_energy_management_self_calibration.png",
            "full_name": "module_5_energy_management_self_calibration_3d_full.png",
            "viewport_name": "module_5_energy_management_self_calibration_3d_viewport.png",
            "step_index": 4,
            "component": "mox",
            "sun": 950,
            "charge": 96
        }
    ]
    
    print("Capturing 3D model screenshots...")
    
    for mod in modules_config:
        print(f"-> Processing {mod['title']}...")
        
        # Trigger UI state
        js_cmd = f"""
        (() => {{
            const steps = document.querySelectorAll('.step');
            if (steps.length > {mod['step_index']}) {{
                steps[{mod['step_index']}].click();
            }}
            const comp = document.querySelector('#componentSelect');
            if (comp) {{
                comp.value = '{mod['component']}';
                comp.dispatchEvent(new Event('change'));
            }}
            const sunSlider = document.querySelector('#sun');
            if (sunSlider) {{
                sunSlider.value = {mod['sun']};
                sunSlider.dispatchEvent(new Event('input'));
            }}
            const chargeSlider = document.querySelector('#charge');
            if (chargeSlider) {{
                chargeSlider.value = {mod['charge']};
                chargeSlider.dispatchEvent(new Event('input'));
            }}
        }})();
        """
        await page.evaluate(js_cmd)
        await page.sleep(1.2)
        
        # 1. Capture Full Viewport (includes 3D Model + Telemetry Panel + Active Step HUD)
        full_dest = os.path.join('modules', mod['full_name'])
        await page.save_screenshot(full_dest)
        
        # 2. Crop 3D Stage Viewport (Isometric 3D exploded assembly, glowing nodes, labels, sun rays)
        im = Image.open(full_dest)
        w, h = im.size
        # The stage occupies [0, 72] to [w - 315, h - 48]
        top_offset = 72
        bottom_offset = 48
        side_panel_width = int(315 * (w / 1920))
        stage_crop = im.crop((0, top_offset, w - side_panel_width, h - bottom_offset))
        
        viewport_dest = os.path.join('modules', mod['viewport_name'])
        stage_crop.save(viewport_dest, quality=95)
        
        # Also save the standard base name (which is what markdown and PPT refer to directly)
        base_dest = os.path.join('modules', mod['base_name'])
        im.save(base_dest, quality=95)
        
        # Copy to ppt/generated_images
        im.save(os.path.join('ppt/generated_images', mod['full_name']))
        im.save(os.path.join('ppt/generated_images', mod['base_name']))
        stage_crop.save(os.path.join('ppt/generated_images', mod['viewport_name']))
        
        print(f"   Saved: {mod['base_name']}, {mod['full_name']}, {mod['viewport_name']}")
        
    # Master System Overview Capture
    print("-> Processing Master 3D Architecture Overview...")
    js_overview = """
    (() => {
        const comp = document.querySelector('#componentSelect');
        if (comp) {
            comp.value = 'mcu';
            comp.dispatchEvent(new Event('change'));
        }
        const sunSlider = document.querySelector('#sun');
        if (sunSlider) {
            sunSlider.value = 800;
            sunSlider.dispatchEvent(new Event('input'));
        }
        const chargeSlider = document.querySelector('#charge');
        if (chargeSlider) {
            chargeSlider.value = 85;
            chargeSlider.dispatchEvent(new Event('input'));
        }
    })();
    """
    await page.evaluate(js_overview)
    await page.sleep(1.2)
    
    overview_full = os.path.join('modules', 'all_modules_overview.png')
    await page.save_screenshot(overview_full)
    
    im_ov = Image.open(overview_full)
    w, h = im_ov.size
    side_panel_width = int(315 * (w / 1920))
    crop_ov = im_ov.crop((0, 72, w - side_panel_width, h - 48))
    crop_ov.save(os.path.join('modules', 'all_modules_3d_viewport.png'), quality=95)
    
    # Copy to PPT folder
    im_ov.save(os.path.join('ppt/generated_images', 'all_modules_overview.png'))
    crop_ov.save(os.path.join('ppt/generated_images', 'all_modules_3d_viewport.png'))
    
    await browser.stop()
    print("All 3D captures completed successfully!")

if __name__ == '__main__':
    asyncio.run(capture_all_modules())
