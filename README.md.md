### AI-Based Cyber Incident Response Agent





#### Overview



This project is an AI-driven cyber incident response prototype designed to analyze SIEM/email logs using User \& Entity Behavior Analytics (UEBA). The system detects anomalous behavior such as after-hours activity and potential data exfiltration, and generates NIST-aligned incident response recommendations using a local LLM.





#### Architecture



Data Ingestion – SIEM / Email logs



Behavior Baseline Modeling – UEBA analysis



Anomaly Detection – Time, Recipient, Volume patterns



AI Reasoning – Local LLM (Gemma 2B via Ollama)



Structured JSON Output – For SIEM/SOAR integration





#### Tech Stack



Python



Pandas



NumPy



Matplotlib



Ollama (Gemma 2B)



JSON





#### Key Features



Behavioral anomaly detection



After-Hours Risk Zone (22:00–06:00)



Offline LLM reasoning



Automated incident response generation

