import zipfile
import json
import os

TARGET_ZIP = "archives/colab_sync_20260108_013035.zip"

def recover_config():
    print("search for GENESIS CONFIGURATION...")
    
    try:
        with zipfile.ZipFile(TARGET_ZIP, 'r') as z:
            # 1. Check for a dedicated config file first
            for f in z.namelist():
                if "config" in f or "params" in f:
                    print(f"📄 Found Config File: {f}")
                    with z.open(f) as cfg:
                        print(cfg.read().decode('utf-8'))
            
            # 2. Scan the metrics log for the first line (Header)
            # This is usually where the run parameters are logged
            for f in z.namelist():
                if f.endswith("metrics_log.jsonl"):
                    print(f"📄 Scanning Header of: {f}")
                    with z.open(f) as log:
                        # Read the first 5 lines looking for 'alpha'
                        for i in range(5):
                            line = log.readline().decode('utf-8')
                            if "alpha" in line:
                                print("\n🏆 FOUND GENESIS CONSTANTS:")
                                data = json.loads(line)
                                print(json.dumps(data, indent=4))
                                return
                            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    recover_config()
