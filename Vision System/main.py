import cv2

def main():
    # stream = Stream()
    # stream.add_type(Stream_Types.IMAGE)
    # stream.add_image_path("Resources\green_buoy.jpg")
    cap = cv2.imread("Resources/green-buoy.png")
    print(cap)
    cv2.imshow("CAP", cap)
    # stream.add_camera(0)
    # stream.resize()
    # stream.colour_detection()
    # # stream.object_tracking()
    # stream.edge_detection()

    # stream.add_trackbars()'`  
    # stream.stream()

    



                 

main()