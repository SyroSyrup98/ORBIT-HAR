import cv2

from app.pose import PoseEstimator


pose = PoseEstimator()

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    raise RuntimeError("Could not open laptop camera")


print("Pose test started. Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        continue

    result = pose.detect(frame)

    if result.pose_landmarks:
        print(
            f"Pose detected: "
            f"{len(result.pose_landmarks[0])} landmarks"
        )

        for landmark in result.pose_landmarks[0]:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 255),
                -1,
            )

    cv2.imshow("ORBIT-HAR Pose Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
pose.close()