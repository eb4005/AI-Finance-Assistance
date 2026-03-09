import subprocess
import sys

services = [
    ("agents.api_agent_service.main", 8001),
    ("agents.retriever_agent_service.main", 8002),
    ("agents.scraping_agent_service.main", 8003),
    ("agents.llm_agent_service.main", 8004),
    ("agents.voice_agent.voice_agent", 8005),
    ("orchestrator.orchestrator_service.main", 8000),
]

processes = []

for module, port in services:
    print(f"Starting {module} on port {port}")
    p = subprocess.Popen([sys.executable, "-m", "uvicorn", f"{module}:app", "--port", str(port)])
    processes.append(p)

print("All services started. Press Ctrl+C to stop.")
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Shutting down services...")
    for p in processes:
        p.terminate()
