import subprocess

file_path = "C:\\Users\\Ali Can\\Desktop\\Proje\\DinamikProje\\requirements.txt"

with open(file_path,'r') as file:
    rows = file.readlines()

for row in rows:
    command = row.strip()

    if command:
        try:
            run_command = subprocess.run(command,shell=True,check=True,stdout=subprocess.PIPE)
            print(f"Komut {command} \n Ciktisi : \n {run_command.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"{command} \n Hata : \n {e.stderr.decode()}")