from __future__ import annotations
import subprocess
from enum import Enum
import sys
import os
import subprocess


def main(mode:Mode)->None:
    base_image:str
    secret_folder:str
    if mode == Mode.CPU:
        base_image = "ubuntu:20.04"
        secret_folder = "dev"
    if mode == Mode.GPU:
        base_image = "tensorflow/tensorflow:2.6.0"
        secret_folder = "prod"




    with open(os.path.join("./secret",secret_folder,"student_id.txt")) as student_ids:
        is_first_build_image = True
        for student_info in [ s.replace("\n","") for s in student_ids.readlines()]:

            student_id = student_info.split()[0]
            dockerimage = student_info.split()[1]

            docker_compose_str:str
            

            if dockerimage == "base":
                with open(os.path.join('./container-template','dockerfile.txt'),"r") as dockerfile:
                    dockerfile_str = replaction_string(dockerfile.read(),base_image,student_id,dockerimage)

            
                with open(os.path.join('./container-template','docker-compose.txt'),"r") as docker_compose:
                    docker_compose_str = replaction_string(docker_compose.read(),base_image,student_id,"brainlab-base-image")


                if is_first_build_image:
                    dockerfile_path = os.path.join("./student-containers","base.Dockerfile")
                    with open(dockerfile_path,"w") as output_dockerfile:
                        output_dockerfile.write(dockerfile_str)
                    
                    subprocess.run(f"docker build -t brainlab-base-image -f {dockerfile_path} .", shell=True, check=True)
                    is_first_build_image = not is_first_build_image
                

            if dockerimage == "custom":
                with open(os.path.join('./container-template','docker-compose-custom.txt'),"r") as docker_compose:
                    docker_compose_str = replaction_string(docker_compose.read(),base_image,student_id,f"{student_id}.Dockerfile")
            docker_compose_path = os.path.join("./compose-files",secret_folder,f"{student_id}-compose.yml")

            
            with open(docker_compose_path,"w") as output_compose:
                output_compose.write(docker_compose_str)
        
def replaction_string(string:str,base_image:str,student_id:str,dockerimage:str)->str:
    return string.replace("--base_image--",base_image).replace("--student_id--",student_id).replace("--dockerimage--",dockerimage)

class Mode(Enum):
    CPU:str = 'CPU'
    GPU:str = 'GPU'

    @staticmethod
    def factory(data:str)->Mode:
        data = data.upper()
        if data == Mode.CPU.value:
            return Mode.CPU
        if data == Mode.GPU.value:
            return Mode.GPU
        raise RuntimeError()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise RuntimeError("args: Mode:cpu/gpu")
    mode:Mode = Mode.factory(sys.argv[1])
    
    main(mode)