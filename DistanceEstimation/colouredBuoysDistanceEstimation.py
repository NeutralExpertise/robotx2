import cv2
import numpy as np

cap = cv2.VideoCapture(0)


red_lower_range = np.array([136, 87, 111], np.uint8)
red_upper_range = np.array([180, 255, 255], np.uint8)

# Known distance of buoy from the camera
buoy_known_distance = 30.0
# Known width of physical buoy
buoy_known_width = 11.0

def focal_length_formula(object_known_distance, object_physical_width, object_pixel_width):

    focal_length = (object_known_distance * object_pixel_width) / object_physical_width

    return focal_length

# Function for Tracking the object with the help of colour
def object_data(img, lower_range, upper_range, r, g, b):
    obj_width = 0
    # Convert the image/frame(s) from BGR (RGB colour space) into HSV (hue, saturation, value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Defines the lower and upper range of a selected colour into HSV
    # Creates a mask for a selected colour to be detected and highlighted
    mask = cv2.inRange(hsv, lower_range, upper_range)

    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    # Create a contour to make the specified coloured area more identifiable and distinguishable
    contours, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # Constructing the size of boxes to be drawn around the detected white area
        x = 600
        if cv2.contourArea(contour) > x:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (r, g, b, 2))
            obj_width = w

    return obj_width

def distance_formula(focal_length, object_physical_width, object_width_in_pixels):

    distance = (object_physical_width * focal_length) / object_width_in_pixels

    return distance


red_buoy_image = cv2.imread("Pictures/red_buoy.jpg")
red_buoy_obj_width = object_data(red_buoy_image, red_lower_range, red_upper_range, 0, 0, 255)
red_buoy_focal_length = focal_length_formula(buoy_known_distance, buoy_known_width, red_buoy_obj_width)
cv2.imshow("Red_BUOY", red_buoy_image)

print(red_buoy_focal_length)

while True:
    ret, frame = cap.read()
    obj_width_in_frame = object_data(frame, red_lower_range, red_upper_range, 0, 0, 255)
    if obj_width_in_frame != 0:
        Distance = distance_formula(red_buoy_focal_length, buoy_known_width, red_buoy_obj_width)
        cv2.putText(frame, f"Distance: {round(Distance, 2)} CM", (30, 35), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0),
                    2)

    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()










