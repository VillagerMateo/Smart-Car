from picamera import PiCamera
import cv2
import numpy as np
#import matplotlib.pyplot as plt


def make_coordinates(view, line_parameters):
    slope, intercept = line_parameters
    #print(view.shape)
    y1 = view.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(view, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    print(left_fit_average, 'left')
    print(right_fit_average, 'right')
    
    left_line = make_coordinates(view, left_fit_average)
    right_line = make_coordinates(view, right_fit_average)
    return np.array([left_line, right_line])
    
    
    


def region_of_interest(view):
    # ustawienie w jakim polu widzenia beda lapane linie
    height = view.shape[0]
    triangle = np.array([
        [(0, height), (420, height), (300, 150), (80, 150)]
        ])
    mask = np.zeros_like(view)
    cv2.fillPoly(mask, triangle, 255)
    masked_view = cv2.bitwise_and(view, mask)
    return masked_view
    
    
def display_lines(view, lines):
    line_view = np.zeros_like(view)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_view, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_view






cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()    
    frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)
    frame = cv2.resize(frame, (420, 320))
    
    # utworzenie kopii tablicy z obrazu
    lane_view = np.copy(frame)


    
    gray = cv2.cvtColor(lane_view, cv2.COLOR_RGB2GRAY)
    
    # redukcja szumu - Rozmycie Gaussiana
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # metoda 'canny' do identyfikacji krawedzi
    canny = cv2.Canny(blur, 50, 150)
    
    
    
    
    
    cropped_view = region_of_interest(canny)
    lines = cv2.HoughLinesP(cropped_view, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)



    averaged_lines = average_slope_intercept(lane_view, lines)
    line_view = display_lines(lane_view, averaged_lines)
    finall_view = cv2.addWeighted(lane_view, 0.8, line_view, 1, 1)

    




    #plt.imshow(canny)
    #plt.show()
    
    cv2.imshow('frame', finall_view)
    
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


#camera.start_preview()
#sleep(5)
#camera.stop_preview()