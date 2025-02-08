# AWS ECS Exec

AWS ECS Exec is an interactive tool written in Python that simplifies executing commands in ECS/Fargate containers using AWS credentials. It interactively helps you discover your ECS clusters, services, tasks, and containers, then executes a command (default is `/bin/sh`) using AWS ECS Exec. It also logs the final command for easy reuse. This tool works seamlessly with AWS Session Manager, making it a popular choice in the community.

## Features

- **Interactive AWS Profile Selection:** Choose an AWS profile if not specified.
- **Automated Discovery:** Automatically lists ECS clusters, services, tasks, and containers.
- **Auto-Selection:** If a task has only one container, the tool auto-selects it and logs a message.
- **Command Logging:** Displays the full `aws ecs execute-command` line for easy copy-and-paste reuse.
- **Session Manager Plugin Option:** Use the `--ssm` flag to enforce the use of the session-manager-plugin. If the flag is provided but the plugin isn’t installed, an error is raised.
- **Verbose Logging:** Enable verbose mode (`--verbose`) for additional debug information.
- **Configuration File Support:** Optionally store default settings in `~/.ecsexec/config.json`.
- **Clear Error Handling:** Provides descriptive error messages (e.g., when ECS Exec isn’t enabled on a task/container).
- **Unit Tested:** Comes with unit tests using Python’s built-in `unittest` framework.

## Prerequisites

Before using this tool, ensure the following are installed and configured:

- **Python:** Requires Python 3.6 or later. This tool is fully compatible with Python 3.11.
- **AWS CLI:** Must be installed and configured (using `aws configure` or AWS SSO) as this tool relies on AWS CLI commands to list profiles and execute ECS commands.
- **AWS Credentials:** Ensure you have valid AWS credentials set up.
- **Python Packages:** Install `boto3` and `botocore` via pip.
- **session-manager-plugin (Optional):** Required if you plan to use the `--ssm` flag to force AWS Session Manager usage. This plugin enhances the ECS Exec experience and is highly valued in the community.

## Quick Start Using pyenv

If you don’t have the desired Python version installed, you can quickly set it up using [pyenv](https://github.com/pyenv/pyenv):

1. **Install pyenv** (if not already installed). For example, on macOS with Homebrew:

   ```bash
   brew update
   brew install pyenv
   ```

2. **Install Python 3.11 (or your desired version):**

   ```bash
   pyenv install 3.11.0
   ```

3. **Set Python 3.11 as the local version:**

   ```bash
   pyenv local 3.11
   ```

4. **Create a virtual environment using Python’s built-in venv module:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Clone the repository and install dependencies:**

   ```bash
   git clone git@github.com:diegugawa/aws-ecs-exec.git
   cd AWS-ECS-exec
   pip install boto3 botocore
   ```

6. **(Optional) To use the Session Manager Plugin, ensure it is installed.**  
   You can download and install it from the [AWS documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html).

7. **Run the tool:**

   ```bash
   python ecsexec.py [OPTIONS]
   ```

## Configuration

You can optionally create a configuration file at `~/.ecsexec/config.json` to store default settings. Example:

```json
{
  "profile": "default",
  "region": "us-west-2",
  "command": "/bin/sh"
}
```

## Usage

Run the script with the desired options:

```bash
python ecsexec.py [OPTIONS]
```

### Supported Options

- `--region <region>`  
  Specify the AWS region. If not provided, the tool will use the region from your AWS configuration or prompt you for it.

- `--profile <profile>`  
  Specify the AWS profile. If not provided, you’ll be prompted to select one interactively.

- `--command <command>`  
  The command to execute in the container. Defaults to `/bin/sh`.

- `--ssm`  
  Force the use of the session-manager-plugin. If the plugin isn’t installed, an error is raised.

- `--verbose`  
  Enable verbose logging for debugging purposes.

### Example Commands

- **Standard Execution:**

  ```bash
  python ecsexec.py --region us-west-2 --profile default
  ```

- **Using Session Manager Plugin:**

  ```bash
  python ecsexec.py --ssm --profile my-profile --region us-east-1 --command '/bin/bash'
  ```

- **Verbose Mode:**

  ```bash
  python ecsexec.py --verbose
  ```

After making your selections, the tool will display the final command it executed. You can copy this command for future use without going through the interactive process again.

## Running Tests

To run the unit tests, execute:

```bash
python -m unittest test_ecsexec.py
```

## Notes

- If ECS Exec is not enabled for the selected task/container, a clear error message with remediation steps will be displayed.
- The tool is designed for macOS and Linux environments.
- This tool is fully compatible with Python 3.11.
- **AWS CLI** must be installed and configured before using this tool.
- **session-manager-plugin** is optional and should be installed if you intend to use the `--ssm` flag to leverage AWS Session Manager functionality.

## Repository

Clone the repository using:

```bash
git clone git@github.com:diegugawa/aws-ecs-exec.git
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.
