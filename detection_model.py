import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2

# Step 1: Load and preprocess the dataset
data_directory = "./dataset"
image_size = (224, 224)
num_classes = 4
batch_size = 32

print("Creating the data generator...")
datagen = ImageDataGenerator(rescale=1.0 / 255.0)


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, image_size)
    image = image.astype("float32") / 255.0
    return image


def load_dataset():
    X, y = [], []
    class_mapping = {}
    label_count = 0

    for class_name in os.listdir(data_directory):
        class_dir = os.path.join(data_directory, class_name)
        class_mapping[class_name] = label_count
        label_count += 1

        for image_name in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_name)
            image = preprocess_image(image_path)
            X.append(image)
            y.append(class_mapping[class_name])  # Use integer labels here

    return np.array(X), np.array(y)


X, y = load_dataset()
y = to_categorical(y, num_classes=num_classes)
print("Dataset loaded and preprocessed successfully.")

# Rest of your code (steps 2 to 8) remains the same


# Step 2: Split the dataset into training and testing sets
print("Splitting the dataset into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Dataset split completed.")

# Step 3: Build the CNN model
print("Creating the model...")
model = Sequential()
model.add(
    Conv2D(32, (3, 3), activation="relu", input_shape=(image_size[0], image_size[1], 3))
)
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(
    Dense(num_classes, activation="softmax")
)  # Output layer with num_classes neurons
print("Model creation complete.")

# Step 4: Compile the model
print("Compiling the model...")
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
print("Model compilation completed.")

# Step 5: Create the data generator for training
print("Creating the data generator for training...")
train_generator = datagen.flow(X_train, y_train, batch_size=batch_size)

# Step 6: Train the model using the data generator
print("Training the model...")
model.fit(
    train_generator,
    steps_per_epoch=len(X_train) // batch_size,
    epochs=10,
    validation_data=(X_test, y_test),
)
print("Model training completed.")

# Step 7: Evaluate the model
print("Evaluating the model...")
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

# Step 8: Save the trained model
print("Saving the trained model...")
model.save("model.h5")
print("Model saved successfully.")
