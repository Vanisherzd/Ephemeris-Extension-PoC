# Ephemeris Extension Attack: Bypassing GPS Time Verification on Mobile Systems

## Researchers
Qi-Jie Huang, Zhen-Dong Lai, Hong-Bin Li, Jieh-Cian Wu  
Department of Computer and Communication Engineering  
National Kaohsiung University of Science and Technology  

---

## Description
A vulnerability exists in the GPS modules of both iOS (versions 13 to 18) and Android (versions 11 to 14) systems, allowing attackers to exploit the **Ephemeris Extension Method** to generate fake GPS signals synchronized with the current time. This bypasses the time verification mechanism, causing devices to accept incorrect geographic location data. Such attacks can deceive GPS-dependent applications, including **navigation software**, **location-based verification services**, **Apple CarPlay**, and **Android Auto**.

---

## Experiment Videos
The following videos demonstrate the Ephemeris Extension Attack on iOS and Android systems:  

1. **iOS Demonstration**  
   [![Watch the iOS demonstration](https://img.youtube.com/vi/TGCezlx4FQI/0.jpg)](https://youtu.be/TGCezlx4FQI)  

2. **Android Demonstration**  
   [![Watch the Android demonstration](https://img.youtube.com/vi/Zb3lNryc4sc/0.jpg)](https://youtu.be/Zb3lNryc4sc)

---

## Attack Type
Wireless Radio Frequency (RF) Signal Spoofing  

---

## Affected Products

### iOS Systems
- **Versions:** iOS 13 to iOS 18  
- **Developer/Manufacturer:** Apple Inc.  
- **Website:** [https://www.apple.com](https://www.apple.com)

### Android Systems
- **Versions:** Android 11 to Android 14  
- **Developer/Manufacturer:** Google LLC  
- **Website:** [https://www.android.com](https://www.android.com)

---

## Vulnerability Details
Attackers can exploit this vulnerability using the following steps:

1. **Obtain and Modify Ephemeris Data:**  
   Download GPS navigation data from public sources (e.g., NASA CDDIS) and modify it to extend the time frame.

2. **Generate Fake GPS Signals:**  
   Use open-source tools such as `gps-sdr-sim` to create a fake GPS signal file (`gpssim.bin`) based on the modified ephemeris data.

3. **Transmit the Spoofed Signal:**  
   Deploy Software-Defined Radio (SDR) devices such as BladeRF xA4 to broadcast the fake GPS signals over the L1 frequency band to the target devices.

4. **Achieve Location Spoofing:**  
   Target devices will process the fake signals, leading to incorrect location and time synchronization.

---

## Impact
- **Confidentiality (C):** Low (mainly affects location accuracy).  
- **Integrity (I):** High (can result in tampering with location-based business processes).  
- **Availability (A):** High (may disrupt the functionality of navigation and verification services, including Apple CarPlay and Android Auto).

---

## CVSS v3.1 Vector
`AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H`

---

## CWE Types
- CWE-290: Authentication Bypass by Spoofing  
- CWE-295: Improper Certificate Validation  

---

## References
1. Huang, Qi-Jie. "A Study of GPS Spoofing Attack to Mobile Terminals." Master's Thesis, National Kaohsiung University of Science and Technology, July 2024.  

2. Experiment videos:  
   - [iOS Demonstration](https://youtu.be/TGCezlx4FQI)  
   - [Android Demonstration](https://youtu.be/Zb3lNryc4sc)

---

## Additional Notes
The research was conducted using BladeRF xA4 as the SDR device and `gps-sdr-sim` for generating spoofed GPS signals. Experiments were performed in both indoor and outdoor environments, confirming the effectiveness and broad applicability of the Ephemeris Extension Attack on both iOS and Android systems, including navigation services like Apple CarPlay and Android Auto.

---
