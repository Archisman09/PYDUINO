# **PYDUINO – Hand Gesture Controlled LEDs and Servo using OpenCV and Arduino**  

### **Overview**  
PYDUINO is an innovative project that combines **computer vision (OpenCV)**, **mediapipe**, and **Arduino programming** to create a gesture-controlled system. By using **hand-tracking and finger recognition**, this project can control **LEDs** and **servo motors** via **Bluetooth communication (HC-05)**, bridging software and hardware interaction seamlessly.  

---

### **Key Features**  
- **Finger Tracking and Recognition** – Uses OpenCV and Mediapipe to detect and track hand landmarks in real-time.  
- **LED Control** – Five LEDs are controlled by detecting the number of raised fingers.  
- **Servo Motor Control** – Servo motor direction is controlled by the distance between the thumb and index finger.  
- **Bluetooth Communication** – Data is sent to Arduino Nano using an HC-05 Bluetooth module.  
- **On-Screen Feedback** – Displays finger count, joint coordinates, and FPS (frames per second) on the screen.  

---

### **Technologies Used**  
- **Languages:** Python, Arduino (C++)  
- **Libraries:**  
  - OpenCV (cv2)  
  - Mediapipe  
  - Numpy  
  - Pyserial (for serial communication)  
  - Math and Time modules  

---

### **How It Works**  
1. **Finger Recognition:**  
   - The webcam detects hand landmarks using **Mediapipe Hand Tracking**.  
   - Finger positions are analyzed to count how many fingers are raised.  
   - The servo motor's angle is controlled by measuring the distance between the thumb and index finger.  

2. **Hardware Communication:**  
   - The Python script sends signals to the Arduino via Bluetooth (HC-05).  
   - The Arduino receives the data and adjusts the LED lights or the servo motor based on the input.  

---

### **Hardware Requirements**  
- Arduino Nano  
- HC-05 Bluetooth Module  
- 5 LEDs  
- Servo Motor (SG90 or similar)  
- Resistors and Breadboard  
- Jumper Wires  

---

### **Project Files**  
- **Pyduino code.py** – Python script for hand tracking, finger detection, and serial communication.  
- **Servo.ino** – Arduino code for receiving signals and controlling LEDs and servo motors.  

---

### **Setup and Installation**  

1. **Install Required Packages**  
```bash
pip install opencv-python mediapipe numpy pyserial
```  

2. **Upload Arduino Code**  
- Connect your Arduino Nano.  
- Open **Servo.ino** in Arduino IDE.  
- Upload the code to the Arduino.  

3. **Run the Python Script**  
```bash
python Pyduino code.py
```  
- Ensure Bluetooth communication is established between your PC and HC-05.  

---

### **Demo**  
- Open the webcam and show your hand.  
- Raising fingers will turn LEDs on or off.  
- Moving the thumb closer to or away from the index finger will control the servo motor's angle.  

---

### **License**  
This project is licensed under the **MIT License** – feel free to modify and distribute.  

---

### **Contact**  
**Archisman Kundu**  
📩 Email: archismankundu04@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/archisman-kundu-020055269/)  

---
