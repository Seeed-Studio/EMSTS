## EMSTS(embedded system test software)
```
sudo su
apt update
apt install python3-pip python3-mraa  python3-upm python3-dev 
```
### lib->display:
```
sudo su
apt install libfreetype6-dev libsdl1.2-dev libsdl-image1.2-dev \
fontconfig fonts-freefont-ttf libsdl-ttf2.0-dev libsmpeg-dev  libportmidi-dev \
libsdl-mixer1.2-dev

python3 -m pip install -U pygame --user
```
### lib->recorder:
```
sudo su
apt install python3-pyaudio
```
### modules->console->apa102
```
sudo su 
git clone --depth 1 https://github.com/respeaker/pixel_ring.git
cd pixel_ring
pip3 install -U -e .
```

### modules->microphone:
```
sudo su
pip3 install evdev
```

### modules->bluetooth:
```
apt install python3-pexpect
```