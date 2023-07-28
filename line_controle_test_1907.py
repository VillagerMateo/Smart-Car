import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()


def make_coordinates(view, line_parameters):
    slope, intercept = line_parameters
    #print(view.shape)
    y1 = view.shape[0]
    y2 = int(y1 * (2/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(view, lines):
    left_fit = [] 
    right_fit = []
    
        
    print("W funkcji intercept: ", lines[0], " ", lines[1])
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            if not left_fit:
                left_fit.append((slope, intercept))
        else:
            if not right_fit:
                right_fit.append((slope, intercept))
            
    if len(left_fit) > 0:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_coordinates(view, left_fit_average)
    else:
        left_line = np.array([np.nan])
    
    if len(right_fit) > 0:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(view, right_fit_average)
    else:
        right_line = np.array([np.nan])
    
    return np.array([left_line, right_line])


def calculate_center_line(left_line, right_line):
    x1_left, y1_left, x2_left, y2_left = left_line
    x1_right, y1_right, x2_right, y2_right = right_line

    center_x1 = int((x1_left + x1_right) / 2)
    center_x2 = int((x2_left + x2_right) / 2)
    center_y1 = int((y1_left + y1_right) / 2)
    center_y2 = int((y2_left + y2_right) / 2)

    center_line = np.array([center_x1, center_y1, center_x2, center_y2])
    return center_line



def canny(gray):
    # redukcja szumu - Rozmycie Gaussiana
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # metoda 'canny' do identyfikacji krawedzi
    canny = cv2.Canny(blur, 50, 150)
    return canny


def vehicle_control(direction):
    

    print(direction)                
#     direction = input("Podaj kierunek: ")
    direction += "\n"
    #print(direction)
            
    ser.write(direction.encode('utf-8'))
    #line = ser.readline().decode('utf-8').rstrip()
    #print(line)
    time.sleep(0.05)


def determine_steering(lines, tolerance, center_line=None):
    
    frame_width = 420  # Szerokość ramki obrazu

#     center_range_start = 190  # Początek zakresu środka ramki
#     center_range_end = 230  # Koniec zakresu środka ramki
    if center_line is not None:
        center_x = center_line[0]
        if center_x < (frame_width / 2) - tolerance:
            vehicle_control("Q")
            return 'left'  # Skręć w lewo
        elif center_x > (frame_width / 2) + tolerance:
            vehicle_control("E")
            return 'right'  # Skręć w prawo
        else:
            vehicle_control("W")
            return 'straight'  # Jedź prosto
    if np.isnan(lines[0][0]) != True:
        vehicle_control("E")
        return "right"
    
    if np.isnan(lines[1][0]) != True:
        vehicle_control("Q")
        return "left"
    
    

def display_lines(view, lines, center_line=None):
    line_view = np.zeros_like(view)
    if lines is not None:
        for line in lines:
            if np.isnan(line).any():
                #print("Pusta: ", line)
                continue
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_view, (x1, y1), (x2, y2), (255, 0, 0), 10)
    
    if center_line is not None:
        x1, y1, x2, y2 = center_line.reshape(4)
        cv2.line(line_view, (x1, y1), (x2, y2), (0, 255, 0), 10)
        print(determine_steering(lines, 35, center_line))
    else:
        print(determine_steering(lines, 35))
    
    
        
    
    
    return line_view


def region_of_interest(view):
    # ustawienie w jakim polu widzenia beda lapane linie
    height = view.shape[0]
    triangle = np.array([
    [(0, 320), (25, 100), (395, 100), (420, 320)]
    ])

    mask = np.zeros_like(view)
    cv2.fillPoly(mask, triangle, 255)
    masked_view = cv2.bitwise_and(view, mask)
    return masked_view

cap = cv2.VideoCapture(0)


while(cap.isOpened()):
    ret, frame = cap.read()    
    frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)
    frame = cv2.resize(frame, (420, 320))
    
    
    
        # utworzenie kopii tablicy z obrazu
    lane_view = np.copy(frame)
    view_with_lines = lane_view

    gray = cv2.cvtColor(lane_view, cv2.COLOR_RGB2GRAY)
        # redukcja szumu - Rozmycie Gaussiana
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # metoda 'canny' do identyfikacji krawedzi
    canny = cv2.Canny(blur, 50, 150)
    
    cropped_view = region_of_interest(canny)
    try:    
        lines = cv2.HoughLinesP(cropped_view, 2, np.pi/180, 100, np.array([ ]), minLineLength=40, maxLineGap=5 )
        
        if np.all(lines != None):
            print("Wszystkie linie nie są równe None")
            averaged_lines = average_slope_intercept(lane_view, lines)
#             print(type(averaged_lines), " - ", averaged_lines)
#             print(type(averaged_lines[0]), " - ", averaged_lines[0])
#             print(type(averaged_lines[1]), " - ", averaged_lines[1], " - ", averaged_lines[1][0])
            
            if np.isnan(averaged_lines[0][0]) != True and np.isnan(averaged_lines[1][0]) != True:
            
            #if averaged_lines[1] != [nan] and averaged_lines[0] != [nan]:
                print("Nasza koordynaty(L/P): ", averaged_lines[0], " | ", averaged_lines[1])
            
                center_line = calculate_center_line(averaged_lines[0], averaged_lines[1])
                print("Środek koordynaty: ", center_line)
            
                line_view = display_lines(lane_view, averaged_lines, center_line)
            
                view_with_lines = cv2.addWeighted(lane_view, 0.8, line_view, 1,1)
            else:
                print("Nasza koordynaty(L/P): ", averaged_lines[0], " | ", averaged_lines[1])
                
                line_view = display_lines(lane_view, averaged_lines)
            
                view_with_lines = cv2.addWeighted(lane_view, 0.8, line_view, 1,1)
        else:
            print(lines[0], " ", lines[1])
        
        
        
    except:
        vehicle_control("O")
        print(" ")
        
    cv2.imshow('frame', cropped_view)
    cv2.imshow('frame2', view_with_lines)
    #cv2.imshow('frame3', lane_view)
#     time.sleep(0.4)
    
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


