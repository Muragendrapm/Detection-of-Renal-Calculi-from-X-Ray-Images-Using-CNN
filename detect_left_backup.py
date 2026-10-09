import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2

# Load the pre-trained model
model = load_model("model.h5")

# Define target image size
image_height, image_width = 224, 224


# Image preprocessing function (same as before)
def preprocess_image(image_path, target_size=(image_height, image_width)):
    image = Image.open(image_path)
    image = image.resize(target_size)
    image = np.array(image)  # Convert PIL Image to NumPy array
    image = image.astype("float32") / 255.0
    return image


calibration_factor = 0.5


# def estimate_size(probability):
#     # Placeholder conversion from probability to size (for demonstration purposes)
#     min_size_mm = 1
#     max_size_mm = 10
#     estimated_size_mm = min_size_mm + (max_size_mm - min_size_mm) * probability
#     return estimated_size_mm


# Create the make_prediction function
def make_prediction():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = preprocess_image(file_path)
        image = Image.fromarray(np.uint8(image * 255))  # Convert back to PIL image

        predictions = model.predict(np.expand_dims(image, axis=0))[0]
        kidney_stone_prob = predictions[1]

        if kidney_stone_prob > 0.5:  # You can adjust the threshold as needed
            # Get image dimensions
            width, height = image.size

            # Calculate the center of the image
            center_x = width // 2
            center_y = height // 2

            # Draw a red marker at the center
            draw = ImageDraw.Draw(image)
            marker_size = 10
            marker_color = (255, 0, 0)  # Red color
            draw.rectangle(
                [
                    center_x - marker_size,
                    center_y - marker_size,
                    center_x + marker_size,
                    center_y + marker_size,
                ],
                outline=marker_color,
                width=2,
            )

        no_kidney_stone_prob = predictions[0]
        image_tk = ImageTk.PhotoImage(image)

        uploaded_image_label.config(image=image_tk)
        uploaded_image_label.image = image_tk
        kidneyStone = ""
        if kidney_stone_prob == 1:
            kidneyStone = "Kidney Stone Present"
        else:
            kidneyStone = "Kidney Stone Not Present"

        # Display probabilities
        result_label.config(
            text=f"{kidneyStone}",
        )


# Create the GUI window
window = tk.Tk()
window.title("Kidney Stone Detection")
window.geometry("800x600")  # Set the initial size of the window

# Create a Frame for the left side
left_frame = tk.Frame(window, background="white")
left_frame.pack(side=tk.LEFT, expand=True, padx=20, pady=10, fill=tk.BOTH)

# Create a Label with larger font at the top left corner
heading_label = tk.Label(
    left_frame,
    text="Kidney Stone Detection",
    font=("Helvetica", 20, "bold"),
    bg="red",
    fg="white",
)
heading_label.pack(fill=tk.BOTH, padx=10, pady=10)

# Create a Frame for prevention tips and button
prevention_frame = tk.Frame(left_frame, bg="white")
prevention_frame.pack(fill=tk.BOTH)

# Create a Label for prevention tips
prevention_text = (
    "Prevention Tips for Kidney Stones:\n\n"
    "1. Stay Hydrated: Drink plenty of water to reduce the risk of stone formation.\n"
    "2. Eat a Balanced Diet: Limit salt, animal protein, and oxalate-rich foods.\n"
    "3. Maintain a Healthy Weight: Aim for a healthy body weight to lower the risk.\n"
    "4. Limit Sugar and Soda: Excess sugar and soda can contribute to stone formation.\n"
)
prevention_label = tk.Label(
    prevention_frame,
    text=prevention_text,
    justify=tk.LEFT,
    padx=20,
    pady=10,
    bg="white",
)
prevention_label.pack(fill=tk.BOTH)

# Create a button to upload an image
upload_button = tk.Button(
    prevention_frame, text="Upload Image", command=make_prediction
)
upload_button.pack(padx=20, pady=(0, 20), anchor=tk.CENTER)


uploaded_image_label = tk.Label(left_frame)
uploaded_image_label.pack(side=tk.TOP, padx=20, pady=20)

result_label = tk.Label(left_frame, text="", font=("Helvetica", 20, "bold"))
result_label.pack(side=tk.TOP, padx=20, pady=50)


image_frame = tk.Frame(left_frame, background="white")
image_frame.pack(expand=True, padx=20, pady=10)



# Add sample images to the frame
sample_images = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]
for row, image_path in enumerate(sample_images):
    img = Image.open(image_path)
    img.thumbnail((200, 200))  # Resize images for display
    img = ImageTk.PhotoImage(img)
    label = tk.Label(image_frame, image=img)
    label.image = img
    label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
# Create a Frame for the right side
right_frame = tk.Frame(window, background="white")
right_frame.pack(side=tk.RIGHT, expand=True, padx=20, pady=10, fill=tk.BOTH)

# size_label = tk.Label(
#     window, text="Estimated Size:", font=("Helvetica", 16, "bold"), bg="white"
# )
# size_label.pack(fill=tk.BOTH, padx=20, pady=10)

# # Create a variable to hold the estimated size
# estimated_size_var = tk.StringVar()
# estimated_size_label = tk.Label(
#     window, textvariable=estimated_size_var, font=("Helvetica", 14), bg="white"
# )
# estimated_size_label.pack(fill=tk.BOTH, padx=20)
# Create a label to display the uploaded image on the right side

# uploaded_image_label = tk.Label(right_frame)
# uploaded_image_label.pack(side=tk.TOP, padx=20, pady=100)

# Create a label to display the prediction result on the right side
# result_label = tk.Label(right_frame, text="", font=("Helvetica", 20, "bold"))
# result_label.pack(side=tk.BOTTOM, padx=20, pady=(0, 100))

# Run the GUI
window.mainloop()
