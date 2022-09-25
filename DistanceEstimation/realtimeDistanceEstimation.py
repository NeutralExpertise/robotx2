import cv2
import numpy as np

# Function to stack images side-by-side in an array
def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rows_available = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rows_available:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank]*rows
        hor_con = [image_blank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def focal_length_buoy(object_known_distance, object_physical_width, object_frame_pixel_width):
    focal_length = (object_frame_pixel_width * object_known_distance) / object_physical_width
    return focal_length

# Function for Tracking the buoy object with the help of colour
def buoy_data(img, lower_range, upper_range, b, g, r):
    buoy_width = 0
    # Convert the image/frame(s) from BGR (RGB colour space) into HSV (hue, saturation, value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Defines the lower and upper range of a selected colour into HSV
    # Creates a mask for a selected colour to be detected and highlighted
    mask = cv2.inRange(hsv, lower_range, upper_range)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # Constructing the size of boxes to be drawn around the detected white area
        x = 600
        if cv2.contourArea(contour) > x:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (b, g, r), 2)
            buoy_width = w
    return buoy_width

# Function formula to find the distance between buoy and camera
def buoy_distance_estimator(buoy_focal_length, buoy_physical_width, buoy_width_in_frame_pixels):
    distance = (buoy_physical_width * buoy_focal_length) / buoy_width_in_frame_pixels

    return distance


cap = cv2.VideoCapture(0)

# Defines the upper and lower ranges for the colour red
red_lower_range = np.array([136, 87, 111], np.uint8)
red_upper_range = np.array([179, 255, 255], np.uint8)

# Defines the upper and lower ranges for the colour green
green_lower_range = np.array([25, 52, 72], np.uint8)
green_upper_range = np.array([102, 255, 255], np.uint8)

# Defines the upper and lower ranges for the colour green
yellow_lower_range = np.array([11, 93, 85], np.uint8)
yellow_upper_range = np.array([65, 180, 255], np.uint8)

# Known distance of buoy from the camera
buoy_known_distance = 30.0
# Known width of physical buoy
buoy_known_width = 11.0

red_buoy_image = cv2.imread("Pictures/red_buoy.jpg")
# Find red buoy width
red_buoy_image_obj_width = buoy_data(red_buoy_image, red_lower_range, red_upper_range, 0, 0, 255)
# Find red buoy focal length
red_buoy_focal_length_found = focal_length_buoy(buoy_known_distance, buoy_known_width, red_buoy_image_obj_width)

green_buoy_image = cv2.imread("Pictures/green_buoy.jpg")
# Find green buoy width
green_buoy_image_obj_width = buoy_data(green_buoy_image, green_lower_range, green_upper_range, 0, 255, 0)
# Find green buoy focal length
green_buoy_focal_length_found = focal_length_buoy(buoy_known_distance, buoy_known_width, green_buoy_image_obj_width)

yellow_buoy_image = cv2.imread("Pictures/yellow_buoy.jpg")
# Find yellow buoy width
yellow_buoy_image_obj_width = buoy_data(yellow_buoy_image, yellow_lower_range, yellow_upper_range, 28, 255, 255)
# Find yellow buoy focal length
yellow_buoy_focal_length_found = focal_length_buoy(buoy_known_distance, buoy_known_width, yellow_buoy_image_obj_width)

# Stack images into an image array
buoys_image_stack = stack_images(0.4, ([red_buoy_image, green_buoy_image, yellow_buoy_image]))
cv2.imshow("Referenced Coloured Buoys", buoys_image_stack)

print("red focal length", red_buoy_focal_length_found)
print("green focal length", green_buoy_focal_length_found)
print("yellow focal length", yellow_buoy_focal_length_found)

# Find distances of selected colours and displays in text in CM
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1080, 720))
    red_buoy_width_in_pixels = buoy_data(frame, red_lower_range, red_upper_range, 0, 0, 255)
    green_buoy_width_in_pixels = buoy_data(frame, green_lower_range, green_upper_range, 0, 255, 0)
    yellow_buoy_width_in_pixels = buoy_data(frame, yellow_lower_range, yellow_upper_range, 28, 255, 255)

    if red_buoy_width_in_pixels != 0:
        red_distance = buoy_distance_estimator(red_buoy_focal_length_found, buoy_known_width, red_buoy_width_in_pixels)
        cv2.putText(frame, f"RED_Buoy_Distance: {round(red_distance, 2)} CM", (30, 35), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)
    if green_buoy_width_in_pixels != 0:
        green_distance = buoy_distance_estimator(green_buoy_focal_length_found, buoy_known_width, green_buoy_width_in_pixels)
        cv2.putText(frame, f"GREEN_Buoy_Distance: {round(green_distance, 2)} CM", (30, 65), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)
    if yellow_buoy_width_in_pixels != 0:
        yellow_distance = buoy_distance_estimator(yellow_buoy_focal_length_found, buoy_known_width, yellow_buoy_width_in_pixels)
        cv2.putText(frame, f"YELLLOW_Buoy_Distance: {round(yellow_distance, 2)} CM", (30, 95), cv2.FONT_HERSHEY_COMPLEX, 0.6, (28, 255, 255), 2)

    cv2.imshow("Coloured Buoys Distance Estimator Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases captured frame
cap.release()
# Eliminates all GUI Windows
cv2.destroyAllWindows()
