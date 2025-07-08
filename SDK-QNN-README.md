# NPU WSL Setup Guide

## Launch QAIRT Dependency Checker

```bash
sudo "/mnt/c/Program Files/qairt/2.36.0.250627/bin/check-linux-dependency.sh"
c

---

## 📄 Linux Setup Documentation

Refer to the official documentation:

[Qualcomm Linux Setup Documentation](https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-50/linux_setup.html?product=1601111740009302)

---

## 🛠️ SDK Environment Setup

```bash
cd /mnt/c/Users/qc_de/Documents/GitHub/Never-answer
# Navigate to the SDK bin directory
cd "/mnt/c/Program Files/qairt/2.36.0.250627/bin"
# Source the environment setup script
source ./envsetup.sh

export QNN_SDK_ROOT="/mnt/c/Qualcomm/AIStack/QAIRT/<version>"


cd /mnt/c/Users/qc_de/Documents/GitHub/Never-answer
cd "/mnt/c/Program Files/qairt/2.36.0.250627/bin"
source ./envsetup.sh


```
Installe model
```bash

cd /mnt/c/Users/qc_de/Documents/GitHub/Never-answer/backend
source backend_env/bin/activate
pip install -U "qai-hub-models[llama-v3-8b-instruct]"

# Model hub Llama location
python -c "import qai_hub_models; print(qai_hub_models.__file__)"
ls backend_env/lib/python3.10/site-packages/qai_hub_models
# Create a Python Script in WSL
python run_llama.py



```

---

## 🧩 Install Legacy Dependencies

### 1. Add Ubuntu 20.04 Focal Repository

```bash
sudo nano /etc/apt/sources.list.d/focal-repo.list
```

Add this line:

```
deb http://archive.ubuntu.com/ubuntu focal-security main universe
```

Then run:

```bash
sudo apt update
sudo apt install libncurses5
```

### 2. Install Linux Build Dependencies

```bash
sudo "/mnt/c/Program Files/qairt/2.36.0.250627/bin/check-linux-dependency.sh"
```

### 3. Manually Install `libffi7`

```bash
wget http://es.archive.ubuntu.com/ubuntu/pool/main/libf/libffi/libffi7_3.3-4_amd64.deb
sudo dpkg -i libffi7_3.3-4_amd64.deb
```

### 4. Install Legacy Libraries (`libncurses5`, `libtinfo5`, `libaio1`)

```bash
curl -O http://launchpadlibrarian.net/648013227/libncurses5_6.4-2_amd64.deb
curl -O http://launchpadlibrarian.net/648013231/libtinfo5_6.4-2_amd64.deb
curl -O http://launchpadlibrarian.net/646633572/libaio1_0.3.113-4_amd64.deb

sudo dpkg -i libncurses5_6.4-2_amd64.deb \
              libtinfo5_6.4-2_amd64.deb \
              libaio1_0.3.113-4_amd64.deb

# Fix any broken dependencies
sudo apt --fix-broken install
```

---

## 🔄 Re-Check SDK Dependencies

```bash
sudo "/mnt/c/Program Files/qairt/2.36.0.250627/bin/check-linux-dependency.sh"
```

---

## ✅ Verify Environment Setup

```bash
${QAIRT_SDK_ROOT}/bin/envcheck -c
```

---

## 🔧 Environment Variable Setup

```bash
nano ~/.bashrc
source "/mnt/c/Program Files/qairt/2.36.0.250627/bin/envsetup.sh"
source ~/.bashrc
```

---

## 🐍 Install QNN SDK Python Dependencies

### Add Deadsnakes PPA and Install Python 3.10

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

sudo apt install python3.10 python3.10-venv python3.10-distutils
python3.10 --version
# Expected: Python 3.10.x
```

---

## 🧪 Create and Configure Python Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv ~/qairt-venv
source ~/qairt-venv/bin/activate

# Install pip tools and run Python dependency check
pip install setuptools
which pip
python "${QAIRT_SDK_ROOT}/bin/check-python-dependency"

# Persist venv activation
echo 'source ~/qairt-venv/bin/activate' >> ~/.bashrc
source ~/.bashrc
```

---

## 🔨 Build Python from Source (Optional)

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev \
                    libreadline-dev libsqlite3-dev libffi-dev wget

cd /tmp
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
tar xvf Python-3.10.13.tgz
cd Python-3.10.13
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall  # Installs as python3.10
```

---

## 🌱 New Project Environment Setup

```bash
cd /mnt/c/Users/jhonn/GitHub/Never-answer/backend
python3.10 -m venv snapdragon-env
source snapdragon-env/bin/activate

pip install --upgrade pip setuptools
python "${QAIRT_SDK_ROOT}/bin/check-python-dependency"
```

---

## 📦 Install Required Python Packages

```bash
pip3 install torch==2.4.0 torchvision==0.19.0 tensorflow==2.10.1 \
            tflite==2.3.0 onnx==1.16.1 onnxruntime==1.18.0 onnxsim==0.4.36
```

> 💡 For PyTorch, if `pip` fails, download the appropriate binary from the [PyTorch previous versions page](https://pytorch.org/get-started/previous-versions/)

| Package     | Version | Description                 |
| ----------- | ------- | --------------------------- |
| torch       | 2.4.0   | PyTorch (QAIRT)             |
| torchvision | 0.19.0  | Computer vision for PyTorch |
| tensorflow  | 2.10.1  | TensorFlow                  |
| tflite      | 2.3.0   | TensorFlow Lite             |
| onnx        | 1.16.1  | ONNX model exchange         |
| onnxruntime | 1.18.0  | ONNX runtime                |
| onnxsim     | 0.4.36  | ONNX simplifier             |

---

## ⚙️ Step 5: Dependencies for Target Hardware

Run dependency check again:

```bash
sudo "/mnt/c/Program Files/qairt/2.36.0.250627/bin/check-linux-dependency.sh"
```

---

### 🧠 CPU Target

* **x86\_64**: Install Clang 14

```bash
sudo apt update
sudo apt install clang-14 lld-14
clang-14 --version  # Should show version 14.x.x
```

---

### 🎮 GPU Target

> Requires OpenCL ≥ 1.2

```bash
sudo apt update
sudo apt install opencl-headers ocl-icd-opencl-dev
```

#### Intel (CPU & iGPU)

```bash
sudo apt install intel-opencl-icd
```

#### NVIDIA

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt update
sudo apt install nvidia-driver-<version>
```

#### AMD

```bash
wget https://repo.radeon.com/amdgpu-install/6.4.1/ubuntu/noble/amdgpu-install_6.4.60401-1_all.deb
sudo apt install ./amdgpu-install_6.4.60401-1_all.deb
sudo amdgpu-install --usecase=graphics,opencl --opencl=rocr --no-dkms
sudo usermod -a -G render,video $USER && sudo reboot
```

```bash
clinfo  # Verify OpenCL platform/devices
```

---

## 🧪 Test OpenCL

```bash
cd /mnt/c/Users/jhonn/GitHub/Never-answer/backend
source snapdragon-env/bin/activate  # Or use your active venv
pip install pyopencl numpy

python test_opencl.py
```

---

```

Let me know if you want this converted to a downloadable `.md` file or need sections tailored for automation scripts.
```
