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

        if newCanvas.points == 0:
            newCanvas.rectangle()
        elif newCanvas.in_rect(track.cx,track.cy) == True:
            newCanvas.clear()
            newCanvas.rectangle()
        newCanvas.show_canvas()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            newCanvas.save_drawing()
            break
        if cv2.waitKey(1) & 0xFF == ord('d'):
            disappr = ~disappr
        if cv2.waitKey(1) & 0xFF == ord('c'):
            newCanvas.clear()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
