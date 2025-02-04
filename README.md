# TCP Connection Tester 🚀

A simple, yet powerful tool to test TCP connectivity to a specified host and port. This script allows you to check if a host is reachable and responsive over TCP, with customizable parameters for attempts, timeouts, and more.

---

## Features ✨

- **Customizable Attempts**: Specify how many times to test the connection.
- **Timeout Control**: Set a timeout period for each connection attempt.
- **Real-time Spinner**: Displays a dynamic spinner while testing connectivity.
- **Clear Stats**: Get detailed test results with success rates, response times, and more.
- **Error Handling**: Shows relevant messages in case of errors like timeouts or connection refusals.
  
---

## Requirements 📋

- Python 3.6+
- `requests` library (install with `pip install requests`)
- `colorama` library (install with `pip install colorama`)

## Usage 🖥️
Follow the on-screen prompts:
- 1. Enter the host IP or domain to test.#
- 2. Specify the port number to test (default is 80 for HTTP, 443 for HTTPS)
- 3. Choose the number of attempts to make (default is 5).
- 4. Set the timeout period for each attempt (default is 5 seconds).
- 5. Press Enter to start the test.

---

## License📄

This project is licensed under the MIT License - see the LICENSE file for details.
