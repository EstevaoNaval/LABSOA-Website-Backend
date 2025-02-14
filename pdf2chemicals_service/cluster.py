import os
import subprocess
from datetime import datetime
import redis
from typing import List
from random import choice
import uuid

from django.conf import settings

from .util.util import generate_random_alphanumeric_sequence

class ResourceUnavailable(Exception):
    pass

class ClusterNodeManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            db=os.getenv('REDIS_DB'),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True
        )

    def get_available_nodes(self) -> List[str]:
        """Obtém todos os nós do cluster com GPU disponível via PBS/TORQUE"""
        try:
            cmd = "pbsnodes | awk '/^[a-zA-Z]/{node=$1} /state = free/{free=1} /NOGPU/{free=0} /^$/{if(free==1) print node; free=0}'"
            
            # Executa comando pbsnodes para listar nós
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            
            # Parse a saída do comando para extrair nós com GPU
            nodes = self._parse_pbsnodes_output(result.stdout)
            
            return nodes
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar pbsnodes: {e}")
            return []

    def _parse_pbsnodes_output(self, output: str) -> List[str]:
        """Parse da saída do pbsnodes para encontrar nós com GPU livre"""
        nodes = []
        
        for node in output.splitlines():
            if node.strip() != '':
                nodes.append(node.strip())
        
        return nodes

    def mark_node_as_busy(self, node_name: str):
        """Marca um nó como ocupado por um job específico"""
        key = f"cluster:node:{node_name}"
        
        reservation_id = uuid.uuid4().hex
        
        self.redis_client.hset(key, mapping={
            'reservation_id': reservation_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return reservation_id

    def mark_node_as_free(self, node_name: str):
        """Marca um nó como livre"""
        key = f"cluster:node:{node_name}"
        self.redis_client.delete(key)

    def get_reservation_id_from_node_name(self, node_name: str) -> str:
        return self.redis_client.hget(f"cluster:node:{node_name}", "reservation_id")

    def get_free_gpu_node(self) -> str:
        """Obtém um nó livre com GPU, considerando os nós já em uso por outros workers"""
        available_nodes = self.get_available_nodes()
        
        # Filtra nós que já estão em uso por outros workers
        free_nodes = [
            node for node in available_nodes
            if not self.redis_client.exists(f"cluster:node:{node}")
        ]
        
        return choice(free_nodes) if free_nodes else ""

    def is_node_reservation_valid(self, node_name: str, reservation_id: str):
        return True if self.redis_client.hget(f"cluster:node:{node_name}", "reservation_id") == reservation_id else False

    def reserve_free_gpu_node(self) -> str:
        free_gpu_node = self.get_free_gpu_node()
        
        if free_gpu_node != "":
            self.mark_node_as_busy(node_name=free_gpu_node)
            
        return free_gpu_node
    
    def cleanup_stale_nodes(self, max_age_hours: int = 2):
        """Limpa registros antigos de nós ocupados"""
        threshold = datetime.now().timestamp() - (max_age_hours * 3600)
        
        # Lista todas as chaves de nós
        for key in self.redis_client.scan_iter("cluster:node:*"):
            node_data = self.redis_client.hgetall(key)
            if node_data:
                timestamp = datetime.fromisoformat(node_data['timestamp']).timestamp()
                if timestamp < threshold:
                    self.redis_client.delete(key)

# Function to load the PBS template and replace variables
def load_and_replace_template(job_id, node_name, template_path, java_home, conda_env, pdf2chemicals_path, pdf_path, output_dir, json_prefix):
    """
    Loads the PBS template and replaces the variables with the correct values.
    
    Parameters:
    - job_id: PBS job id.
    - template_path: Path to the template file.
    - java_home: JAVA_HOME path.
    - conda_env: Conda environment name.
    - pdf2chemicals_path: Path to the pdf2chemicals script.
    - pdf_path: Path to the PDF to be processed.
    - output_dir: Directory where the output will be saved.
    - json_prefix: Prefix for the output JSON file.
    
    Returns:
    - The script content with the replaced variables.
    """
    # Load the template content
    with open(template_path, 'r') as file:
        script_content = file.read()

    # Replace the variables in the template
    script_content = script_content.replace("{{job_id}}", job_id)
    script_content = script_content.replace("{{node_name}}", node_name)
    script_content = script_content.replace("{{JAVA_HOME}}", java_home)
    script_content = script_content.replace("{{conda_env}}", conda_env)
    script_content = script_content.replace("{{pdf2chemicals_path}}", pdf2chemicals_path)
    script_content = script_content.replace("{{pdf_path}}", pdf_path)
    script_content = script_content.replace("{{output_dir}}", output_dir)
    script_content = script_content.replace("{{json_prefix}}", json_prefix)
    
    return script_content

# Function to generate a script name with a random suffix
def generate_script_name(base_name="pbs_script") -> str:
    """
    Generates a unique PBS script name with a random suffix.
    Returns: The script name with the random suffix.
    """
    PBS_SCRIPT_RANDOM_SUFFIX_SIZE = 10
    
    random_suffix = generate_random_alphanumeric_sequence(PBS_SCRIPT_RANDOM_SUFFIX_SIZE)
    return f"{base_name}_{random_suffix}.pbs"

# Function to save the generated script in the media directory
def save_script(script_content):
    """
    Saves the PBS script content to a file inside MEDIA_ROOT.
    
    Parameters:
    - script_content: The content of the PBS script.
    - script_name: The name of the file where the script will be saved.
    """
    # Directory to save PBS scripts
    pbs_scripts_dir = os.path.join(settings.MEDIA_ROOT, 'pbs_scripts')
    
    # Generate the script name with a random suffix
    script_name = generate_script_name()
    
    # Ensure the directory exists, otherwise create it
    os.makedirs(pbs_scripts_dir, exist_ok=True)

    # Full path to the file where the script will be saved
    script_path = os.path.join(pbs_scripts_dir, script_name)

    # Save the script to the file
    with open(script_path, 'w') as file:
        file.write(script_content)
    
    return script_path 

def get_pdf2chemicals_pbs_template_path():
    return os.path.join(os.path.dirname(__file__), 'pbs_template', 'pdf2chemicals_pbs_template.pbs')

def get_pdf2chemicals_path():
    return os.path.join(settings.BASE_ROOT_DIR, 'libs', 'pdf2chemicals', 'pdf2chemicals.py')
                    
def generate_pbs_script(pdf_path, output_dir, json_prefix, node_name):
    """
    Generates a PBS script for chemical processing by replacing the necessary variables.
    
    Parameters:
    - template_path: Path to the PBS template file.
    - pdf2chemicals_path: Path to the pdf2chemicals script.
    - pdf_path: Path to the PDF to be processed.
    - output_dir: Directory where the results will be saved.
    - json_prefix: Prefix for the output JSON file.
    """
    JOB_ID_SIZE = 10

    job_id = generate_random_alphanumeric_sequence(JOB_ID_SIZE)

    template_path = get_pdf2chemicals_pbs_template_path()

    pdf2chemicals_path = get_pdf2chemicals_path()

    # Load the template and replace the variables
    script_content = load_and_replace_template(
        job_id,
        node_name,
        template_path, 
        os.getenv('JAVA_HOME'), 
        os.getenv('CONDA_ENV'), 
        pdf2chemicals_path, 
        pdf_path, 
        output_dir, 
        json_prefix
    )

    # Save the generated script in the media directory
    script_path = save_script(script_content)
    
    return script_path

def is_pbs_job_completed(job_id: str) -> bool:
    """Checks if a PBS/Torque job is completed based on tracejob and grep command

    Args:
        job_id (str): Job ID to be checked

    Returns:
        bool: True if the job is complete, False otherwise.
    """
    try:
        # Comando para buscar palavras-chave diretamente com grep
        result = subprocess.run(
            f"tracejob -q -n 30 {job_id} | grep -qE 'resources_used|Exit_status|array_index'",
            shell=True
        )

        # Retorna True se grep encontrou algo, False caso contrário
        return result.returncode == 0

    except FileNotFoundError:
        print("Error: tracejob or grep not found. Check your installation.")
        return False