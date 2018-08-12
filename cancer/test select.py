from matplotlib import pyplot as plt
import numpy as np
import cv2

russia = cv2.imread("russia.jpg", cv2.IMREAD_ANYDEPTH)
plt.imshow(russia, interpolation='nearest')
f = plt.gcf()
plt.autoscale(False)
ax = f.gca()
coordinates = []

f.show()
def get_left_and_right_points(ls):
    ls=sorted(ls,key=lambda ls: ls[1])
    left = []
    right = []
    top = ls[0]
    bottom=ls[-1]
    if(ls[-1][1]==ls[-2][0]):
        bottom = ls[-1] if ls[-1][0] <ls[-2][0] else ls[-2]
    slope = (top[1]-bottom[1])/(top[0]-bottom[0])
    b = top[1] - (slope*top[0])
    for point in ls:
        expected_x = (point[1] - b)/slope
        if point[0]<=expected_x:
            left.append(point)
        if point[0]>=expected_x:
            right.append(point)
    return [left,right] 
def get_eqn_from_line(point1, point2):
    y2 = point2[1]
    y1 = point1[1]
    x2 = point2[0]
    x1 = point1[0]
    m = (y2-y1)/(x2-x1)
    b = y2-(m*x2)
    return [m,b]
def ROI(left,right):
    ROI_values = []
    starting_point = left[0]
    ending_point = left[-1]
    for point in left:
        point[0] = int(point[0])
        point[1] = int(point[1])
    for point in right:
        point[0] = int(point[0])
        point[1] = int(point[1])
    counter = point[0][1]
    end = point[-1][1]
    border_x_coordinate = starting_point[0]
    border_y_coordinate = starting_point[1]
    current_y = starting_point[1]
    up_or_down = -1 if current_y > ending_point[1] else 1
    while (current_y != ending_point[1]):
        leftside_point1 = 0
        leftside_point2 = 0
        rightside_point1 = 0
        rightside_point2 = 0
        for i in range(len(left)):
            if current_y < left[i][1]:
                leftside_point2= left[i]
                leftside_point1 = left[i-1]
        for i in range(len(right)):
            if current_y < right[i][1]:
                rightside_point2 = right[i]
                rightside_point1 = right[i-1]
        segment_tuple = []
        rightside_dif_y = abs(rightside_point2[1] - current_y)
        leftside_dif_y = abs(leftside_point2[1] - current_y)
        if rightside_dif_y <= leftside_dif_y:
            segment_tuple = [current_y,rightside_point2]
        else:
            segment_tuple = [current_y,leftside_point2]
        [m,b]=
        for i in range(current_y,segment_tuple[1],up_or_down):
            
        
            
def onclick(event):    
    coordinates.append([event.xdata,event.ydata])
    if len(coordinates)>1:
        if(abs(coordinates[0][0] - event.xdata) < 5 and abs(coordinates[0][1] - event.ydata) < 5):
            x1 = coordinates[-2][0]
            x2 = coordinates[0][0]
            y1 = coordinates[-2][1]
            y2 = coordinates[0][1]
            plt.plot([x1,x2],[y1,y2],'m--')
            coordinates.pop()
            f.canvas.mpl_disconnect(cid)
            left,right = get_left_and_right_points(coordinates)
            print(left)
            print(right)
        else:
            
            x1 = coordinates[-1][0]
            x2 = coordinates[-2][0]
            y1 = coordinates[-1][1]
            y2 = coordinates[-2][1]
            plt.plot([x1,x2],[y1,y2],'m--')
        f.canvas.draw()
    f.canvas.draw()
cid=f.canvas.mpl_connect('button_press_event',onclick)


    
