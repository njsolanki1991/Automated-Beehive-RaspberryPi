## Automated Beehive Monitoring System  

This project utilizes Raspberry Pi 3B+ and various sensors to monitor and analyze beehive conditions. Sensor data is collected and stored in Firebase Cloud Firestore for further analysis.  

### **Features**  
- **Environmental Monitoring:** Temperature, humidity, air pressure (DHT22, BME280).  
- **Air Quality Analysis:** Gas detection (MQ135).  
- **Hive Activity Tracking:** Sound analysis (USB mic), weight measurement (Load cells + HX711).  
- **Hive Orientation:** Gyroscope & accelerometer (MPU-6050).  
- **GPS Tracking:** Hive location monitoring (Neo 6M).  
- **Visual Monitoring:** Night vision camera.  

### **Hardware Used**  
- Raspberry Pi 3B+  
- Various sensors (MQ135, DHT22, MPU6050, BME280, USB mic, Neo 6M, etc.)  
- ADC modules (MCP3008, HX711)  

### **Software Used**  
- **OS:** Raspbian Buster  
- **Programming:** Python 3  
- **Database:** Firebase Cloud Firestore  
- **Schematics:** Fritzing  

### **Modifications from Initial Design**  
- **KY-037 Sound Sensor** replaced with a **USB mic** for better accuracy.  
- **MPU-6050 (Gyroscope & Accelerometer)** added for orientation tracking.  
- **Connections moved from breadboard to matrix board** for robustness.  

### **Setup & Installation**  
1. Install Raspbian Buster on Raspberry Pi.  
2. Connect sensors as per circuit schematics.  
3. Install required Python libraries.  
4. Configure Firebase Cloud Firestore.  
5. Run the data collection scripts.  

### **Challenges & Improvements**  
- Improved sound detection by replacing KY-037 with a USB mic.  
- Enhanced durability with matrix board connections.  
- Added orientation tracking for better hive monitoring.  

This project aims to provide real-time insights into beehive conditions, ensuring better management and health tracking. 🚀🐝
