#  imports
import pickle
from pathlib import Path
from sys import argv

import cv2
import numpy as np
import pandas as pd
from keras.models import load_model
from mediapipe import solutions

from preprocessing import extract_features, load_image
nl = "\n"


class ModelWrapper:

    

    def __init__(self, choice="rf"):
        
        self.mtype = choice
        if choice == "rf":
            with open(Path("saved_models") / "model.sav", "rb") as f:
                model_dict = pickle.load(f)
                self.model = [*model_dict.values()][0]
        elif choice == "nn":
            self.model = load_model(str((Path("saved_models") / "NN_model").resolve()))

    def predict_proba(self, *args, **kwargs):
        if self.mtype == "rf":
            return self.model.predict_proba(*args, **kwargs).flatten()
        elif self.mtype == "nn":
            return self.model.predict_proba(*args, **kwargs).flatten()

    def labels(self):
        if self.mtype == "rf":
            return self.model.classes_
        elif self.mtype == "nn":
            return [
                "Child's pose",
                "Cobra Pose",
                "Downward-facing Dog",
                "Easy Pose",
                "Half Splits Pose",
                "Happy Baby's pose",
                "Low Lunge",
                "Standing Forward Bend",
                "Upward-Facing Dog",
                "cat pose",
                "cow pose",
                "high plank",
            ]


mp_drawing = solutions.drawing_utils
cv2.waitKey(0)


def process_video(file, fps=2, model_choice="rf", show_video=None, output_file=None):
    
    
    model = ModelWrapper(model_choice)

    
    cap = cv2.VideoCapture(file)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frames_between_predict = int(video_fps / fps) if fps is not None else 1
    video_size = int(cap.get(3)), int(cap.get(4))

    
    if output_file:
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        export_video = cv2.VideoWriter(output_file, fourcc, video_fps, video_size)

    draw_results = output_file or show_video

    
    out = []
    counter = 0
    detected_pose = None

    while cap.isOpened():
        ret, frame = cap.read()
        counter += 1
        time = counter * 1 / video_fps

        
        if ret:
            
            if counter % frames_between_predict == 0:
                
                with solutions.pose.Pose(
                    static_image_mode=True,
                    model_complexity=2,
                    min_detection_confidence=0.5,
                ) as pose:
                    
                    detected_pose = pose.process(frame)

                
                pose_features = extract_features(detected_pose.pose_landmarks)
                ft_np = np.atleast_2d([*pose_features.values()])
                if not np.isnan(ft_np.sum()):
                    predicted_pose = model.predict_proba(ft_np)

                    
                    result = {"time": time}
                    for key, val in zip(model.labels(), predicted_pose):
                        result[key] = val
                    out.append(result)

                    
                    best_pred = get_best_predicition(predicted_pose, model.labels())
                    if best_pred:
                        print(
                            ", ".join(
                                f"{name} ({(prob-0.1)*112.98:.0f}%)" for name, prob in best_pred
                            )
                        )

            
            if draw_results:
                if detected_pose:
                    mp_drawing.draw_landmarks(frame, detected_pose.pose_landmarks)
                    if best_pred:
                        for i, prediction in enumerate(best_pred):
                            yoga_move = f"{prediction[0]} , Accuracy:({prediction[1]*100:.0f}%)"
                            cv2.putText(
                                frame,
                                yoga_move,
                                (50, 50 + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.75,
                                (0, 0, 0),
                                2,
                                cv2.LINE_AA,
                            )
                if show_video:
                    cv2.imshow("Video", frame)
                if output_file:
                    export_video.write(frame)

        else:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    
    cv2.destroyAllWindows()

    return pd.DataFrame(out)


def get_best_predicition(proba, labels, thresholt=0.05) -> list:



    

    order = np.argsort(proba)[::-1]
    results = [(labels[order[0]], proba[order[0]])]
    cum_proba = proba[order[0]]
    for o in order[1:]:
        if abs(results[-1][1] - proba[o]) > thresholt:
            break
        results.append((labels[o], proba[o]))
        cum_proba += proba[o]

    if cum_proba > 0.30 and len(results) < 4:
        return results
    else:
        return []


if __name__ == "__main__":
    filename = argv[1]

    if filename == "webcam":
        filename = 0
        outname = "webcam_annotated.mp4"
    else:
        filename = Path(filename)
        outname = filename.stem

    model = argv[2] if len(argv) >= 3 else "rf"
    print(f"{filename}, {outname}, {model}")

    video = process_video(
        str(filename.resolve()),
        show_video=False,
        fps=5,
        model_choice=model,
        output_file=f"{outname}_{model}_annotated.mp4",
    )

    
    video.to_csv(f"video_results-{model}-{outname}.csv", index=False)
