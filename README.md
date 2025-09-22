# Ephemeris Extension Abuse: Demonstrating GNSS Signal Misuse on Mobile Devices

## Researchers
Qi-Jie Huang, Zhen-Dong Lai, Yu-Han Liu, Jieh-Cian Wu  
Department of Computer and Communication Engineering  
National Kaohsiung University of Science and Technology

---

## What This Project Shows
The Ephemeris Extension Method (EEM) is a **signal-spoofing abuse scenario**. It does not exploit a software bug in iOS or Android; instead it repurposes how GNSS receivers legitimately trust freshly broadcast ephemeris data. By stretching the time tags inside a valid-looking navigation message, we can keep spoofed GPS satellites "alive" longer than the GNSS specification anticipates. Mobile devices then continue to produce coherent time and position solutions from forged signals.

---

## Why It Is Classified as Abuse, Not a Vulnerability
- **Specification-compliant inputs:** The forged navigation frames respect GPS ICD structures and parity. Receivers accept them because they have no reason, within the standard, to reject timely ephemerides.
- **No privilege escalation on the platform:** Neither iOS nor Android code is bypassed; radios simply ingest RF that emulates space segment behaviour.
- **Requires RF access:** An adversary must already be capable of radiating on L1, so this is an operational misuse of GNSS trust rather than a patchable OS flaw.

This repo therefore documents the conditions under which EEM can be abused and offers tooling to reproduce the phenomenon in controlled environments.

---

## Demonstration Videos
1. **iOS field test** – [YouTube link](https://youtu.be/TGCezlx4FQI)  
2. **iPhone & AirPods Pro 2 test** – [YouTube link](https://youtu.be/Zb3lNryc4sc)

---

## Attack Workflow
1. **Fetch navigation data** from sources such as NASA CDDIS (RINEX BRDC/BRDM).
2. **Extend the ephemeris lifetime** with the included `ephemeris_extension.py` script, adding a controlled offset to clock parameters.
3. **Synthesize RF samples** using `gps-sdr-sim` or the companion `BDS-SDRSIM` project in this repository to create IQ recordings.
4. **Transmit with SDR hardware** (e.g., bladeRF xA4, HackRF) at the GPS L1 frequency.
5. **Observe spoofed solutions** on iOS 13–18 and Android 11–14 devices, including apps such as Apple CarPlay and Android Auto.

---

## Relation to `BDS-SDRSIM`
The `BDS-SDRSIM` directory provides a BeiDou B1I simulator that shares the same tooling pipeline. While EEM focuses on GPS L1, integrating `BDS-SDRSIM` lets researchers explore multi-constellation spoofing and compare mitigation ideas under identical lab setups. Both projects:
- Consume broadcast ephemerides (RINEX 3.x) and adjust their timing parameters.
- Output baseband IQ suitable for software-defined radios.
- Highlight the trust assumptions GNSS receivers make when presented with syntactically correct navigation frames.

---

## Impact and Practical Constraints
- **Integrity risk:** Location and time can be falsified for dependent services (navigation, geofencing, time-based authentication).
- **Operational challenges:** Requires RF line-of-sight, sufficient power, and careful alignment to avoid detection. Outdoor experiments demand regulatory approval.
- **Mitigation avenues:** Cross-checking with inertial sensors, encrypted signals, assisted-GNSS sanity checks, or multi-constellation consistency testing.

---

## Using the Ephemeris Extension Script
```bash
python3 ephemeris_extension.py --rinex /path/to/brdc1760.24n --offset-hours 2 \
        --workdir /path/to/output
```
- The script clones the final navigation block, extends the time of clock (TOC), time of ephemeris (TOE), and transmission times, then writes a suffixed file ready for simulators.
- Specify an explicit working directory to avoid the historical hard-coded path.

See `python3 ephemeris_extension.py --help` for all options.

---

## Running Simulations
1. Generate the spoofed navigation file with the script above.
2. Use `gps-sdr-sim` or `BDS-SDRSIM` to produce `gpssim.bin` (GPS) or `beidou_b1i.bin` (BeiDou) IQ samples.
3. Replay the IQ file with your SDR transmitter. Tune gain cautiously to maintain lawful emissions.
4. Validate on isolated test devices before attempting any field study.

---

## Research Context
- Huang, Qi-Jie. *A Study of GPS Spoofing Attack to Mobile Terminals.* Master's Thesis, National Kaohsiung University of Science and Technology, July 2024.

Experiments covered indoor offices and controlled outdoor lots. The abuse worked consistently across modern iPhone and Android devices, even when paired with vehicle infotainment systems.

---

## Tests
Run the Markdown hygiene test with:
```bash
pytest
```
The suite ensures documentation code fences remain well-formed.

---
