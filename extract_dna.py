import zipfile
import json
import os

# TARGET: The specific vault and file we found
TARGET_ZIP = "archives/colab_sync_20260108_013035.zip"
TARGET_FILE = "data/logs/metrics_log.jsonl"

def extract_god_mode():
    print("🧪 SRCL SURGICAL EXTRACTION")
    print("==========================")
    
    if not os.path.exists(TARGET_ZIP):
        print(f"❌ Error: Cannot find {TARGET_ZIP}")
        return

    print(f"💉 Injecting into: {TARGET_ZIP}")
    
    try:
        with zipfile.ZipFile(TARGET_ZIP, 'r') as z:
            # Check if file exists in zip
            if TARGET_FILE not in z.namelist():
                # Sometimes paths are different, let's search for the filename
                found = False
                for f in z.namelist():
                    if f.endswith("metrics_log.jsonl"):
                        TARGET_FILE_ACTUAL = f
                        found = True
                        break
                if not found:
                    print("❌ Could not locate metrics_log.jsonl inside zip.")
                    return
            else:
                TARGET_FILE_ACTUAL = TARGET_FILE
            
            print(f"📄 Reading: {TARGET_FILE_ACTUAL}")
            
            with z.open(TARGET_FILE_ACTUAL) as f:
                content = f.read().decode('utf-8')
                lines = content.splitlines()
                
                best_entropy = 100.0
                winning_dna = None
                
                # Scan line by line for the -412 record
                for line in lines:
                    try:
                        data = json.loads(line)
                        ent = data.get('entropy_A', 100)
                        
                        # We look for that specific Deep Research finding
                        if ent < -400:
                            best_entropy = ent
                            winning_dna = data
                    except:
                        continue
                
                if winning_dna:
                    print("\n🏆 GOD MODE CONSTANTS RECOVERED")
                    print("==============================")
                    print(f"📉 Entropy:   {winning_dna.get('entropy_A')}")
                    print(f"🔗 Coherence: {winning_dna.get('coherence_A')}")
                    print(f"🧬 ALPHA (Vol):   {winning_dna.get('alpha')}")
                    print(f"🧬 BETA (Trend):  {winning_dna.get('beta')}")
                    print(f"🧬 GAMMA (Grav):  {winning_dna.get('gamma')}")
                    print(f"🧬 D (Fractal):   {winning_dna.get('D')}")
                    
                    # Save them to a file so we don't lose them again
                    with open("god_mode_constants.json", "w") as outfile:
                        json.dump(winning_dna, outfile, indent=4)
                    print("\n✅ Saved to 'god_mode_constants.json'")
                    
                else:
                    print("⚠️ File opened, but could not re-find the -412 entropy line.")
                    
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")

if __name__ == "__main__":
    extract_god_mode()
