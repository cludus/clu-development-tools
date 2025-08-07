import os
from jinja2 import Environment, FileSystemLoader
import shutil
import pathlib
import yaml
import random
import string
import subprocess

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def copy_files(source_directory, destination_directory):
    script_directory = pathlib.Path(__file__).parent.resolve()
    source_directory = os.path.join(script_directory, source_directory)
    try:
        if os.path.exists(destination_directory) and os.path.exists(destination_directory + '/.bin'):
            try:
                shutil.rmtree(destination_directory + '/.bin')
                print(f"Directory '{destination_directory}/.bin' removed successfully.")
            except shutil.Error as e:
                print(f"Error deleting directory: {e}")
            except OSError as e:
                print(f"Error removing directory '{destination_directory}': {e}")
        shutil.copytree(source_directory, destination_directory, dirs_exist_ok=True)
        print(f"Directory '{source_directory}' and its contents copied to '{destination_directory}' successfully.")
    except shutil.Error as e:
        print(f"Error copying directory: {e}")
    except OSError as e:
        print(f"OS Error: {e}")

def remove_cluster_dir():
    directory_name = ".cluster"
    if os.path.exists(directory_name) and not os.path.exists(directory_name + '/.vagrant'):
        try:
            shutil.rmtree(directory_name)
            print(f"Directory '{directory_name}' removed successfully.")
        except shutil.Error as e:
            print(f"Error deleting directory: {e}")
        except OSError as e:
            print(f"Error removing directory '{directory_name}': {e}")

def create_cluster_dir():
    directory_name = ".cluster"
    try:
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
            print(f"directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"directory '{directory_name}' already exists.")

def render_template(tpl, data, output):
    script_directory = pathlib.Path(__file__).parent.resolve()
    template_dir = 'templates'
    template_dir = os.path.join(script_directory, template_dir)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(tpl)
    rendered_output = template.render(data)
    with open(output, 'w') as f:
        f.write(rendered_output)

def create_vagrant_file(data):
    render_template('Vagrantfile.j2', data, '.cluster/Vagrantfile')

def create_ansible_inventory(data):
    render_template('inventory.yml.j2', data, '.cluster/inventory.yml')

def create_hosts(data):
    render_template('hosts.txt.j2', data, '.cluster/hosts.txt')

def create_gen_root(data):
    render_template('gen-root-ca.j2', data, '.cluster/.bin/gen-root-ca')

def create_ssh_copy_ids(data):
    render_template('ssh-copy-ids.j2', data, '.cluster/.bin/ssh-copy-ids')

def give_exec_access():
    give_exec_access_to_file(".cluster/.bin/ssh-copy-ids")
    give_exec_access_to_file(".cluster/.bin/gen-root-ca")

def give_exec_access_to_file(path):
    result = subprocess.run(["chmod", "+x", path], capture_output=True, text=True, check=True)
    # print("Stdout:", result.stdout)
    # print("Stderr:", result.stderr)

def create_setup(data):
    print(f'creating setup for  {data['name']}')  # Press Ctrl+8 to toggle the breakpoint.
    remove_cluster_dir()
    copy_files('files', '.cluster')
    create_vagrant_file(data)
    create_ansible_inventory(data)
    create_hosts(data)
    create_gen_root(data)
    create_ssh_copy_ids(data)
    give_exec_access()

def read_config(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print("Error: config.yaml not found.")
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")

def create_cluster():
    if not os.path.exists('cluster.yml'):
        print(f"Error cluster.yml not found in current dir")
        return

    data = read_config('cluster.yml')
    data['cluster_token'] = generate_random_string(64)
    master_index=-1
    for index, node in enumerate(data['nodes']):
        if node['type'] == 'master':
            master_index = index
    for index, node in enumerate(data['nodes']):
        node['master_index'] = master_index
    create_setup(data)
