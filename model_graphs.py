import streamlit as st
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Model Training Graphs", layout="wide")

st.title("📊 MNIST Model Training Performance")

# Load dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Model
model = Sequential([
    Dense(256, activation="relu", input_shape=(784,)),
    Dropout(0.2),
    Dense(128, activation="relu"),
    Dropout(0.2),
    Dense(10, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

st.write("Training model...")

history = model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=128,
    validation_split=0.2,
    verbose=1
)

st.success("Training complete ✔️")

# ------------------------------------------------
# GRAPH SECTION
# ------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12,4))

# Accuracy
ax[0].plot(history.history["accuracy"], label="Training Accuracy")
ax[0].plot(history.history["val_accuracy"], label="Validation Accuracy")
ax[0].set_title("Accuracy")
ax[0].set_xlabel("Epochs")
ax[0].set_ylabel("Accuracy")
ax[0].legend()
ax[0].grid(True)

# Loss
ax[1].plot(history.history["loss"], label="Training Loss")
ax[1].plot(history.history["val_loss"], label="Validation Loss")
ax[1].set_title("Loss")
ax[1].set_xlabel("Epochs")
ax[1].set_ylabel("Loss")
ax[1].legend()
ax[1].grid(True)

st.pyplot(fig)