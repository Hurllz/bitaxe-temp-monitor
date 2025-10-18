from gui import BitaxeAutotuningApp
from headless import app
import sys


if __name__ == "__main__":
    # Check if the first argument is "headless" to launch the server
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'headless':
        # Run the Flask web server when specified
        print("Starting Flask web server in headless mode...")
        app.run(host='0.0.0.0', port=5000)
    else:
        # Run the desktop autotuning app by default
        try:
            app = BitaxeAutotuningApp()
            app.run()
        except KeyboardInterrupt:
            print("\nProgram interrupted and exiting cleanly...")