# **AWS ECS Exec**

AWS ECS Exec is an interactive Python tool that simplifies executing commands in **ECS/Fargate containers** using **AWS credentials**. It interactively helps you **discover ECS clusters, services, tasks, and containers**, then executes a command (`/bin/sh` by default) using **AWS ECS Exec**. 

This tool **requires AWS Session Manager Plugin** and ensures a seamless experience for developers and DevOps teams.

---

## **🚀 Features**
- **Interactive AWS Profile Selection**  
  - Prompts for AWS profile if not specified.
- **Automated Discovery of ECS Resources**  
  - No need to manually look up clusters, services, tasks, or containers.
- **Auto-Selection for Single Container Tasks**  
  - If only one container exists, the tool auto-selects it.
- **Command Logging for Easy Reuse**  
  - Displays the full `aws ecs execute-command` line for future reference.
- **Session Manager Plugin (SSM) Required**  
  - Enforces secure execution via AWS SSM.
- **Verbose Logging (`--verbose`) for Debugging**  
  - Enables additional log details.
- **Clear Error Handling**  
  - Provides descriptive error messages when ECS Exec isn’t enabled.
- **Unit Tested**  
  - Includes tests using Python’s `unittest` framework.

---

## **📌 Prerequisites**
Before using this tool, ensure the following are installed and configured:

### **Required**
1. **Python 3.6+ (Python 3.11 Recommended)**
   ```sh
   python3 --version
   ```
2. **AWS CLI (v2+)**
   ```sh
   aws --version
   ```
   If not installed, follow the [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

3. **AWS Session Manager Plugin (Required)**
   ```sh
   session-manager-plugin --version
   ```
   If missing, install via:
   - macOS (Homebrew):
     ```sh
     brew install session-manager-plugin
     ```
   - Linux:
     ```sh
     sudo apt install session-manager-plugin
     ```
   - Windows: Download from [AWS Docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html).

4. **AWS Credentials Configured**
   - Run `aws configure` or use AWS SSO:
     ```sh
     aws sso login --profile default
     ```
   - Ensure IAM role includes:
     ```json
     {
       "Effect": "Allow",
       "Action": [
         "ecs:ExecuteCommand",
         "ssmmessages:CreateControlChannel",
         "ssmmessages:CreateDataChannel",
         "ssmmessages:OpenControlChannel",
         "ssmmessages:OpenDataChannel"
       ],
       "Resource": "*"
     }
     ```

---

## **🔧 Installation**
Clone the repository and set up a virtual environment:

```sh
git clone git@github.com:diegugawa/aws-ecs-exec.git
cd aws-ecs-exec
python3 -m venv .venv
source .venv/bin/activate
pip install boto3 botocore
```

---

## **🚀 Usage**
Run the script to execute a command inside an ECS container:

```sh
python ecsexec.py --profile default --region us-west-2
```

This will:
1. **Auto-detect the ECS cluster, service, task, and container.**
2. **Prompt for selection (if multiple options exist).**
3. **Run an interactive shell (`/bin/sh`) inside the container.**

### **📌 Supported Options**
| Option | Description |
|--------|-------------|
| `--region <region>` | AWS region (e.g., `us-west-2`). Uses AWS CLI config if not provided. |
| `--profile <profile>` | AWS profile name. Prompts interactively if not provided. |
| `--command <command>` | Command to execute inside the container (default: `/bin/sh`). |
| `--ssm` | Uses AWS **Session Manager Plugin** (required). |
| `--verbose` | Enables **detailed logs for debugging**. |

### **Example Commands**
#### **1️⃣ Execute `/bin/sh` in a Container**
```sh
python ecsexec.py --profile default --region us-west-2
```
- Selects ECS Cluster, Service, Task, and Container.
- Runs an interactive shell (`/bin/sh`).

#### **2️⃣ Execute a Custom Command**
```sh
python ecsexec.py --command "ls -la"
```
- Runs `ls -la` inside the container.

#### **3️⃣ Enable Verbose Logging for Debugging**
```sh
python ecsexec.py --verbose
```
- Displays **detailed logs**.

---

## **⚙️ Configuration File (Optional)**
You can create a configuration file at `~/.ecsexec/config.json` to store default settings.

### **Example Config File (`~/.ecsexec/config.json`)**
```json
{
  "profile": "default",
  "region": "us-west-2",
  "command": "/bin/sh"
}
```
If this file exists, `ecsexec.py` will use the stored values unless overridden by command-line arguments.

---

## **🔍 Troubleshooting**
If you encounter problems, try these solutions:

### **🔴 AWS Permissions Issue**
Error:
```
An error occurred (AccessDeniedException) when calling the ExecuteCommand operation
```
✅ **Solution**: Ensure your IAM role has the correct permissions (see prerequisites above).

---

### **🔴 Session Manager Plugin Not Found**
Error:
```
SessionManagerPlugin is not found.
```
✅ **Solution**:
- Install the **Session Manager Plugin**:
  ```sh
  brew install session-manager-plugin
  ```
  **or**
  ```sh
  sudo apt install session-manager-plugin
  ```

---

### **🔴 "TargetNotConnectedException"**
Error:
```
An error occurred (TargetNotConnectedException) when calling the ExecuteCommand operation: The execute command failed due to an internal error.
```
✅ **Solution**:
1. **Check if `enableExecuteCommand` is set to `true`:**
   ```sh
   aws ecs describe-tasks --cluster my-cluster --tasks my-task --query "tasks[].enableExecuteCommand"
   ```
   - If it returns `false`, **enable ECS Exec**:
     ```sh
     aws ecs update-service --cluster my-cluster --service my-service --enable-execute-command
     ```

2. **Ensure IAM permissions allow `ssm:StartSession`.** (See permissions above.)

---

### **🔴 ECS Cluster Not Found**
Error:
```
No ECS clusters found.
```
✅ **Solution**:
- Ensure you are using the **correct AWS region**:
  ```sh
  aws ecs list-clusters --region us-west-2
  ```

---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **📌 Contributors**
- **Diego Saavedra-Kloss**
- **Community contributions are welcome!**  

If you find issues or want to improve the project, **submit a pull request**!

---

## **🚀 Next Steps**
- Try executing different commands inside ECS containers.
- Use `--verbose` to debug command execution.
- **If an error occurs, check IAM permissions and ensure `ecs:ExecuteCommand` is enabled.**
