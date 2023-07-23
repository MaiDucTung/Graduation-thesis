import cv2

def open_camera():
    # Open the USB camera
    cap = cv2.VideoCapture(0, cv2.CAP_USB)

    while True:
        # Read the current frame from the camera
        ret, frame = cap.read()

        # Display the frame in a window called "Camera Preview"
        cv2.imshow('Camera Preview', frame)

        # Check for the 'q' key to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to open the USB camera
open_camera()
