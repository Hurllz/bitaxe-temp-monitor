Of course. Here is the updated guide with the correct `config.json` example.

-----

# How to Deploy with Docker Compose

This guide explains how to run the Bitaxe application on a Linux server using Docker Compose. This is the recommended method for a stable, long-running deployment, as it handles container creation, networking, and restarting automatically.

-----

## Prerequisites 📋

Before you begin, ensure you have the following set up on your Linux server:

  * You are connected to your server via an SSH session.
  * **Docker** is installed.
  * **Docker Compose** is installed.

-----

## Step 1: Get the Project Files

First, you need to get the application code and configuration files onto your server. The easiest way is to clone the project repository using Git.

1.  **Clone the repository** (replace the URL with the actual project's Git URL):

    ```bash
    git clone https://github.com/your-username/bitaxe-app.git
    ```

2.  **Navigate into the new project directory:**

    ```bash
    cd bitaxe-app
    ```

    This directory should contain your `Dockerfile`, `docker-compose.yaml`, `main.py`, and other necessary files.

-----

## Step 2: Update Your Configuration (optional)

The application uses a `config.json` file for settings. You can edit this file before launching the app if needed.

1.  **Adjust your configuration settings.** This is the default configuration `config.json`.

    ```json
    {
        "voltage_step": 10,
        "frequency_step": 5,
        "monitor_interval": 5,
        "default_target_temp": 50,
        "temp_tolerance": 2,
        "refresh_interval": 5,
        "enforce_safe_pairing": true,
        "daily_reset_enabled": false,
        "daily_reset_time": "03:00",
        "flatline_detection_enabled": true,
        "flatline_hashrate_repeat_count": 5,
        "miners": []
    }
    ```

-----

## Step 3: Launch the Application 🚀

With the files in place, you can now launch the application using a single Docker Compose command.

1.  **Run the application in detached mode.** The `-d` flag tells it to run in the background, so it will keep running even after you close your SSH session.

    ```bash
    docker compose up -d
    ```

2.  Docker Compose will now automatically:

      * **Build** the Docker image from the `Dockerfile` (if it hasn't been built before).
      * **Create** a container with the settings from your `docker-compose.yaml` file.
      * **Start** the application.

-----

## Step 4: Access the Web Interface

The application is now running and accessible on your network.

1.  **Find your server's IP address** by running this command in the server's terminal:

    ```bash
    hostname -I
    ```

2.  **Open a web browser** on your computer and navigate to the server's IP address on port `5000`:

    ```
    http://<your_server_ip_address>:5000
    ```

-----

## Managing the Application ⚙️

Here are some common commands for managing your running application:

  * **View Logs:** To see the live output from the application (useful for debugging), use:

    ```bash
    docker-compose logs -f
    ```

    (Press `Ctrl+C` to stop viewing the logs).

  * **Stop the Application:** To stop and remove the running container, use:

    ```bash
    docker-compose down
    ```

  * **Restart the Application:**

    ```bash
    docker-compose restart
    ```

  * **Update the Application:** After pulling new changes with `git pull`, you can rebuild and restart the app with:

    ```bash
    docker-compose up -d --build
    ```