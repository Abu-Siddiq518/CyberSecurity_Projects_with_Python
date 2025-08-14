
# 🖥️ Python Keylogger (Ethical Use Only)

A simple, modular Python-based keylogger designed for **educational and authorized security testing**.  
It records keystrokes, including special keys, and saves them to a timestamped log file for later analysis.

---

## 📌 Overview
This project demonstrates how keystroke logging works in a controlled lab environment.  
It uses the `pynput` library to capture keyboard input and logs the data to a local file.  
**⚠️ Disclaimer:** This tool is intended **only** for systems you own or have permission to test. Unauthorized use is illegal.

---


## 📂 Project Structure
python-keylogger/
│
├── main.py # Entry point to start the keylogger
├── logger/
│ ├── init.py
│ ├── key_capture.py # Captures and buffers keystrokes
│ ├── file_writer.py # Saves buffered keys to a file with timestamps
└── logs/ # Stores generated log files

## Sample Image 
<img width="1556" height="897" alt="Screenshot 2025-08-13 123116" src="https://github.com/user-attachments/assets/ebb03b63-0275-4dc3-94e1-57c05fc49cc9" />
