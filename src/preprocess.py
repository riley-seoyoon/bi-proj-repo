import os

import yaml

yml_dir = os.path.abspath("bulk-rnaseq-preproc/workflow/params.yaml")


def modify_yaml_files(tools, params):
    # Modify tools.yaml
    with open(f"{yml_dir}/tools.yaml") as f:
        tools_config = yaml.safe_load(f)

    # Modify tool configuration based on user input
    for tool in tools:
        if tool in tools_config:
            tools_config[tool]["use_tool"] = True

    # Write modified tools.yaml
    with open(f"{yml_dir}/tools.yaml", "w") as f:
        yaml.dump(tools_config, f)

    # Modify params.yaml
    with open(f"{yml_dir}/params.yaml") as f:
        params_config = yaml.safe_load(f)

    # Modify parameters based on user input
    for key, value in params.items():
        if key in params_config:
            params_config[key] = value

    # Write modified params.yaml
    with open(f"{yml_dir}/params.yaml", "w") as f:
        yaml.dump(params_config, f)


def rename_input_files(input_dir, is_paired_end):
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith(".fastq.gz"):
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(
                    root, get_new_file_name(file_name, is_paired_end)
                )
                os.rename(old_path, new_path)


def get_new_file_name(file_name, is_paired_end):
    parts = file_name.split("_")
    sample = parts[0]
    suffix = parts[-1].split(".")[0]

    if is_paired_end:
        read = parts[1]
        return f"{sample}_{read}.{suffix}.fastq.gz"
    else:
        return f"{sample}.{suffix}.fastq.gz"


def preprocess():
    # Load tools.yaml to get available tools
    with open("tools.yaml") as f:
        tools_config = yaml.safe_load(f)

    # Print available tools
    print("Available tools:")
    for tool, config in tools_config.items():
        print(f"- {tool}: {config['description']}")

    # Prompt user for input
    tools_input = input("Enter the tools to use (comma-separated): ")
    is_paired_end = input("Is the data paired-end? (yes/no): ").lower() == "yes"

    # Parse user input
    tools = [tool.strip() for tool in tools_input.split(",")]

    # Modify the YAML files
    modify_yaml_files(tools, {})

    # Rename input files
    input_dir = "."  # Set the input directory
    rename_input_files(input_dir, is_paired_end)


if __name__ == "__main__":
    preprocess()
