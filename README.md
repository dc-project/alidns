```angular2html
# For MAC 
export "CFLAGS=-I/usr/local/include -L/usr/local/lib" 
pip install pycrypto
pip install aliyun-python-sdk-core-v3
```

## Usage

```
cp config_same.py config.py

# add domain record example
python dns.py add hub.core.ysbot.top -ip 172.16.0.155

# update domain record example

python dns.py update hub.core.ysbot.top -ip 172.16.0.155
```
