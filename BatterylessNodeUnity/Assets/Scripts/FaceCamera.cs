using UnityEngine;

public class FaceCamera : MonoBehaviour
{
    void LateUpdate()
    {
        if (Camera.main) transform.rotation = Camera.main.transform.rotation;
    }
}
