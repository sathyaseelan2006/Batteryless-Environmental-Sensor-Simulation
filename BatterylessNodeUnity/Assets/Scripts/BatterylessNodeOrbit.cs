using UnityEngine;

public class BatterylessNodeOrbit : MonoBehaviour
{
    public Transform target;
    float distance = 22, yaw, pitch = 22;

    void LateUpdate()
    {
        if (!target) return;
        if (Input.GetMouseButton(0))
        {
            yaw += Input.GetAxis("Mouse X") * 4;
            pitch = Mathf.Clamp(pitch - Input.GetAxis("Mouse Y") * 3, 8, 58);
        }
        distance = Mathf.Clamp(distance - Input.mouseScrollDelta.y, 13, 34);
        transform.position = target.position + Quaternion.Euler(pitch, yaw, 0) * new Vector3(0, 0, -distance);
        transform.LookAt(target.position);
    }
}
