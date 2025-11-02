import subprocess
import json
import time
import shutil
import os

import os
os.environ['OLLAMA_HOST'] = 'http://10.139.126.46:11437'

import subprocess
import json
import time
import shutil
import os

def find_ollama_path():
    """Find the ollama binary path"""
    # Use the exact path from your system
    ollama_path = '/packages/apps/ollama/0.12.3/bin/ollama'
    
    if os.path.exists(ollama_path):
        return ollama_path
    
    # Try to find ollama in PATH as fallback
    ollama_path = shutil.which('ollama')
    if ollama_path:
        return ollama_path
    
    # Common installation paths
    common_paths = [
        '/usr/local/bin/ollama',
        '/usr/bin/ollama',
        os.path.expanduser('~/.ollama/bin/ollama'),
        '/opt/ollama/bin/ollama'
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return 'ollama'  # Fallback to just 'ollama'

def query_ollama(model_name, prompt, stream=False):
    """
    Query an Ollama model with a given prompt
    
    Args:
        model_name: Name of the model (e.g., 'deepseek-r1:8b')
        prompt: Input text/question
        stream: Whether to stream the response (default: False)
    
    Returns:
        The model's response as a string
    """
    try:
        ollama_cmd = find_ollama_path()
        
        # Prepare the command
        cmd = [ollama_cmd, 'run', model_name, prompt]
        
        if stream:
            # Stream output in real-time
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=os.environ.copy(),
                bufsize=0,  # Unbuffered
                universal_newlines=True
            )
            
            output = []
            print(f"\nStreaming response from {model_name}:")
            print("-" * 80)
            
            # Read character by character for true streaming
            while True:
                char = process.stdout.read(1)
                if not char:
                    break
                print(char, end='', flush=True)
                output.append(char)
            
            # Wait for process to complete
            process.wait(timeout=300)
            
            print()  # New line after streaming
            
            if process.returncode == 0:
                return ''.join(output).strip()
            else:
                error_msg = process.stderr.read().strip() if process.stderr else "Unknown error"
                return f"Error: {error_msg}"
        else:
            # Non-streaming: capture all output at once
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                env=os.environ.copy()
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return f"Error: {error_msg}"
    
    except subprocess.TimeoutExpired:
        return "Error: Request timed out"
    except FileNotFoundError:
        return "Error: Ollama not found. Please ensure Ollama is installed and in your PATH"
    except Exception as e:
        return f"Error: {str(e)}"


def run_inference_on_all_models(prompt, models):
    """
    Run inference on all specified models and display results
    
    Args:
        prompt: Input text to send to all models
        models: List of model names
    """
    results = {}
    
    print("=" * 80)
    print(f"INPUT PROMPT: {prompt}")
    print("=" * 80)
    print()
    
    for model in models:
        print(f"\n{'=' * 80}")
        print(f"MODEL: {model}")
        print(f"{'=' * 80}")
        
        start_time = time.time()
        response = query_ollama(model, prompt)
        elapsed_time = time.time() - start_time
        
        print(f"\nRESPONSE:")
        print(response)
        print(f"\nTime taken: {elapsed_time:.2f} seconds")
        print(f"{'=' * 80}\n")
        
        results[model] = {
            'response': response,
            'time': elapsed_time
        }
    
    return results

import subprocess
result = subprocess.run(['/packages/apps/ollama/0.12.3/bin/ollama', 'list'], 
                       capture_output=True, text=True)
print(result.stdout)


models = [
    # 'llama3.2:latest'
    # 'deepseek-r1:8b',

    'gpt-oss:20b',
    'gemma3:27b',
    'qwen3:32b',

    # 'llama3.3:70b',
    # 'deepseek-r1:70b',
    # 'llama3.1:405b',
    # 'gpt-oss:120b',
]

input_prompt = "who is the strongest character in one piece"
results = run_inference_on_all_models(input_prompt, models)


print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
for model, data in results.items():
    print(f"{model}: {data['time']:.2f}s")
print("=" * 80)