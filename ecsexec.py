#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import subprocess
from shutil import which

import boto3
import botocore.exceptions

logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.expanduser("~/.ecsexec/config.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            logger.info("Loaded config from %s", config_path)
        except Exception as e:
            logger.warning("Failed to load config file: %s", e)
    return config

def interactive_selection(options, prompt):
    if not options:
        return None
    if len(options) == 1:
        logger.info("Only one option available. Auto-selecting: %s", options[0])
        return options[0]
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}) {option}")
    while True:
        choice = input("Enter choice number: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("Invalid selection. Please try again.")

def get_aws_profiles():
    try:
        result = subprocess.run(
            ["aws", "configure", "list-profiles"],
            capture_output=True,
            text=True,
            check=True
        )
        profiles = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
        return profiles
    except subprocess.CalledProcessError as e:
        logger.error("Failed to get AWS profiles: %s", e)
        return []

def get_boto3_session(profile, region):
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        return session
    except botocore.exceptions.BotoCoreError as e:
        logger.error("Failed to create boto3 session: %s", e)
        sys.exit(1)

def list_ecs_clusters(ecs_client):
    try:
        response = ecs_client.list_clusters()
        arns = response.get("clusterArns", [])
        cluster_names = [arn.split("/")[-1] for arn in arns]
        return cluster_names
    except botocore.exceptions.ClientError as e:
        logger.error("Error listing ECS clusters: %s", e)
        sys.exit(1)

def list_ecs_services(ecs_client, cluster):
    try:
        response = ecs_client.list_services(cluster=cluster)
        services = response.get("serviceArns", [])
        if not services:
            logger.error("No services found in cluster %s", cluster)
            sys.exit(1)
        return services
    except botocore.exceptions.ClientError as e:
        logger.error("Error listing ECS services for cluster %s: %s", cluster, e)
        sys.exit(1)

def list_ecs_tasks(ecs_client, cluster, service):
    try:
        response = ecs_client.list_tasks(cluster=cluster, serviceName=service, desiredStatus="RUNNING")
        tasks = response.get("taskArns", [])
        if not tasks:
            logger.error("No running tasks found for service %s in cluster %s", service, cluster)
            sys.exit(1)
        return tasks
    except botocore.exceptions.ClientError as e:
        logger.error("Error listing ECS tasks for service %s in cluster %s: %s", service, cluster, e)
        sys.exit(1)

def get_task_containers(ecs_client, cluster, task):
    try:
        response = ecs_client.describe_tasks(cluster=cluster, tasks=[task])
        tasks = response.get("tasks", [])
        if not tasks:
            logger.error("No details found for task %s", task)
            sys.exit(1)
        containers = tasks[0].get("containers", [])
        container_names = [c.get("name") for c in containers if c.get("name")]
        if not container_names:
            logger.error("No containers found for task %s", task)
            sys.exit(1)
        return container_names
    except botocore.exceptions.ClientError as e:
        logger.error("Error describing task %s in cluster %s: %s", task, cluster, e)
        sys.exit(1)

def check_session_manager_plugin():
    if which("session-manager-plugin") is None:
        logger.error("session-manager-plugin is required when using --ssm, but it was not found.")
        sys.exit(1)
    else:
        logger.info("session-manager-plugin is installed.")

def build_execute_command(profile, region, cluster, container, task, command, use_ssm):
    cmd = [
        "aws", "ecs", "execute-command",
        "--cluster", cluster,
        "--container", container,
        "--task", task,
        "--interactive",
        "--command", command
    ]
    if profile:
        cmd.extend(["--profile", profile])
    if region:
        cmd.extend(["--region", region])
    # The --ssm flag doesn't change the command, but forces a check.
    return cmd

def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="ECS Exec Interactive Script")
    parser.add_argument("--region", help="AWS region", default=config.get("region"))
    parser.add_argument("--profile", help="AWS profile", default=config.get("profile"))
    parser.add_argument("--command", help="Command to execute in container", default=config.get("command", "/bin/sh"))
    parser.add_argument("--ssm", action="store_true", help="Force use of session-manager-plugin")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    profile = args.profile
    region = args.region

    if not profile:
        profiles = get_aws_profiles()
        if not profiles:
            logger.error("No AWS profiles found. Please configure AWS CLI.")
            sys.exit(1)
        profile = interactive_selection(profiles, "Choose an AWS profile:")
        logger.info("Selected profile: %s", profile)

    if not region:
        session_tmp = boto3.Session(profile_name=profile)
        region = session_tmp.region_name
        if not region:
            region = input("Enter AWS region: ")
    logger.info("Using region: %s", region)

    if args.ssm:
        check_session_manager_plugin()
    else:
        logger.info("Using AWS credentials from aws configure (not enforcing session-manager-plugin).")

    boto3_session = get_boto3_session(profile, region)
    ecs_client = boto3_session.client("ecs")

    clusters = list_ecs_clusters(ecs_client)
    if not clusters:
        logger.error("No ECS clusters found. Ensure your ECS environment is set up and you are logged in.")
        sys.exit(1)
    cluster = interactive_selection(clusters, "Select an ECS cluster:")
    logger.info("Selected cluster: %s", cluster)

    services = list_ecs_services(ecs_client, cluster)
    service = interactive_selection(services, "Select an ECS service:")
    logger.info("Selected service: %s", service)

    tasks = list_ecs_tasks(ecs_client, cluster, service)
    task = interactive_selection(tasks, "Select an ECS task:")
    logger.info("Selected task: %s", task)

    containers = get_task_containers(ecs_client, cluster, task)
    container = interactive_selection(containers, "Select a container:")
    logger.info("Selected container: %s", container)

    execute_cmd = build_execute_command(profile, region, cluster, container, task, args.command, args.ssm)
    logger.info("Executing command: %s", " ".join(execute_cmd))
    try:
        subprocess.run(execute_cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("ECS Exec command failed: %s", e)
        logger.error("Please ensure that ECS Exec is enabled for the task/container and try again.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
