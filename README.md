# QRanibal the Scanibal

This is a simple Flask web app I wrote to scan QR codes and extract DEV EUIs using the device's camera.

## Usage

Before all else, let's clone the repo:

```bash
git clone https://github.com/Ducktatorrr/qranibal-the-scanible.git
```

There are two ways to run this app:

### Docker

#### 1. Build the Docker image:

```bash
docker build -t qranibal .
```

#### 2. Run the Docker image:

```bash
docker run -p 5000:5000 qranibal
```

### From python source

#### 0. Prerequisites:

You will need zbar installed on your system.

On **Linux**:

```bash
sudo apt-get install libzbar0
```

On **Mac OS X**:

```bash
brew install zbar
```

**Optional**: Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

#### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 3. Run the app:

```bash
python app.py
```
