from pathlib import Path
from datetime import datetime

#This path is inside the Docker volume
log_dir = Path("/data/logs")
log_dir.mkdir(parents=True, exist_ok=True)

out = log_dir / "hello.txt"

with out.open("a") as f:
    f.write(f"Hello docker volume: {datetime.now()}\n")

print("Written to Docker volume:")
print(out)
