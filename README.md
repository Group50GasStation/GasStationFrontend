# GasStationFrontend

Web app built for software design, allows creation of quotes for fuel purchases.

# Starting the app


First, install necessary libraries from pip. Make sure you do this inside of a virtual env that you create inside of the cloned repository.

Activate the env, then install packages:

```
pip install flask flask-login flask-sqlalchemy flask-wtf coverage email_validator
```

Then you can run

```
flask --debug --app app run
```

To start the application. From there, navigate to http://127.0.0.1:5000/ to see the rendered webpage.

Changes made to html or css files will be hot reloaded upon a refresh in the browser.


_________________________________________________________________________________________________________________________________________________________

# Python Unit Testing with unittest Framework

### Running the Tests

To run the unit tests, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory containing the project files.
3. Run the following command:

    ```bash
    python -m unittest discover
    ```

    This command automatically discovers and runs all test cases in the project.

### Interpreting the Results

After running the tests, you'll see output indicating whether each test case passed or failed. Here's what to look for:

- **OK**: Indicates that all tests passed successfully.
- **FAIL**: Indicates that one or more tests failed. The output will provide details about which tests failed and why.
- **ERROR**: Indicates that an unexpected error occurred during the test execution. The output will provide information about the error.

Additionally, you can generate a code coverage report to see how much of the codebase is covered by the tests. Follow the instructions in the [Code Coverage](#code-coverage) section to generate and interpret the report.

# Contributing

If you'd like to contribute to this project by adding more tests or improving existing ones, feel free to fork the repository, make your changes, and submit a pull request.

# Code Coverage

Code coverage measures the percentage of your codebase that is covered by unit tests. To generate a code coverage report, follow these steps:

1. Ensure you have the `coverage` tool installed. If not, install it using `pip`

2. Run the tests with coverage:

    ```bash
    coverage run -m unittest discover
    ```

3. Generate the coverage report:

    ```bash
    coverage report
    ```

    This command will display the code coverage percentage and detailed information about which lines of code are covered and which are not.


To run only the tests in the test_main.py file using coverage, you can specify the test file directly in the coverage command. Here's how you can do it:

```bash
coverage run -m unittest backend.test_main
```

This command will run the tests in the test_main.py file under the backend package and collect coverage data. After running this command, you can generate a coverage report specific to this test file:

```bash
coverage report backend/test_main.py
```
