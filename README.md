# Personal Password Strength Checker

A command-line interface (CLI) application built in Python to help users evaluate the strength of their passwords. This tool provides detailed feedback, a strength score, and suggestions for improvement.

## Features

- **Modern GUI**: A user-friendly graphical interface built with Tkinter.
- **Real-Time Breach Check**: Integrates with the 'Have I Been Pwned' API to check if a password has been exposed in a data breach.
- **Password Strength Analysis**: Checks for length, character variety, and common weak patterns.
- **Detailed Feedback**: Provides actionable suggestions to improve password security.
- **Strength Score**: Rates passwords on a scale of 1 to 10, penalizing compromised passwords.
- **Color-Coded Output**: Displays strength levels in different colors for quick assessment.
- **Secure Input**: Hides password typing in the CLI for privacy.
- **Interactive CLI and GUI**: Choose between a command-line or graphical experience.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/password-strength-checker.git
    cd password-strength-checker
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

This project provides both a command-line (CLI) and a graphical user interface (GUI) application.

### GUI Application

To run the GUI application, execute the following command:

```bash
python3 main_gui.py
```

This will open a window where you can type your password and see the analysis in real-time.

### CLI Application

To run the original CLI application from your terminal:

```bash
python3 password_checker.py
```

You will be prompted to enter a password. The application will then display a detailed analysis.

To exit the application, type `exit` or `quit`, or press `Ctrl+C`.

### Example

```
$ python3 password_checker.py
Personal Password Strength Checker
Type 'exit' or 'quit' to close.
---------------------------------
Enter your password:
--- Password Analysis ---
Strength Score: 8/10

--- Feedback & Suggestions ---
- Password length is adequate.
- Password has a good mix of character types.
---------------------------
```

## Examples of Strong vs. Weak Passwords

### Weak Passwords
- `password`
- `123456`
- `qwerty`
- `iloveyou`

**Why they are weak:** They are short, predictable, and appear in dictionary attacks.

### Strong Passwords
- `Tr0ub4dor&3`
- `!P@ssw0rdStr0ng!`
- `MyP@ssw0rdIsVeryL0ngAndS3cur3!`

**Why they are strong:** They are long, contain a mix of uppercase and lowercase letters, numbers, and special characters, and are not easily guessable.

## Security Considerations

- **Do Not Store Passwords**: This tool analyzes passwords in memory and does not store them.
- **Local Execution**: The checker runs entirely on your local machine, so your passwords are never transmitted over the internet.
- **Clipboard Use**: Be cautious when copying and pasting passwords. It is recommended to type them directly into the CLI.

## Testing

The project includes a suite of unit tests to ensure the reliability of the password analysis logic. To run the tests, execute the following command from the root directory:

```bash
python3 -m unittest test_password_checker.py
```

The tests cover:
- Password length checks
- Character variety validation
- Detection of common weak patterns
- Strength score calculation
- Feedback generation

## Contributing

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a pull request.
