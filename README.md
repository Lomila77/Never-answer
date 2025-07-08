# Snapdragon Windows & WSL Ubuntu Launch Guide

## Backend (Python) Setup in WSL Ubuntu

1. **Open WSL Ubuntu terminal.**
2. **Navigate to your project backend directory:**
   ```bash
   cd /mnt/c/Users/qc_de/Documents/GitHub/Never-answer/backend
   ```
3. **(Optional) Create a virtual environment if not already created:**
   ```bash
   sudo add-apt-repository universe
   sudo apt update
   sudo apt install python3-venv

   apt install python3.10-venv
   python3 -m venv backend_env
   ```
4. **Activate the virtual environment:**
   ```bash
   source backend_env/bin/activate
   export PYTHONPATH=$PYTHONPATH:/mnt/c/Users/qc_de/Documents/GitHub/Never-answer
   ```
5. **Install Python requirements:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Set your Groq API key and run the backend:**
   ```bash
   export GROQ_API_KEY="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"
   cd ..
   pip install uvicorn
   pip install fastapi
   pip install groq
   pip install langchain
   pip install langchain_huggingface
   pip install langchain-community
   pip install langchain-core
   pip install sentence-transformers

   python3 -m backend.main
   ```

---

## Frontend (Vite + Tauri) Setup in Windows PowerShell

1. **Open a PowerShell terminal.**
2. **Navigate to the frontend directory:**
   ```powershell
   cd "C:\Users\qc_de\Documents\GitHub\Never-answer\frontend"
   ```
3. **Install frontend dependencies:**
   ```powershell
   npm install
   ```
4. **(Optional) Install Tauri CLI if not already installed:**
   ```powershell
   npm install -D @tauri-apps/cli
   ```
5. **Start the Vite development server:**
   ```powershell
   cd C:\Users\qc_de\Documents\GitHub\Never-answer\frontend
   npm run dev
   ```
   - Open the URL shown in the terminal (usually http://localhost:5173) in your browser.
6. **(In a new PowerShell terminal) Launch the Tauri desktop app:**
   ```powershell
   Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
   Start-Process .\rustup-init.exe -Wait
   cd C:\Users\qc_de\Documents\GitHub\Never-answer\frontend
   dir package.json
   npm run tauri
   ```
   If tauri installation fails
   ```
   C:\Users\qc_de\.cargo\bin
   dir "$env:USERPROFILE\.cargo\bin\cargo.exe"
   cargo --version
   If That Still Fails: Manually Add Cargo to PATH
   If cargo still isn't recognized, add it manually:
   Open System Properties → Environment Variables
   Under User variables, find or create a variable called PATH
   npm run tauri
   ```
---

## Tips & Troubleshooting
- Always run backend commands in WSL Ubuntu, not in Windows PowerShell.
- Always run frontend commands in Windows PowerShell, not in WSL Ubuntu.
- If you need to set the API key in Windows for some reason, use:
  ```powershell
  $env:GROQ_API_KEY = "your_api_key_here"
  ```
- If you want a shortcut to activate your backend environment, add this alias to your `~/.bashrc` in WSL:
  ```bash
  alias backend_never_answer='cd ~/never-answer/backend && source backend_env/bin/activate'
  ```

---

## WSL Ubuntu Setup (if not already done)
- Install WSL and Ubuntu from Windows Terminal:
  ```powershell
  wsl --install -d Ubuntu
  ```
- If you need to enable features:
  ```powershell
  dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
  dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
  dism.exe /online /enable-feature /featurename:Hyper-V /all /norestart
  ```
- Update and install Python in Ubuntu:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install python3-pip python3-venv -y
  ```

---

## Summary
- **Backend:** WSL Ubuntu (Linux terminal)
- **Frontend:** Windows PowerShell
- **API Key:** Set in WSL for backend, or hardcoded fallback in code

You're ready to develop and launch Never-answer on Windows with WSL Ubuntu!


