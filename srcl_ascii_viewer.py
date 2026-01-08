import os
import time
import subprocess

# Directory where the SRCL-MQ results are stored
results_dir = "/home/schlieve001/origin/continuity_lab/results_srclmq"

# Find all step images
frames = sorted([
    f for f in os.listdir(results_dir)
    if f.startswith("srclmq_step_") and f.endswith(".png")
])

if not frames:
    print("⚠️ No SRCL-MQ frames found in", results_dir)
    exit(1)

print(f"🌀 Displaying {len(frames)} SRCL-MQ frames as ASCII animation...")
print("Press Ctrl+C to stop.\n")

# Loop through frames as an ASCII animation
try:
    for frame in frames:
        frame_path = os.path.join(results_dir, frame)
        # Clear the screen each frame
        os.system("clear")
        print(f"🎞️ Frame: {frame}\n")
        subprocess.run(["jp2a", "--width=80", frame_path])
        time.sleep(0.5)  # delay between frames (adjust for speed)
except KeyboardInterrupt:
    print("\n🛑 Animation stopped by user.")
