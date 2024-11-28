# Real-Time Fall Detection
![GitHub contributors](https://img.shields.io/github/contributors/tonlongthuat/YOLOv8-MultiPerson-Fall-Detection)

A robust, IoT-based fall detection system utilizing YOLOv11 and ESP32-CAM for real-time monitoring in multi-person environments. This project captures image streams from ESP32, processes them server-side with Python, and uses advanced detection algorithms to identify falls accurately. With real-time streaming and analysis, the system is well-suited for continuous monitoring in healthcare, eldercare, and security applications, ensuring efficient incident detection and response.
## Project Description

This system is designed to detect falls by capturing and analyzing live images transmitted from ESP32 to a server, leveraging the YOLOv11 object detection model. Unlike traditional pose-specific models, YOLOv11 excels in recognizing multiple individuals simultaneously, enhancing the accuracy of fall detection in crowded environments.

Key components of the project:
- **ESP32**: Streams image data over Wi-Fi to a server for processing.
- **YOLO**: Employs the `ultralytics` YOLOv11 model to detect and assess activity, allowing accurate identification of falls within the frame.
- **Python**: Manages image retrieval, fall detection algorithms, and data handling.
- **Flask**: Hosts a web interface for easy access to live monitoring and system outputs.
- **Multithreading**: Ensures seamless operation by handling tasks like data streaming, fall detection, and web service delivery concurrently.

This system combines edge computing with advanced detection algorithms to deliver efficient and reliable fall detection. Its capability to monitor multiple subjects simultaneously enhances safety in healthcare and residential settings, significantly improving response times and reducing fall-related risks.
## Requirements

To run this project, you will need the following hardware and software:

### Hardware:
- **ESP32**: Used for capturing and streaming images over Wi-Fi.
- **Camera Module**: Integrated with the ESP32 to capture live images.
- **Computer or Server**: Running Python for image processing and fall detection.

### Software:
- **Python 3.x**: Make sure Python 3.x is installed on your system.
- **ESP32 Camera Library**: The appropriate library and setup to capture and stream images from the ESP32.

### How to Use the Project:
To use the projects, follow these steps:

1. **Clone the project from GitHub:**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/tonlongthuat/Real-Time-Fall-Detection.git

2. **Install dependencies:**
   
   To install the necessary Python libraries, run the following command:

   ```bash
    pip install -r requirements.txt

3. **Configure ESP32 (In case you don't want to use the ESP32, just use upload file feature):**

   - **Module Requirements**: Ensure you are using the ESP32 AI Thinker module for compatibility.

   - **Library Installation**: Install the necessary libraries by including the following in your Arduino IDE:

     ```cpp
     #include <WiFi.h>
     #include <esp_camera.h>
     #include <WebServer.h>
     ```

   - **Wi-Fi Credentials**: Modify the user credentials in your code as follows:

     ```cpp
     const char* ssid = "YOUR_SSID";
     const char* password = "YOUR_PASSWORD";
     ```

   - **Firmware Upload**: Upload your firmware using the Arduino IDE. Open the Serial Monitor (baud rate 115200) to obtain the assigned IP address.

   - **Python Integration**: Update your Python script to replace the placeholder IP address with the ESP32's actual IP address to ensure communication.



