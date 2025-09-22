# Ephemeris Extension Abuse on Android Devices

## Researchers
Qi-Jie Huang, Zhen-Dong Lai, Yu-Han Liu, Jieh-Cian Wu  
Department of Computer and Communication Engineering  
National Kaohsiung University of Science and Technology

---

## Abuse Scenario Summary
Android 11–14 phones faithfully ingest GPS L1 ephemeris frames that comply with the ICD. When an attacker radiates forged frames whose time-of-clock and time-of-ephemeris fields are **artificially extended**, the handset maintains navigation fixes sourced entirely from spoofed satellites. This is an abuse of GNSS trust assumptions rather than a defect in the Android OS.

---

## Distinguishing Factors
- **Standards-conforming broadcast:** The spoofed message passes the parity and structure checks implemented inside GNSS chipsets.
- **Radio-only capability required:** Adversaries need SDR hardware and RF access; no exploit code executes on Android.
- **Abuse of timing slack:** Extending ephemeris validity shifts the acceptable window without modifying firmware.

---

## Reproduction Pipeline
1. Collect RINEX navigation data (BRDC/BRDM) from NASA CDDIS or other MGEX mirrors.
2. Run `python3 ephemeris_extension.py --rinex <file> --offset-hours 2` to build a spoof-ready navigation set.
3. Generate IQ samples with `gps-sdr-sim` or the in-repo `BDS-SDRSIM` simulator (for BeiDou or multi-constellation comparison).
4. Replay the IQ stream over L1 using a bladeRF xA4, HackRF, or similar SDR.
5. Monitor Android Auto, Google Maps, or custom location-based apps to observe coerced coordinates and time.

---

## Observed Impact and Limitations
- **Integrity:** Navigation routes, ride-hailing pickup points, and time-based one-time passwords relying on GPS can be steered off-course.
- **Availability:** Receivers may become stuck on spoofed satellites, delaying recovery after transmission stops.
- **Constraints:** Requires line-of-sight and careful gain control. Multi-constellation devices may recover faster if other constellations remain authentic.

---

## Tooling Notes
- `ephemeris_extension.py` clones the most recent hour block, advances TOC/TOE by a configurable offset, and saves the result for simulators.
- `BDS-SDRSIM` offers a BeiDou baseband generator that shares the same workflow, making it straightforward to test cross-constellation defences.

---

## Reference Material
- Huang, Qi-Jie. *A Study of GPS Spoofing Attack to Mobile Terminals.* Master's Thesis, National Kaohsiung University of Science and Technology, July 2024.
- Demonstration video: [Android Auto spoofing sequence](https://youtu.be/Zb3lNryc4sc).

All experiments were performed in controlled environments with regulatory compliance.

---
