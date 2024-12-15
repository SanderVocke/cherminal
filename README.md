# Termchat

Termchat is a web-based interface for interacting with a shell process. It allows users to run a command as a subprocess and communicate with it through a web page. This can be useful for monitoring and interacting with long-running processes or for providing a simple web interface to command-line tools.

## Features

- Run a shell command as a subprocess and interact with it via a web interface.
- Basic authentication support using an htpasswd file.
- Debug mode to log inputs sent to the subprocess.

## Requirements

- Python 3.12 or later
- Flask
- Flask-HTTPAuth
- Passlib

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd termchat
   ```

2. Install the package using pip:
   ```bash
   pip install .
   ```

## Usage

Run the application with the following command:

```bash
python termchat.py -c "<command>" [-d] [--password <htpasswd-file>]
```

- `-c`, `--command`: The command to run as a subprocess.
- `-d`, `--debug`: Enable debug mode to log inputs.
- `--password`: Path to an htpasswd file for basic authentication.

Example:

```bash
python termchat.py -c "tail -f /var/log/syslog" --password /path/to/htpasswd
```

## Accessing the Web Interface

Open a web browser and navigate to `http://localhost:5000` to access the Termchat interface.

## License

This project is licensed under the MIT License.
