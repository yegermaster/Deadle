"""
This module serves as the entry point for the Deadle game application.

It imports the Flask app instance from the app package and runs the application
in debug mode if the script is executed directly.

Usage:
    python run.py

This will start the Flask development server for the Deadle game application.
"""
from application.appGenerator import get_app

def main():
    app = get_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()