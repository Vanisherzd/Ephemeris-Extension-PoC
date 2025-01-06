# Ephemeris Extension Attack: Bypassing GPS Time Verification on iOS Systems

## Researchers
Qi-Jie Huang, Zhen-Dong Lai, Hong-Bin Li, Jieh-Cian Wu  
Department of Computer and Communication Engineering  
National Kaohsiung University of Science and Technology  

---

## Description
A vulnerability exists in the GPS module of iOS systems (versions 13 to 18), allowing attackers to exploit the **Ephemeris Extension Method** to generate fake GPS signals synchronized with the current time. This bypasses the time verification mechanism, causing the device to accept incorrect geographic location data. This attack can deceive GPS-dependent applications such as **navigation software**, **location-based verification services**, and **Apple CarPlay**.

---

## Experiment Video
The following video demonstrates the Ephemeris Extension Attack on iOS systems:  

[![Watch the demonstration](https://img.youtube.com/vi/TGCezlx4FQI/0.jpg)](https://youtu.be/TGCezlx4FQI)

---

## Experiment Results
The following image shows the experimental results of the Ephemeris Extension Attack:

![Experiment Results](./Result%20includes%20iPhone%20and%20Air%20Pods%20Pro%202.png)

### Key Points:
- **Original Location:** Kaohsiung, Taiwan (22°45'N, 120°20'E)  
- **Spoofed Location:** Washington, D.C., USA (38°53'N, 77°2'W)  
- **Affected Systems:**
  - iPhone’s “Find My” feature displayed the spoofed location.
  - AirPods Pro 2, with built-in location tracking, also reflected the altered GPS data.

---

## Attack Type
**Wireless Radio Frequency (RF) Signal Spoofing**

---

## Affected Products
- **Product Name:** iOS Systems  
- **Versions:** iOS 13 to iOS 18  
- **Developer/Manufacturer:** Apple Inc.  
- **Website:** [https://www.apple.com](https://www.apple.com)

---

## Vulnerability Details
Attackers can exploit this vulnerability using the following steps:

1. **Obtain and Modify Ephemeris Data:**  
   Download GPS navigation data from public sources (e.g., NASA CDDIS) and modify it to extend the time frame. The starting time for this experiment was set to **UTC+0, September 27, 8:48**.

2. **Generate Fake GPS Signals:**  
   Use open-source tools such as `gps-sdr-sim` to create a fake GPS signal file (`gpssim.bin`) based on the modified ephemeris data.

3. **Transmit the Spoofed Signal:**  
   Deploy Software-Defined Radio (SDR) devices such as BladeRF xA4 to broadcast the fake GPS signals over the L1 frequency band to the target iOS devices.

4. **Achieve Location Spoofing:**  
   Target devices will process the fake signals, leading to incorrect location and time synchronization.

---

## Experiment Timeline
- **17 Seconds:** Normal GPS signals began to be interfered with.  
- **31 Seconds:** The spoofed GPS signal fully replaced the original, and the location was altered.  

---

## Impact
- **Confidentiality (C):** Low (mainly affects location accuracy).  
- **Integrity (I):** High (can result in tampering with location-based business processes).  
- **Availability (A):** High (may disrupt the functionality of navigation and verification services, including Apple CarPlay).

---

## CVSS v3.1 Vector
`AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H`

---

## CWE Types
- **CWE-290:** Authentication Bypass by Spoofing  
- **CWE-295:** Improper Certificate Validation  

---

## Evidence
- **Experiment Video:** [Watch the demonstration](https://youtu.be/TGCezlx4FQI)  
  Demonstrates the attack process and its effects on iOS devices, including incorrect location data in Apple CarPlay.  
- **Test Report:** Detailed in "A Study of GPS Spoofing Attack to Mobile Terminals," supported with experimental results showing the vulnerability's impact on iOS devices.

---

## Reference
Huang, Qi-Jie. "A Study of GPS Spoofing Attack to Mobile Terminals." Master's Thesis, National Kaohsiung University of Science and Technology, July 2024.  

---

## Additional Notes
The research was conducted using BladeRF xA4 as the SDR device and `gps-sdr-sim` for generating spoofed GPS signals. Experiments were performed in both indoor and outdoor environments, confirming the effectiveness and broad applicability of the Ephemeris Extension Attack.

---
