# 🧠 DigitVision

## Professional Handwritten Digit Recognition System

DigitVision is an AI-powered handwritten digit recognition application built using Deep Learning and Computer Vision technologies. The project uses a Convolutional Neural Network (CNN) trained on the MNIST dataset to recognize handwritten digits drawn by users in real time.

---

## 🚀 Features

* Real-time handwritten digit recognition
* Interactive drawing canvas
* CNN-based deep learning model
* Multi-page Streamlit dashboard
* Training analytics visualization
* Modern dark-themed user interface
* Model architecture overview
* Performance metrics dashboard

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### Deep Learning

* TensorFlow
* Keras

### Computer Vision

* OpenCV

### Data Processing

* NumPy

### Visualization

* Matplotlib

---

## 🧠 Model Architecture

The project uses a Convolutional Neural Network (CNN) consisting of:

* Conv2D Layer (32 Filters)
* MaxPooling Layer
* Conv2D Layer (64 Filters)
* MaxPooling Layer
* Flatten Layer
* Dense Layer (128 Neurons)
* Dropout Layer
* Output Layer (10 Classes)

---

## 📊 Dataset

The model is trained on the MNIST Handwritten Digit Dataset.

Dataset Statistics:

* 70,000 handwritten digit images
* 10 digit classes (0–9)
* Image Size: 28 × 28 pixels
* Grayscale images

---

## 📈 Model Performance

| Metric    | Value |
| --------- | ----- |
| Accuracy  | 99.1% |
| Optimizer | Adam  |
| Epochs    | 10    |
| Dataset   | MNIST |

---

## 📂 Project Structure

DigitVision/

├── app.py

├── mnist_trained_model.h5

├── training_history.pkl

├── requirements.txt

├── README.md

├── utils/

│ └── styling.py

└── pages/

├── 2_Predict.py

├── 3_Analytics.py

├── 4_Model.py

└── 5_About.py

---

## ⚙️ Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/DigitVision.git

cd DigitVision

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

---

## 🎯 Project Objectives

* Demonstrate Deep Learning concepts
* Implement CNN-based image classification
* Explore Computer Vision workflows
* Build interactive AI applications
* Deploy machine learning models using Streamlit

---

## 📸 Application Screenshots

Add screenshots here before publishing.

Example:

* Dashboard Page
* Prediction Page
* Analytics Dashboard
* Model Architecture Page
* About Page

---

## 👨‍💻 Author

Yukthesh

DigitVision was developed as a portfolio project to demonstrate practical implementation of Deep Learning, Computer Vision, and AI-powered web applications.
