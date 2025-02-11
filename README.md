# **AWS ECS Exec Utility**

## **Overview**
`ecsexec.py` is a Python-based interactive tool that simplifies executing commands inside **AWS ECS/Fargate containers** using **ECS Exec** and **AWS Session Manager**.

### **Key Features**
- **Interactive AWS Profile & Region Selection**  
  - If not provided, the tool prompts for selection.
- **Automated ECS Cluster, Service, Task & Container Discovery**  
  - Reduces the need to manually look up resources.
- **Auto-Selection for Single Container Tasks**  
  - If a task has only one container, it is auto-selected.
- **Logs the Final Executed Command**  
  - Makes it easy to copy for reuse.
- **Requires AWS Session Manager Plugin**  
  - Enforces secure ECS Exec execution.
- **Verbose Mode for Debugging (`--verbose`)**  
  - Logs additional details.
- **Unit Tested with Python's `unittest` Framework**  
  - Ensures stability and reliability.

---

## **📌 Prerequisites**
Before using this tool, ensure the following are installed:

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

3. **AWS Session Manager Plugin** (Required)
   ```sh
   session-manager-plugin --version
   ```
   If missing, install it via:
   - macOS (Homebrew):  
     ```sh
     brew install session-manager-plugin
     ```
   - Linux:  
     ```sh
     sudo apt install session-manager-plugin
     ```
   - Windows: Download from [AWS Docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html).

4. **AWS Credentials** (Must Have `ecs:ExecuteCommand` Permissions)
   ```sh
   aws configure
   ```
   - Ensure your profile has `ecs:ExecuteCommand` permissions.
   - For AWS SSO users:
     ```sh
     aws sso login --profile default
     ```

5. **Required Python Packages**
   ```sh
   pip install boto3 botocore
   ```

---

## **🚀 Installation**
Clone the repository and set up a virtual environment:

```sh
git clone git@github.com:diegugawa/aws-ecs-exec.git
cd aws-ecs-exec
python3 -m venv .venv
source .venv/bin/activate
pip install boto3 botocore
```

---

## **🔧 Usage**
Run the script to execute a command inside an ECS container:

```sh
python ecsexec.py --profile default --region us-west-2
```

This will:
1. **Auto-detect the ECS cluster, service, task, and container.**
2. **Prompt for selection (if multiple options exist).**
3. **Run an interactive shell (`/bin/sh`) inside the container.**

### **Common Usage Examples**
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
✅ **Solution**: Ensure your IAM role has the following permissions:
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
✅ If using SSM, add:
```json
{
  "Effect": "Allow",
  "Action": "ssm:StartSession",
  "Resource": "*"
}
```
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
