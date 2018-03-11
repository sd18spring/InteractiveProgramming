from fingerTrack import *
from canvas import *
import cv2


def main():
    """
    """
    track = finger_track()
    cap = cv2.VideoCapture(0)
    newCanvas = canvas(cap.get(3), cap.get(4))
    disappr = True


    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)

        hsv = track.BGR2HSV(frame)
        redMask = track.red_mask(hsv)
        mask = cv2.bilateralFilter(redMask, 10, 40, 40)
        mask = cv2.blur(mask, (5, 5))
        res = cv2.bitwise_and(frame, frame, mask=redMask)
        cv2.imshow('original', res)
        mask = cv2.blur(mask, (20, 20))
        track.find_center(mask, frame)
        # track.refine_path()
        track.draw(newCanvas, disappr=disappr)
        newCanvas.show_canvas()

        if cv2.waitKey(1) & 0xFF == ord('s'):
            newCanvas.save_drawing()
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('d'):
            disappr = ~disappr
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            newCanvas.clear()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
