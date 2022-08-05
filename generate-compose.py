from __future__ import annotations
import subprocess
from enum import Enum
import sys
import os
import subprocess


def main(mode:str)->None:
    
    secret_folder:str = mode


    with open(os.path.join("./secret",secret_folder,"users.txt")) as user_ids:
        is_first_buildimage_cpu = True
        is_first_buildimage_gpu = True
        for user_info in [ s.replace("\n","") for s in user_ids.readlines()]:
            if user_info == "":
                continue
            if user_info[0] == "#":
                continue

            user_id = user_info.split()[0]
            dockerimage,tag = user_info.split()[1].split(":")

            docker_compose_str:str
            
            building_cmd:str
            if dockerimage == "base":
                building_cmd=f"""image: brainlab-baseimage:{tag}-0.0.1"""
                

            
                with open(os.path.join('./container-template','docker-compose.txt'),"r") as docker_compose:
                    docker_compose_str = replaction_string(docker_compose.read(),building_cmd,user_id)

                if "cpu" in tag:
                    if is_first_buildimage_cpu:
                        
                        dockerfile_path = os.path.join("./container-template","base-cpu.Dockerfile")                        
                        subprocess.run(f"docker build -t brainlab-baseimage:{tag}-0.0.1 -f {dockerfile_path} .", shell=True, check=True)
                        is_first_buildimage_cpu = not is_first_buildimage_cpu

                if "gpu" in tag:
                    if is_first_buildimage_gpu:
                        dockerfile_path = os.path.join("./container-template","base-gpu.Dockerfile")                     
                        subprocess.run(f"docker build -t brainlab-baseimage:{tag}-0.0.1 -f {dockerfile_path} .", shell=True, check=True)
                        is_first_buildimage_gpu = not is_first_buildimage_gpu
                

            if dockerimage == "custom":
                building_cmd=f"""build:
      context: ../../user-custom-dockerfile
      dockerfile: {tag}.Dockerfile"""
                with open(os.path.join('./container-template','docker-compose.txt'),"r") as docker_compose:
                    docker_compose_str = replaction_string(docker_compose.read(),building_cmd,user_id)
            docker_compose_path = os.path.join("./compose-files",secret_folder,f"{user_id}-compose.yml")

            
            with open(docker_compose_path,"w") as output_compose:
                output_compose.write(docker_compose_str)
        
def replaction_string(string:str,build_image_cmd:str,user_id:str)->str:
    user_volume:str = user_id.split("-")[0]
    return string.replace("--building_cmd--",build_image_cmd).replace("--user_id--",user_id).replace("--user_volume--",user_volume)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise RuntimeError("args: Mode:dev/prod")
    mode:str = sys.argv[1]
    
    main(mode)