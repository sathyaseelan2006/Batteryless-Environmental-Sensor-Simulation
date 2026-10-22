using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

/// <summary>Creates a complete interactive architecture scene from Unity's menu.</summary>
public static class BatterylessNodeSceneBuilder
{
    static readonly Color Navy = new Color(.035f, .07f, .12f);
    static readonly Color Amber = new Color(1f, .68f, .24f);
    static readonly Color Blue = new Color(.23f, .62f, 1f);
    static readonly Color Mint = new Color(.24f, .92f, .62f);
    static readonly Color Violet = new Color(.69f, .52f, 1f);
    static readonly Color Pink = new Color(1f, .4f, .56f);
    static Transform root;
    static BatterylessNodeDemo demo;
    static Dictionary<string, Transform> nodes;

    [MenuItem("Batteryless Node/Build Interactive Demo Scene")]
    public static void Build()
    {
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        root = new GameObject("Batteryless Sensor Node · Exploded Architecture").transform;
        nodes = new Dictionary<string, Transform>();
        var rig = new GameObject("Orbit Camera Rig");
        var cam = rig.AddComponent<Camera>();
        cam.tag = "MainCamera";
        rig.transform.position = new Vector3(0, 11, -19);
        rig.transform.rotation = Quaternion.LookRotation(new Vector3(0, -7, 2));
        cam.clearFlags = CameraClearFlags.SolidColor; cam.backgroundColor = Navy;
        cam.fieldOfView = 47; cam.nearClipPlane = .1f; cam.farClipPlane = 150;
        cam.gameObject.AddComponent<AudioListener>();
        var orbit = rig.AddComponent<BatterylessNodeOrbit>();
        orbit.target = root;
        var sun = new GameObject("Sun · soft key light").AddComponent<Light>();
        sun.type = LightType.Directional; sun.intensity = 1.4f; sun.color = new Color(1f,.87f,.68f);
        sun.transform.rotation = Quaternion.Euler(48,-28,0);
        RenderSettings.ambientLight = new Color(.35f,.42f,.55f);

        Cube("PCB visualization", new Vector3(0,-.28f,0), new Vector3(15.8f,.18f,9.2f), new Color(.055f,.12f,.17f), root);
        Cube("Board edge", new Vector3(0,-.39f,0), new Vector3(15.9f,.12f,9.3f), new Color(.11f,.2f,.27f), root);
        Label("BATTERYLESS ENVIRONMENTAL SENSOR NODE", new Vector3(0,.04f,4.38f), 0.28f, Color.white);
        Label("Solar harvesting  ·  predictive energy management  ·  adaptive sensing", new Vector3(0,.04f,4.02f), .14f, new Color(.61f,.73f,.86f));

        nodes["PV"] = BoxNode("SOLAR PV", "10 cm² · photovoltaic panel", new Vector3(-5.5f,.12f,1.75f), new Vector3(2.65f,.22f,2.0f), new Color(.07f,.29f,.41f), Amber);
        PanelCells(nodes["PV"]);
        nodes["PMIC"] = BoxNode("ENERGY PMIC", "MPPT · boost harvester", new Vector3(-2.55f,.1f,1.75f), new Vector3(1.8f,.56f,1.45f), new Color(.13f,.2f,.27f), Amber);
        nodes["CAP"] = CylinderNode("SUPERCAPACITOR", "2.0 F · 2.2–5.0 V", new Vector3(.05f,.28f,1.75f), new Vector3(1.15f,.8f,1.15f), Blue);
        nodes["LDO18"] = BoxNode("BUCK / LDO 1", "regulated 1.8 V", new Vector3(2.42f,.08f,2.85f), new Vector3(1.45f,.48f,.85f), new Color(.12f,.2f,.34f), Blue);
        nodes["LDO33"] = BoxNode("BUCK / LDO 2", "regulated 3.3 V", new Vector3(2.42f,.08f,.65f), new Vector3(1.45f,.48f,.85f), new Color(.12f,.2f,.34f), Blue);
        nodes["MCU"] = BoxNode("ULP MCU · ARM CORTEX-M", "14-input neural solar forecaster", new Vector3(-.05f,.13f,-.55f), new Vector3(3.2f,.72f,1.65f), new Color(.17f,.12f,.31f), Violet);
        Label("PRE-CHARGE GATE  ·  LASF SCHEDULER", new Vector3(-.05f,.56f,-.65f), .13f, new Color(.83f,.75f,1f));
        nodes["SW"] = BoxNode("MOSFET LOAD SWITCH", "heater power gate", new Vector3(4.45f,.08f,.65f), new Vector3(1.55f,.48f,.85f), new Color(.1f,.26f,.22f), Mint);
        nodes["MOX"] = BoxNode("MOX GAS SENSOR", "micro-hotplate · 120 mW", new Vector3(6.45f,.1f,.65f), new Vector3(1.75f,.62f,1.15f), new Color(.28f,.19f,.13f), Mint);
        nodes["SHT"] = BoxNode("TEMP / HUMIDITY", "SHT40 · I²C · 0.1 mW", new Vector3(-3.8f,.08f,-2.5f), new Vector3(1.9f,.45f,1.05f), new Color(.12f,.25f,.23f), Mint);
        nodes["LUX"] = BoxNode("LIGHT / LUX", "photodiode · ADC", new Vector3(-.9f,.08f,-2.5f), new Vector3(1.9f,.45f,1.05f), new Color(.12f,.25f,.23f), Amber);
        nodes["RADIO"] = BoxNode("WIRELESS RADIO", "BLE / LoRa · data uplink", new Vector3(2.05f,.08f,-2.5f), new Vector3(1.9f,.45f,1.05f), new Color(.27f,.12f,.19f), Pink);
        Label("HARVEST + STORE", new Vector3(-2.7f,.06f,3.04f), .13f, Amber);
        Label("REGULATE", new Vector3(2.42f,.06f,3.55f), .13f, Blue);
        Label("ALWAYS-ON SENSOR & CONTROL BUS", new Vector3(-.15f,.03f,-3.45f), .13f, Mint);

        demo = new GameObject("Energy Flow Animation + Controls").AddComponent<BatterylessNodeDemo>();
        demo.rotatingRoot = root;
        AddFlow("PV","PMIC",Amber); AddFlow("PMIC","CAP",Amber);
        AddFlow("CAP","LDO18",Blue); AddFlow("CAP","LDO33",Blue);
        AddFlow("LDO18","MCU",Blue); AddFlow("LDO18","SHT",Mint);
        AddFlow("LDO18","LUX",Mint); AddFlow("LDO18","RADIO",Blue);
        AddFlow("LDO33","SW",Blue); AddFlow("SW","MOX",Mint,true);
        AddFlow("MCU","SW",Violet); AddFlow("CAP","MCU",Violet);
        AddFlow("MCU","RADIO",Pink);
        Save();
        Selection.activeObject = root.gameObject;
        EditorGUIUtility.PingObject(AssetDatabase.LoadAssetAtPath<SceneAsset>("Assets/Scenes/BatterylessNodeDemo.unity"));
        Debug.Log("Batteryless Sensor Node demo scene created. Press Play; drag to orbit and use the on-screen sliders.");
    }

    static void Save()
    {
        if (!AssetDatabase.IsValidFolder("Assets/Scenes")) AssetDatabase.CreateFolder("Assets", "Scenes");
        EditorSceneManager.SaveScene(SceneManager.GetActiveScene(), "Assets/Scenes/BatterylessNodeDemo.unity");
    }
    static void AddFlow(string a,string b,Color color,bool gated=false)
    {
        var go=new GameObject("Flow · "+a+" → "+b); go.transform.SetParent(root);
        var lr=go.AddComponent<LineRenderer>(); lr.positionCount=2; lr.useWorldSpace=false;
        lr.SetPosition(0,nodes[a].localPosition+Vector3.up*.13f);lr.SetPosition(1,nodes[b].localPosition+Vector3.up*.13f);
        lr.startWidth=.035f;lr.endWidth=.035f;lr.material=Glow(color);lr.startColor=color;lr.endColor=color;
        demo.flows.Add(new BatterylessNodeDemo.Flow{from=nodes[a],to=nodes[b],color=color,gated=gated});
    }
    static Transform BoxNode(string title,string subtitle,Vector3 pos,Vector3 size,Color body,Color accent)
    {
        var g=GameObject.CreatePrimitive(PrimitiveType.Cube);g.name=title;g.transform.SetParent(root);g.transform.localPosition=pos;g.transform.localScale=size;
        g.GetComponent<Renderer>().material=Mat(body,accent*.38f);
        var edge=GameObject.CreatePrimitive(PrimitiveType.Cube);edge.name=title+" · accent trim";edge.transform.SetParent(g.transform);edge.transform.localPosition=new Vector3(0,.5f,0);edge.transform.localScale=new Vector3(.94f,.025f,.94f);edge.GetComponent<Renderer>().material=Mat(accent,accent*.6f);Object.DestroyImmediate(edge.GetComponent<Collider>());
        Label(title,pos+Vector3.up*(size.y*.5f+.22f),.15f,Color.white);
        Label(subtitle,pos+Vector3.up*(size.y*.5f+.02f),.105f,new Color(.66f,.76f,.86f));
        return g.transform;
    }
    static Transform CylinderNode(string title,string subtitle,Vector3 pos,Vector3 size,Color accent)
    {
        var g=GameObject.CreatePrimitive(PrimitiveType.Cylinder);g.name=title;g.transform.SetParent(root);g.transform.localPosition=pos;g.transform.localScale=size;g.GetComponent<Renderer>().material=Mat(new Color(.12f,.22f,.32f),accent*.4f);
        Label(title,pos+Vector3.up*(size.y*.5f+.26f),.16f,Color.white);Label(subtitle,pos+Vector3.up*(size.y*.5f+.04f),.105f,new Color(.68f,.81f,.94f));return g.transform;
    }
    static void PanelCells(Transform panel)
    {
        for(int i=0;i<5;i++){var cell=GameObject.CreatePrimitive(PrimitiveType.Cube);cell.name="PV cell gridline";cell.transform.SetParent(panel);cell.transform.localPosition=new Vector3(-.38f+i*.19f,.51f,0);cell.transform.localScale=new Vector3(.012f,.02f,.94f);cell.GetComponent<Renderer>().material=Mat(new Color(.37f,.75f,.94f),new Color(.25f,.58f,.82f));Object.DestroyImmediate(cell.GetComponent<Collider>());}
    }
    static void Label(string text,Vector3 pos,float size,Color color)
    {
        var g=new GameObject("Label · "+text);g.transform.SetParent(root);g.transform.position=pos;
        var tm=g.AddComponent<TextMesh>();tm.text=text;tm.fontSize=64;tm.characterSize=size/6f;tm.anchor=TextAnchor.MiddleCenter;tm.alignment=TextAlignment.Center;tm.color=color;tm.richText=false;g.AddComponent<FaceCamera>();
    }
    static Material Mat(Color color,Color emission)
    {
        var m=new Material(Shader.Find("Universal Render Pipeline/Lit")??Shader.Find("Standard"));m.color=color;m.EnableKeyword("_EMISSION");m.SetColor("_EmissionColor",emission);return m;
    }
    static Material Glow(Color color)=>Mat(new Color(color.r,color.g,color.b,.75f),color*.8f);
}

