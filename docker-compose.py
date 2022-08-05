from __future__ import annotations
import subprocess
from enum import Enum
import sys
import os

def main(mode:Mode, cmd:str)->None:
    directory:str = f"./compose-files/{mode.value}".lower()
    compose_files:list[str] = os.listdir(directory)
  
    compose_files = [ os.path.join(directory,f) for f in compose_files]
    compose_string:str = f"-f {' -f '.join(compose_files)}"
    final_cmd = f"docker-compose -p brain-lab-{mode.value.lower()} {compose_string} {cmd}"
    subprocess.run(final_cmd, shell=True, check=True)
    # print(final_cmd)

class Mode(Enum):
    DEV:str = 'DEV'
    PROD:str = 'PROD'

    @staticmethod
    def factory(data:str)->Mode:
        data = data.upper()
        if data == Mode.DEV.value:
            return Mode.DEV
        if data == Mode.PROD.value:
            return Mode.PROD
        raise RuntimeError()
if __name__ == "__main__":

    mode:Mode
    cmd:str
    
    if  "--dev" in sys.argv[1] or "--prod" in sys.argv[1]:
        mode = Mode.factory(sys.argv[1].replace("--",""))
        cmd = " ".join(sys.argv[2:len(sys.argv)])
    else:
        mode = Mode.DEV
        cmd = " ".join(sys.argv[1:len(sys.argv)])

    main(mode,cmd)