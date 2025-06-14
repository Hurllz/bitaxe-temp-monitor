# Bitaxe Temperature Monitor and Auto-Tuner

This project contains a Python-based monitoring and auto-tuning application for the Bitaxe Gamma 601 Bitcoin solo miner. This tool dynamically adjusts operating frequency and voltage to achieve optimal hash rate while preventing overheating.

## Overview

The **Bitaxe Temp Monitor & Auto-Tuner** continuously polls the Bitaxe's `/api/system/info` endpoint to monitor current temperature, hash rate, and voltage. Based on configurable parameters (target temperature, interval, voltage step, etc.), the script automatically adjusts:

- **Frequency**: Decreases frequency if the temperature exceeds the target or increases it if the temperature is well below the target.
- **Voltage**: If frequency adjustments alone are insufficient or at their limits, voltage is also adjusted within safe operating ranges.

The app aims to maximize the miner's hash rate while maintaining stable and safe operation.

## Features

- **Automatic Auto-Tuning**: Continuously monitors the Bitaxe's performance and temperature.
- **Dynamic Adjustment**: Automatically adjusts frequency and voltage in real-time based on temperature and hash rate.
- **Graceful Shutdown**: Listens for interrupt signals (Ctrl+C) and exits safely.
- **Customizable Parameters**: Easily modify settings such as target temperature, sample interval, and safe operating limits.
- **Cross-Platform Support**: Works on **Windows**, **Linux**, **macOS**, and **Raspberry Pi**.

## Requirements

- **Python 3.x** (tested with Python 3.9+)
- Required Python modules:
  - `requests`
  - `pandas`
  - `tkinter`  
    - Pre-installed on Windows  
    - May require manual installation on Linux/macOS

---

## Installation

### 🪟 Windows

1. Open Command Prompt as Administrator.
2. Clone the repository:

   ```bash
   git clone https://github.com/hurllz/bitaxe-temp-monitor.git
   cd bitaxe-temp-monitor
   ```

3. Install dependencies:

   ```bash
   pip install requests pandas
   ```

4. Run the application:

   ```bash
   python main.py
   ```

---

### 🍎 macOS

1. Open a terminal window.
2. Install Homebrew (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. Install Python 3 and Tkinter:

   ```bash
   brew install python
   brew install tcl-tk
   ```

4. Add this to your shell profile (`~/.zshrc`, `~/.bash_profile`, or `~/.bashrc`):

   ```bash
   export PATH="/opt/homebrew/opt/python/libexec/bin:$PATH"
   export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
   export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
   export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"
   ```

5. Apply changes:

   ```bash
   source ~/.zshrc   # or ~/.bash_profile
   ```

6. Clone the project:

   ```bash
   git clone https://github.com/hurllz/bitaxe-temp-monitor.git
   cd bitaxe-temp-monitor
   ```

7. Install dependencies:

   ```bash
   pip3 install requests pandas
   ```

8. Run the application:

   ```bash
   python3 main.py
   ```

---

### 🐧 Linux

1. Open a terminal window.
2. Clone the repository:

   ```bash
   git clone https://github.com/hurllz/bitaxe-temp-monitor.git
   cd bitaxe-temp-monitor
   ```

3. Install dependencies:

   ```bash
   sudo apt-get install python3-tk
   pip3 install requests pandas
   ```

4. Run the application:

   ```bash
   python3 main.py
   ```

---

### 🍓 Raspberry Pi (RPi 5)

1. Open a terminal window.
2. Clone the repository:

   ```bash
   git clone https://github.com/hurllz/bitaxe-temp-monitor.git
   cd bitaxe-temp-monitor
   ```

3. Install dependencies:

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-tk
   pip3 install --upgrade pip
   pip3 install pandas requests
   ```

4. Run the application:

   ```bash
   python3 main.py
   ```

---

## Usage

After launching the app, scan your network or manually add your Bitaxe's IP. You can specify initial voltage, frequency, target temperature, and the interval for autotuning using the GUI or the `config.json` file.

---

## How It Works

1. **Initialization**: Applies the initial voltage and frequency settings to the Bitaxe.
2. **Autotuning Loop**:  
   - Continuously polls the Bitaxe API.
   - Decreases frequency or voltage if the temperature exceeds the target.
   - Increases frequency or voltage if temperature is well below target and hashrate is low.
3. **Dynamic Adjustment**: Applies updated settings in real-time.
4. **Graceful Exit**: On shutdown, the current state is logged and the app exits cleanly.

---

## Disclaimer

**WARNING:** This tool modifies hardware settings and may stress-test your Bitaxe. Although safeguards are in place, running the miner outside its standard operating parameters can pose risks. Use this script at your own risk. The authors are not responsible for any damage to your hardware.

---

## Contributors

- **Birdman332** (Reddit): Created GUI management features.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## Inspirational Shoutouts

The benchmark tool below is highly recommended for baselining and optimizing your miner's tuning:

1. **WhiteyCookie**: [Bitaxe-Hashrate-Benchmark](https://github.com/WhiteyCookie/Bitaxe-Hashrate-Benchmark)  
2. **mrv777**: [Forked Bitaxe Benchmark](https://github.com/mrv777/bitaxe-hashrate-benchmark)

---

## License

This project is licensed under the [MIT License](LICENSE).
