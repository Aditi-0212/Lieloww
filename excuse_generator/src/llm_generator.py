import subprocess

def generate_response(model_name, prompt):
    process = subprocess.Popen(
        ["ollama", "run", model_name,],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate(input=prompt.encode("utf-8"))

    # Decode output safely
    response = stdout.decode("utf-8", errors="ignore")

    return response.strip()