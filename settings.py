import os

DEBUG = os.getenv("DEBUG", False)

# si debug es TRUE, incluira estas librerias
if DEBUG:
    print("We are in debug")
    from pathlib import Path
    from dotenv import load_dotenv
    env_path = Path(".") / ".env.debug"
    load_dotenv(dotenv_path=env_path)
    from settings_files.dev import *

# de lo contrario, incluira solo este
else:
    print("Production")
    from settings_files.prod import *
