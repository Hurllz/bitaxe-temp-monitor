# How to Run the Web Interface (Headless Mode)

This guide explains how to launch the Bitaxe-temp-monitor application as a local web server ("headless mode"). This allows you to interact with the interface using a web browser on the same machine.

-----

## Prerequisites

  * Python 3 and `pip` are installed on your system.
  * You have downloaded the Bitaxe project files.

-----

## Step 1: Install Dependencies

Before you can run the application, you need to install its required Python packages.

1.  **Open a terminal** (like Command Prompt, PowerShell, or Terminal).

2.  **Navigate to the project directory** where you saved the files.

    ```bash
    cd /path/to/your/bitaxe-temp-monitor
    ```

3.  **Install the dependencies** using `pip`.

    ```bash
    pip install -r requirements.txt
    ```

-----

## Step 2: Launch the Web Server

Now you can run the main script with the `headless` argument to start the local server.

1.  **In the same terminal**, run the following command:

    ```bash
    python3 main.py headless
    ```

2.  You should see output indicating that the server is active and listening for connections, similar to this:

    ```
    Starting Flask web server in headless mode...
     * Running on http://127.0.0.1:5000
    ```

The server is now running. **Keep this terminal window open.**

-----

## Step 3: Access the Web Interface

With the server running, you can access the interface in your browser.

1.  **Open your preferred web browser** (like Chrome, Firefox, or Safari).

2.  **Navigate to the following address** in the address bar:

    ```
    http://localhost:5000
    ```

    Alternatively, you can use `http://127.0.0.1:5000`.

The Bitaxe web interface should now load in your browser tab.

-----

## How to Stop the Server

When you are finished, you can easily shut down the web server.

1.  Go back to the terminal window where the server is running.
2.  Press **`Ctrl+C`** on your keyboard.

The server will stop, and the terminal will return to a normal command prompt.