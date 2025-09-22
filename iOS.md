# Ephemeris Extension Abuse on iOS Devices

## Researchers
Qi-Jie Huang, Zhen-Dong Lai, Yu-Han Liu, Jieh-Cian Wu  
Department of Computer and Communication Engineering  
National Kaohsiung University of Science and Technology

---

## Overview
The Ephemeris Extension Method (EEM) demonstrates that iOS 13–18 devices faithfully trust GPS navigation frames that align with the specification. By forging frames with extended validity windows, spoofed satellites remain authoritative long enough to mislead Apple Maps, CarPlay, and time-sensitive apps. This behaviour reflects the GNSS trust model rather than an exploitable iOS bug.

---

## Characteristics of the Abuse
- **Specification-aligned frames:** The forged ephemerides carry valid parity and timing fields; receivers accept them as if they originated from space.
- **Radio-layer dependency:** The attack happens entirely in RF. No code executes on iOS and no sandbox or entitlement is bypassed.
- **Time-extension trick:** Adjusting Time of Clock (TOC) and Time of Ephemeris (TOE) keeps spoofed data inside the acceptance window, even after the original broadcast should have expired.

---

## Workflow
1. Download RINEX navigation data (BRDC/BRDM) for the target day.
2. Execute `python3 ephemeris_extension.py --rinex <file> --offset-hours 2` to clone and shift the latest navigation block.
3. Convert the modified ephemeris into IQ samples using `gps-sdr-sim` or the co-hosted `BDS-SDRSIM` (for BeiDou or multi-GNSS experiments).
4. Replay the samples on an SDR (bladeRF xA4, HackRF, USRP) centred at 1575.42 MHz.
5. Observe iOS devices tracking the spoofed satellites and adopting falsified position/time.

---

## Impact Snapshot
- **Integrity:** Navigation, automation workflows, and time-synchronised apps may follow attacker-chosen coordinates and timestamps.
- **Availability:** Spoofing can delay reacquisition of authentic satellites after the broadcast stops.
- **Limitations:** Requires close-range RF control, lab licensing, and often shielding to avoid affecting bystanders. Multi-constellation receivers can fall back to real signals if the attacker does not jam them.

---

## Tooling Highlights
- `ephemeris_extension.py` now exposes CLI flags for the input file, output path, and offset, avoiding hard-coded directories.
- `BDS-SDRSIM` enables BeiDou B1I simulations using the same workflow; mixing GPS and BeiDou spoofing helps evaluate cross-constellation defences on iOS.

---

## Evidence
- Demonstration video (iOS focus): [https://youtu.be/TGCezlx4FQI](https://youtu.be/TGCezlx4FQI)
- Demonstration video (AirPods Pro 2 / multi-device): [https://youtu.be/Zb3lNryc4sc](https://youtu.be/Zb3lNryc4sc)

---

## Reference
- Huang, Qi-Jie. *A Study of GPS Spoofing Attack to Mobile Terminals.* Master's Thesis, National Kaohsiung University of Science and Technology, July 2024.

---

## Repository Usage
```bash
git clone https://github.com/YourRepository/Ephemeris-Extension-PoC.git
cd Ephemeris-Extension-PoC
python3 ephemeris_extension.py --help
```
Consult the README for simulation guidance and cross-links to `BDS-SDRSIM`.

---
