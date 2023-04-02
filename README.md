# Pytropolis

Pytropolis is a Python application that runs Python scripts via an API in a virtual environment. It provides a simple and efficient way to execute Python scripts in a controlled environment without having to manage dependencies manually.

## Getting Started

To get started with Pytropolis, follow these steps:

1. Install Python on your system.
2. Clone the Pytropolis repository to your local machine.
3. Create a virtual environment and activate it.
4. Install the required dependencies using `pip`.
5. Run the application using `python app.py`.

## Usage

Pytropolis provides a REST API that allows you to run Python scripts in a virtual environment. You can send a request to the API with the path to your script and any arguments you want to pass in.

For example, to execute a Python script called `my_script.py` with two arguments, you can send a `POST` request to `http://localhost:5000/run` with the following payload:

```json
{
    "script_path": "my_script.py",
    "args": ["arg1", "arg2"]
}
