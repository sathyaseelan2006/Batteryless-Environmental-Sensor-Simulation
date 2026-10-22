using System.Collections.Generic;
using UnityEngine;

/// <summary>Runtime controls and animated energy packets for the generated demo scene.</summary>
public class BatterylessNodeDemo : MonoBehaviour
{
    [System.Serializable] public class Flow
    {
        public Transform from, to;
        public Color color;
        public float speed = 0.48f;
        public bool gated;
        [HideInInspector] public Transform packet;
    }

    public List<Flow> flows = new List<Flow>();
    public Transform rotatingRoot;
    public float sunlight = 720f;
    [Range(0, 100)] public float charge = 68f;
    public bool playing = true;
    public bool rotate = true;
    float clock;
    Material packetMaterial;

    public bool HeaterReady => charge >= 50f && sunlight >= 360f;

    void Start()
    {
        packetMaterial = new Material(Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard"));
        foreach (var flow in flows)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            go.name = "Animated energy packet";
            go.transform.SetParent(transform);
            go.transform.localScale = Vector3.one * .13f;
            var col = go.GetComponent<Collider>(); if (col) Destroy(col);
            var mat = new Material(packetMaterial); mat.color = flow.color;
            mat.EnableKeyword("_EMISSION"); mat.SetColor("_EmissionColor", flow.color * 1.8f);
            go.GetComponent<Renderer>().material = mat;
            flow.packet = go.transform;
        }
    }

    void Update()
    {
        if (playing) clock += Time.deltaTime;
        if (rotate && rotatingRoot && !Input.GetMouseButton(0))
            rotatingRoot.Rotate(Vector3.up, 3.4f * Time.deltaTime, Space.World);
        foreach (var f in flows)
        {
            if (!f.packet || !f.from || !f.to) continue;
            bool enabled = !f.gated || HeaterReady;
            f.packet.gameObject.SetActive(enabled);
            if (!enabled) continue;
            float phase = Mathf.Repeat(clock * f.speed + FlowOffset(f), 1f);
            f.packet.position = Vector3.Lerp(f.from.position, f.to.position, phase) + Vector3.up * (.18f + Mathf.Sin(phase * Mathf.PI) * .2f);
        }
    }

    static float FlowOffset(Flow f) => (Mathf.Abs(f.from.GetInstanceID() * 17 + f.to.GetInstanceID() * 31) % 1000) / 1000f;

    void OnGUI()
    {
        const int width = 310;
        GUI.Box(new Rect(18, 18, width, 260), "BATTERYLESS NODE  |  LIVE MODEL");
        GUILayout.BeginArea(new Rect(32, 52, width - 28, 220));
        GUILayout.Label("Solar irradiance   " + Mathf.RoundToInt(sunlight) + " W/m²");
        sunlight = GUILayout.HorizontalSlider(sunlight, 0, 1100);
        GUILayout.Space(7);
        GUILayout.Label("Supercapacitor    " + Mathf.RoundToInt(charge) + "%   ·   " + Voltage.ToString("0.00") + " V");
        charge = GUILayout.HorizontalSlider(charge, 0, 100);
        GUILayout.Space(8);
        GUI.color = HeaterReady ? new Color(.5f, 1f, .72f) : new Color(1f, .72f, .48f);
        GUILayout.Label(HeaterReady ? "●  ENERGY WINDOW AVAILABLE" : "●  CALIBRATION DEFERRED — PRE-CHARGE GATE");
        GUI.color = Color.white;
        GUILayout.Label("Harvester  " + (sunlight * .001f * .18f * 1000f).ToString("0.0") + " mW   |   MOX heater 120 mW");
        GUILayout.Space(8);
        GUILayout.BeginHorizontal();
        if (GUILayout.Button(playing ? "Ⅱ  Pause flow" : "▶  Play flow")) playing = !playing;
        if (GUILayout.Button(rotate ? "⟳  Stop orbit" : "⟳  Orbit")) rotate = !rotate;
        GUILayout.EndHorizontal();
        GUILayout.Label("Drag to orbit · scroll to zoom");
        GUILayout.EndArea();
    }

    float Voltage => Mathf.Sqrt(2.2f * 2.2f + charge / 100f * (25f - 2.2f * 2.2f));
}
