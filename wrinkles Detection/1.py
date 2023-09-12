import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to process the image and detect wrinkles
def detect_wrinkles():
    # Load the input image from the file selected by the user
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img = cv2.resize(img, (421, 612))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, 10, 100)
        ret, thresh = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        wrinkle_count = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10 and h > 5 and w < 50 and h < 20 and w / h > 2:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                wrinkle_count += 1

        if wrinkle_count > 0:
            result_label.config(text="Wrinkles detected")
        else:
            result_label.config(text="No wrinkles detected")

        # Convert the OpenCV image to a format that tkinter can display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        # Update the image label with the new image
        image_label.img_tk = img_tk  # Keep a reference to avoid garbage collection
        image_label.config(image=img_tk)

# Create a tkinter window
window = tk.Tk()
window.title("Wrinkle Detection")

# Set the window size
window.geometry("800x700")  # Set the dimensions to your desired size

# Create a label to display the image
image_label = tk.Label(window)
image_label.pack()

# Create a button to open the image file
open_button = tk.Button(window, text="Open Image", command=detect_wrinkles)
open_button.pack()

# Create a label to display the result
result_label = tk.Label(window, text="", font=("Helvetica", 16))
result_label.pack()

# Run the tkinter main loop
window.mainloop()
