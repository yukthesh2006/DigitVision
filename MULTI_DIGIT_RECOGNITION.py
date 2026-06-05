import streamlit as st
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import numpy as np
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas
import cv2

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="Multi Digit Recognition", layout="wide")
st.title("Handwritten Number Recognition (0-99)")

# -------------------------------
# LOAD DATASET
# -------------------------------
@st.cache_data
def load_data():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train = x_train.reshape(-1,28,28,1)
    x_test = x_test.reshape(-1,28,28,1)

    y_train = to_categorical(y_train,10)
    y_test = to_categorical(y_test,10)

    return x_train,y_train,x_test,y_test

x_train,y_train,x_test,y_test = load_data()

# -------------------------------
# BUILD CNN MODEL
# -------------------------------
@st.cache_resource
def build_model():

    model = Sequential([
        Conv2D(32,(3,3),activation="relu",input_shape=(28,28,1)),
        MaxPooling2D((2,2)),
        Conv2D(64,(3,3),activation="relu"),
        MaxPooling2D((2,2)),
        Flatten(),
        Dense(128,activation="relu"),
        Dense(10,activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        x_train,
        y_train,
        epochs=5,
        batch_size=128,
        validation_split=0.2,
        verbose=0
    )

    return model

model = build_model()

st.success("Model trained successfully")

# -------------------------------
# DRAWING CANVAS
# -------------------------------
st.subheader("Draw a number (0-99)")

canvas = st_canvas(
    fill_color="black",
    stroke_width=12,
    stroke_color="white",
    background_color="black",
    width=400,
    height=200,
    drawing_mode="freedraw",
    key="canvas"
)

# -------------------------------
# PREDICTION BUTTON
# -------------------------------
if st.button("Predict Number"):

    if canvas.image_data is None:
        st.warning("Draw a number first")

    else:

        img = Image.fromarray(canvas.image_data.astype("uint8")).convert("L")
        img = ImageOps.invert(img)

        img = np.array(img)

        # threshold
        _,thresh = cv2.threshold(img,50,255,cv2.THRESH_BINARY)

        contours,_ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        digits = []

        for contour in contours:

            x,y,w,h = cv2.boundingRect(contour)

            if w*h < 100:
                continue

            digit = thresh[y:y+h,x:x+w]

            digit = cv2.resize(digit,(28,28))

            digit = digit.astype("float32")/255.0

            digit = digit.reshape(1,28,28,1)

            pred = model.predict(digit,verbose=0)

            digit_label = np.argmax(pred)

            digits.append((x,str(digit_label)))

        digits = sorted(digits,key=lambda x:x[0])

        result = "".join([d[1] for d in digits])

        st.success(f"Predicted Number: {result}")