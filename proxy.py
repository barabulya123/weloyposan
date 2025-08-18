import sys
import os

def main():
    try:
        username = raw_input("Enter username: ")
    except:
        username = input("Enter username: ")
    if not username.strip():
        username = "userproxy"
        print("Using default username: userproxy")
    
    try:
        password_proxy = raw_input("type your password here: ")
    except:
        password_proxy = input("type your password here: ")
    
    try:
        port = raw_input("Enter port (default 1080): ")
    except:
        port = input("Enter port (default 1080): ")
    if not port.strip():
        port = "1080"
        print("Using default port: 1080")
    else:
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                print("Invalid port range. Using default port: 1080")
                port = "1080"
        except ValueError:
            print("Invalid port format. Using default port: 1080")
            port = "1080"
    
    os.system("apt-get update")
    os.system("apt-get -y install build-essential libwrap0-dev libpam0g-dev libkrb5-dev libsasl2-dev")
    os.system("wget --no-check-certificate https://ahmetshin.com/static/dante.tgz")
    os.system("tar -xvpzf dante.tgz")
    os.system("apt-get -y install libwrap0 libwrap0-dev")
    os.system("apt-get -y install gcc make")
    os.system("mkdir /home/dante")
    os.system("""cd dante && ./configure --prefix=/home/dante && make && make install""")
    
    config_content = f"""
            echo '
            logoutput: syslog /var/log/danted.log
            internal: eth0 port = {port}
            external: eth0
            socksmethod: username
            user.privileged: root
            user.unprivileged: nobody
            client pass {{
                from: 0.0.0.0/0 to: 0.0.0.0/0
                log: error
            }}
            socks pass {{
                from: 0.0.0.0/0 to: 0.0.0.0/0
                command: connect
                log: error
                method: username
            }}' > /home/dante/danted.conf
                """
    os.system(config_content)
    
    os.system("useradd --shell /usr/sbin/nologin -m %s" % username)
    os.system('echo "%s:%s" | chpasswd' % (username, password_proxy))
    os.system("apt-get -y install ufw")
    os.system("ufw status")
    os.system("ufw allow ssh")
    os.system(f"ufw allow proto tcp from any to any port {port}")
    os.system("ufw status numbered")
    os.system("echo 'y' | ufw enable")
    
    os.system("""
echo '#!/bin/sh -e
sleep 20
/home/dante/sbin/sockd -f /home/dante/danted.conf -D
exit 0
' > /etc/rc.local
""")
    
    os.system("chmod +x /etc/rc.local")
    os.system("chmod +x /home/dante/sbin/sockd")
    os.system("/home/dante/sbin/sockd -f /home/dante/danted.conf -D")
    os.system("echo 'proxy install success'")
    os.system("echo ' '")
    os.system("echo '________'")
    os.system("echo ' '")
    os.system("echo \"YOUR IP ADDRESS: `hostname -I | awk '{print $1}'`\"")
    os.system(f"echo 'PORT: {port}'")
    os.system("echo 'LOGIN: %s'" % username)
    os.system("echo 'PASSWORD: %s'" % password_proxy)

if __name__ == "__main__":
    main()
