from fingerTrack import *
from canvas import *
import cv2
from optparse import OptionParser
import time

def init_opts():
    parser = OptionParser()
    parser.add_option("-d", action="store_false",
                      dest="disappr", default=True,
                      help="To run the program in the drawing mode")
    parser.add_option("-t", action="store_true",
                      dest="disappr", default=True,
                      help="To run the program in the tailing mode where the lines disappear after a period of time")
    parser.add_option("-g", action="store_true",
                      dest="game", default=False,
                      help="To run the program in the gaming mode where you try to hit boxes")
    parser.add_option("-l", "--length", action="store", type='int',
                      dest="length", default=3,
                      help="The starting length of the line")
    options, args = parser.parse_args()
    return options, args


def main():
    """
    """

    font = cv2.FONT_HERSHEY_SIMPLEX
    options, args = init_opts()
    track = finger_track()
    cap = cv2.VideoCapture(0)
    newCanvas = canvas(cap.get(3), cap.get(4))
    disappr = options.disappr
    track.pathlength = options.length
    game_time = 5
    current_time = 1
    start = time.time()
    while True:
        if time.time() - start > 1 and options.game:
            current_time += 1
            start = time.time()

        if current_time == game_time+1:
            while True:
                cv2.putText(newCanvas.new_canvas, 'Yay!!!', (int(newCanvas.width/2-100), int(newCanvas.height/2)), font, 3, (255, 0, 0), 2)
                cv2.putText(newCanvas.new_canvas, 'Your final score is:', (int(newCanvas.width/2-300), int(newCanvas.height/2+50)), font, 2, (0, 0, 255), 2)
                cv2.putText(newCanvas.new_canvas, str(newCanvas.points)+'!!!', (int(newCanvas.width/2-75), int(newCanvas.height/2+50)+75), font, 3, (0, 255, 0), 2)
                newCanvas.show_canvas()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            break
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        hsv = track.BGR2HSV(frame)
        redMask = track.red_mask(hsv)
        mask = cv2.bilateralFilter(redMask, 10, 40, 40)
        mask = cv2.blur(mask, (5, 5))
        res = cv2.bitwise_and(frame, frame, mask=redMask)
        cv2.imshow('original', res)
        mask = cv2.blur(mask, (20, 20))
        track.find_center(mask, frame, disappr=disappr)
        # track.refine_path()
        track.draw(newCanvas)

        # newCanvas.rectangle()
        if options.game:
            # print(newCanvas.points, newCanvas.run)
            if newCanvas.points == 0:
                if newCanvas.run == False:
                    newCanvas.make_rect()
                newCanvas.show_rect()
            flag = newCanvas.in_rect(track.cx, track.cy)
            if flag == True:
                newCanvas.addpoints(track)
                newCanvas.clear()
                newCanvas.show_rect()
            newCanvas.show_rect()
        cv2.putText(newCanvas.new_canvas, 'Time left: '+str(game_time-current_time), (0, 15), font, .5, (255, 255, 255), 1)
        newCanvas.show_canvas()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            newCanvas.save_drawing()
            break

        if cv2.waitKey(1) & 0xFF == ord('d'):
            if disappr:
                disappr = False
            else:
                disappr = True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('d'):
            disappr = ~disappr

        if cv2.waitKey(1) & 0xFF == ord('c'):
            newCanvas.clear()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    main()
