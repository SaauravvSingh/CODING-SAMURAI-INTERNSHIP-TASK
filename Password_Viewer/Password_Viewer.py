import subprocess
import re
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not is_admin():
    print("WARNING: Not running as administrator. Passwords will fail to show.\n")

output = subprocess.check_output(
    ["netsh", "wlan", "show", "profiles"],
    text=True,
    encoding="utf-8",
    errors="ignore"
)

profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)

for profile in profiles:
    profile = profile.strip()
    try:
        details = subprocess.run(
            ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True
        ).stdout
    except subprocess.CalledProcessError as e:
        print(f"Wi-Fi: {profile}")
        print(f"Password: Error retrieving ({e.stderr.strip() or 'access denied'})")
        print("-" * 40)
        continue

    password_match = re.search(r"Key Content\s*:\s*(.*)", details)
    password = password_match.group(1).strip() if password_match else "No password"
    print(f"Wi-Fi: {profile}")
    print(f"Password: {password}")
    print("-" * 40)