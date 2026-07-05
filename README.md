# IoT and Computer Vision-Based Smart Stick for Visually Impaired Persons

## Overview

This project presents an **IoT and Computer Vision-Based Smart Stick for Visually Impaired Persons** designed to assist visually impaired users in identifying surrounding objects and obstacles. The system combines **ESP32-based hardware**, **ESP32-CAM video streaming**, **YOLOv8 object detection**, **audio feedback through DFPlayer Mini**, and **ultrasonic sensing** as a backup obstacle detection mechanism.

The smart stick works in **two modes**:

* **Online Mode:** Uses the ESP32-CAM and a laptop running a YOLOv8 model to detect objects in real time. Detected objects are announced to the user through pre-recorded voice messages.
* **Offline Mode:** If the internet/mobile hotspot connection is lost for a few seconds, the system automatically switches to ultrasonic-based obstacle detection and alerts the user using a buzzer.

This makes the stick a low-cost assistive solution that combines **computer vision, IoT communication, and embedded sensing** for safer mobility.


## Objectives

The main objectives of this project are:

* To help visually impaired persons detect and identify nearby objects.
* To provide **audio-based guidance** using recorded voice alerts.
* To integrate **computer vision and IoT** into a portable smart stick.
* To provide a **backup obstacle detection system** when online object recognition is unavailable.
* To create a practical and affordable assistive mobility device.

---

## Features

* **Real-time object detection** using YOLOv8 and ESP32-CAM.
* **Voice output** for detected objects using DFPlayer Mini and speaker.
* **Support for COCO classes** with pre-recorded MP3 voice labels.
* **Unknown object alert** if the object does not match a known class.
* **Automatic fallback to ultrasonic obstacle detection** when online mode is unavailable.
* **Buzzer-based distance alert** for nearby obstacles.
* **ESP32-based control system** for handling communication and outputs.
* **Portable battery-powered design** using a power bank.

---

## System Architecture

The system consists of the following major parts:

### 1. Vision and Detection Unit

* **ESP32-CAM** captures live video and streams it over the local network.
* A **laptop** receives the video stream and processes frames using **OpenCV + YOLOv8n**.
* The detection result is sent to the ESP32.

### 2. Audio Feedback Unit

* **ESP32** receives the detected object label.
* It triggers the **DFPlayer Mini** to play a corresponding audio file from the SD card.
* The **speaker** announces the object name to the user.

### 3. Obstacle Detection Backup Unit

* If the online system disconnects or becomes unavailable for about 5 seconds:

  * The **ultrasonic sensor** starts measuring distance.
  * The **buzzer** alerts the user about nearby obstacles.

---

## Required Components

The following components are used in this project:

1. ESP32-CAM
2. ESP32
3. DFPlayer Mini
4. SD Card
5. Speaker
6. Power Bank (10000 mAh)
7. ON/OFF Button
8. Capacitors:

   * Two × 470 µF
   * One × 47 µF
9. Jumper wires
10. Type-B Micro USB cable
11. Vero board
12. Double-sided tape
13. Glue gun
14. Soldering material
15. Box for fixing hardware on the stick
16. PVC pipe with wooden base
17. Laptop for ESP32-CAM video processing
18. Ultrasonic sensor
19. Buzzer

---

## Working Principle

## Step 1: Power ON

When the ON/OFF button is pressed, both the **ESP32-CAM** and **ESP32** are powered on.

## Step 2: Network Connection

Turn on the mobile hotspot and connect the following devices to the **same network**:

* ESP32-CAM
* ESP32
* Laptop

## Step 3: Camera Stream Check

The ESP32-CAM provides a live video stream through its IP address.
The user checks the stream by entering the ESP32-CAM IP in a browser using HTTP.

## Step 4: System Initialization

After pressing the **ENB button** of the ESP32, the system plays startup voice files such as:

* `001.mp3`
* `002.mp3`

These indicate that the smart stick system has started successfully.

## Step 5: Object Detection

* The laptop reads the video stream from the ESP32-CAM.
* Frames are processed using **OpenCV** and the **YOLOv8n model**.
* The detected object label is sent to the ESP32.
* The ESP32 maps the object label to a corresponding MP3 file on the SD card.
* The DFPlayer Mini plays the audio file through the speaker.

### Audio File Mapping

* `003.mp3` to `082.mp3` → Pre-recorded voice labels for **COCO object classes**
* `083.mp3` → Played when an **unknown object** is detected

## Step 6: Offline Backup Mode

If the mobile hotspot/network is unavailable for about **5 seconds**, the system switches to backup mode:

* The **ultrasonic sensor** measures the distance to obstacles.
* The **buzzer** gives a warning beep every **1.5 seconds** when an obstacle is detected.

---

## Hardware Connections

# ESP32-CAM

* Connect directly to the main power source (power bank).
* Connect **VCC (5V)** and **GND** with a **470 µF capacitor** for power stabilization.

# ESP32 Connections

## DFPlayer Mini to ESP32

* **DFPlayer RX** → ESP32 **TX2 (Pin 17)** through a **1 kΩ resistor**
* **DFPlayer TX** → ESP32 **RX2 (Pin 16)**
* **DFPlayer VCC** → ESP32 **3.3V**
* **DFPlayer GND** → ESP32 **GND**
* Add a **470 µF capacitor** across DFPlayer Mini power lines for stable operation

## Speaker

* Connect the speaker to the **SPK1/SPK2** pins of the DFPlayer Mini

## Ultrasonic Sensor

* **Trig** → ESP32 **Pin 5**
* **Echo** → ESP32 **Pin 18**
* Use a **voltage divider** on Echo pin for ESP32 protection
* **VCC/GND** connected to ESP32 power with a **47 µF capacitor**

## Buzzer

* **Buzzer VCC / Positive** → ESP32 **Pin 4**
* **Buzzer GND** → ESP32 **GND**

## LED

* Built-in LED on **Pin 2**
* It turns ON when the ESP32 receives a detection result from the laptop
* An external LED can also be connected to **Pin 2** if required

---

## Software and Tools Used

* **Arduino IDE** / ESP32 programming environment
* **Python**
* **OpenCV**
* **YOLOv8n**
* **ESP32-CAM Web Stream**
* **DFPlayer Mini audio playback**
* **Mobile hotspot / local Wi-Fi network**

---

## Project Workflow

1. Power ON the ESP32 and ESP32-CAM.
2. Connect laptop, ESP32, and ESP32-CAM to the same hotspot/network.
3. Start the ESP32-CAM stream.
4. Run the Python object detection code on the laptop.
5. Detect objects using YOLOv8n.
6. Send detection labels to ESP32.
7. ESP32 plays the corresponding voice message via DFPlayer Mini.
8. If the network fails, switch to ultrasonic obstacle detection mode.
9. Alert the user using the buzzer.

---

## Applications

This project can be used in:

* **Assistive technology for visually impaired persons**
* **Smart mobility aids**
* **IoT and embedded system research**
* **Computer vision-based safety devices**
* **Low-cost intelligent walking assistance systems**

---

## Advantages

* Provides real-time object awareness to visually impaired users
* Combines both **vision-based** and **sensor-based** detection
* Offers voice feedback instead of requiring visual output
* Uses low-cost and widely available hardware components
* Includes a backup mode for safer operation during network failure

---

## Limitations

* The object detection model currently depends on a **laptop** for processing
* Online mode requires all devices to remain on the **same network**
* Performance depends on camera quality, lighting conditions, and network stability
* Unknown objects are not named specifically; only a generic unknown-object alert is given

---

## Future Improvements

The project can be improved further by:

* Running object detection directly on an edge AI device for full portability
* Adding **GPS tracking** for navigation support
* Adding **text-to-speech navigation instructions**
* Improving offline mode with additional sensors
* Integrating **face recognition**, **currency recognition**, or **signboard reading**
* Designing a compact PCB and enclosure for better portability


Conclusion

The **IoT and Computer Vision-Based Smart Stick for Visually Impaired Persons** is an assistive embedded system that enhances mobility and safety for visually impaired individuals. By combining **ESP32-CAM video streaming**, **YOLOv8 object detection**, **ESP32 control**, **DFPlayer voice feedback**, and **ultrasonic obstacle sensing**, the system provides both object recognition and obstacle warning capabilities. The inclusion of an offline backup mode increases reliability and makes the solution more practical for real-world use.


 Authors

**Project Title:** IoT and Computer Vision-Based Smart Stick for Visually Impaired Persons

You can add your names here, for example:

* Muhammad Amir Mushtaq
*Shanza Shafiq



This project is for **academic and research purposes**.
You may modify and extend it for educational use.
