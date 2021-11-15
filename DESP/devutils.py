import os
import sys


def remove_migrations():
    for f1 in os.listdir("platform_apps"):
        if os.path.isdir(f"platform_apps/{f1}"):
            base = f"platform_apps/{f1}/migrations"
            if os.path.exists(base):
                for f2 in os.listdir(base):
                    if f2.startswith("0") and f2.endswith(".py"):
                        os.remove(f"{base}/{f2}")


arg2func = {
    "remove_migrations": remove_migrations,
}

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        func = arg2func.get(arg)
        if func:
            func()
