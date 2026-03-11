import pandas as pd
import requests
import json
import os

#SETUP# This ensures a clean workspace and professional file management
if not os.path.exists('audit_logs'):
    os.makedirs('audit_logs')

# 2. DETECTION ENGINE (Multi-Domain Analysis) 
def detect_threats(df):
    threats = []
    # Domain A: Data Exfiltration (After-hours personal email)
    leaks = df[((df['hour'] < 9) | (df['hour'] > 18)) & 
               (df['to'].str.contains('gmail|yahoo|outlook|hotmail', na=False, case=False))]
    for _, row in leaks.iterrows():
        threats.append({"user": row['user'], "type": "Data Exfiltration", "details": f"Sent to {row['to']} at {row['date']}"})

    # Domain B: Bulk Harvesting (Volume Spike)
    surge = df.groupby(['user', 'hour']).size().reset_index(name='count')
    high_vol = surge[surge['count'] > 50] 
    for _, row in high_vol.iterrows():
        threats.append({"user": row['user'], "type": "Bulk Harvesting", "details": f"Spike of {row['count']} emails at hour {row['hour']}:00"})
    return threats

#3. AI BRAIN (The Detailed NIST Playbook)
def get_ai_playbook(user, threat_type, details):
    url = "http://localhost:11434/api/generate"
    prompt = (
        f"Context: Senior Security Responder at Barclays SOC.\n"
        f"Incident: {threat_type} for user {user}.\n"
        f"Evidence: {details}.\n\n"
        f"Task: Provide a detailed 4-step NIST Playbook:\n"
        f"1. INITIAL ANALYSIS: Technical explanation of why this was flagged.\n"
        f"2. IMMEDIATE CONTAINMENT: Steps to lock account/revoke access.\n"
        f"3. OPERATIONAL ESCALATION: How to notify the Barclays Operational Team.\n"
        f"4. RECOVERY: Long-term monitoring plan."
    )
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False, "options": {"num_predict": 550, "temperature": 0.2}}
    try:
        response = requests.post(url, json=payload, timeout=90)
        return response.json().get('response', "Generation failed.")
    except: return "Connection Error: Is Ollama running?"

#4. MAIN EXECUTION & AUTOMATED REPORTING
if __name__ == "__main__":
    if not os.path.exists('email.csv'):
        print("Error: email.csv not found in this directory!")
    else:
        print("Step 1: Scanning logs for Multi-Domain Anomalies...")
        df = pd.read_csv('email.csv', nrows=100000)
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].dt.hour
        
        found = detect_threats(df)

        if found:
            print(f"[!] {len(found)} threats detected. Generating Forensic Packets...\n")
            
            # For the demo, we process the first 2
            for i, target in enumerate(found[:2]): 
                print(f"--- TRIAGING INCIDENT #{i+1}: {target['user']} ---")
                playbook = get_ai_playbook(target['user'], target['type'], target['details'])
                print(playbook)

                # Generate JSON Audit Trail
                audit_data = {
                    "incident_id": f"BARC-2026-{i+1:03d}",
                    "user": target['user'],
                    "risk_score": 85 if target['type'] == "Data Exfiltration" else 70,
                    "type": target['type'],
                    "evidence": target['details']
                }
                
                # Save to the new audit_logs folder
                file_path = f"audit_logs/incident_{target['user']}_{i+1}.json"
                with open(file_path, "w") as jf:
                    json.dump(audit_data, jf, indent=4)
                
                print(f"\n[SYSTEM] Forensic JSON saved to: {file_path}\n")
                print("="*50)
            
            print(f"\n[SUCCESS] Demo complete. Check the 'audit_logs' folder for full forensic data.")
        else:
            print("No threats detected.")