import os
import datetime
import traceback
import sys
import subprocess

COMMON_REQUIRED_DELIVERABLES = ["DOCKER", "PYTHON", "SQL", "LINUX", "APIS"]
MODULE_1_REQUIRED_DELIVERABLES = ["DBT"]
MODULE_2_REQUIRED_DELIVERABLES = ["GCP_ALMACENAMIENTO"]
COMMON_GRADE = "NOTA COMUNES"
MODULE_1_GRADE = "MDIA_M1"
MODULE_2_GRADE = "MDIA_M2"

# Cada grupo de alumnos indica qué materiales docentes determinan sus
# entregables. MDES comparte los mismos entregables que los grupos MDIA.
# Todos se apoyan en los materiales docentes de MDIA.
MASTER_DELIVERABLE_SOURCES = {
    "MDIAA": "MDIA",
    "MDIAB": "MDIA",
    "MDES": "MDIA",
}

MASTER_TITLES = {
    "MDIAA": "Entregas Grupo MDIA A",
    "MDIAB": "Entregas Grupo MDIA B",
    "MDES": "Entregas Grupo MDES",
}



def get_deliverables(master):
    source = MASTER_DELIVERABLE_SOURCES[master]
    master_path = os.path.join(os.getcwd(), "PROFESORES", source)
    common_path = os.path.join(os.getcwd(), "PROFESORES", "COMUN")
    deliverables = os.listdir(master_path) + os.listdir(common_path)
    return [
        deliverable
        for deliverable in deliverables
        if os.path.isdir(os.path.join(master_path, deliverable))
        or os.path.isdir(os.path.join(common_path, deliverable))
    ]


def check_class(folder_path):
    master = os.path.basename(folder_path)
    source = MASTER_DELIVERABLE_SOURCES[master]
    deliverables=get_deliverables(master)
    if ".DS_Store" in deliverables:
        deliverables.remove(".DS_Store")
    alumnos={}
    
    for alumno in os.listdir(folder_path):
        file_path = os.path.join(folder_path, alumno)
        common_deliverables_completed = 0
        module_1_deliverables_completed = 0
        module_2_deliverables_completed = 0
        if os.path.isdir(file_path):
            delivs={}
            alumnos[alumno]=delivs
            for element in deliverables:
                #print(file_path+"/"+element)
                if os.path.exists(file_path+"/"+element) & os.path.isdir(file_path+"/"+element):
                    print("Entregable "+element+" Existe para el alumno "+alumno)
                    alumnos[alumno][element]=True
                    if element in COMMON_REQUIRED_DELIVERABLES:
                        common_deliverables_completed += 1
                    if source == "MDIA":
                        if element in MODULE_1_REQUIRED_DELIVERABLES:
                            module_1_deliverables_completed += 1
                        if element in MODULE_2_REQUIRED_DELIVERABLES:
                            module_2_deliverables_completed += 1
                else:
                    print("Entregable "+element+" NO Existe para el alumno "+alumno)
                    alumnos[alumno][element]=False
            alumnos[alumno][COMMON_GRADE] = (
                common_deliverables_completed * 10 / len(COMMON_REQUIRED_DELIVERABLES)
            )
            if source == "MDIA":
                alumnos[alumno][MODULE_1_GRADE] = (
                    module_1_deliverables_completed * 10 / len(MODULE_1_REQUIRED_DELIVERABLES)
                )
                alumnos[alumno][MODULE_2_GRADE] = (
                    module_2_deliverables_completed * 10 / len(MODULE_2_REQUIRED_DELIVERABLES)
                )
                
    return alumnos

def check_names(folder_path):
    for alumno in os.listdir(folder_path):
        file_path = os.path.join(folder_path, alumno)
        if os.path.isdir(file_path):
            # list all files in directory
            files = os.listdir(file_path)
            # for element in files:
            #     print(element)


def generate_table(clase,alumnos):
    source = MASTER_DELIVERABLE_SOURCES[clase]
    deliverables=get_deliverables(clase)
    deliverables = deliverables + [COMMON_GRADE]
    if ".DS_Store" in deliverables:
        deliverables.remove(".DS_Store")
    if source == "MDIA":
        deliverables = deliverables + [MODULE_1_GRADE, MODULE_2_GRADE]
    print("Generating Table")
    try:
        table="<table>\n<tr><th>Alumno</th>"
        for element in deliverables:     
            if element in (
                MODULE_1_REQUIRED_DELIVERABLES
                + COMMON_REQUIRED_DELIVERABLES
                + MODULE_2_REQUIRED_DELIVERABLES
            ):
                table+="\n<th>*"+element+"*</th>"
            else:
                table+="\n<th>"+element+"</th>"
        table+="\n</tr>\n"
        table+="<tr>\n"  
        for alumno in sorted(alumnos):            
            table+="<tr>\n<td><a href='https://github.com/a10pepo/EDEM_MDIA2627/tree/main/ALUMNOS/"+clase+"/"+alumno+"'>"+str.upper(alumno)+"</a></td>"
            for element in deliverables:
                if alumnos[alumno][element]:
                    if element in (COMMON_GRADE, MODULE_1_GRADE, MODULE_2_GRADE):
                        table+="\n<td>"+str(alumnos[alumno][element])+"</td>"
                    else:
                        table+="\n<td>✅</td>"
                else:
                    if element in (COMMON_GRADE, MODULE_1_GRADE, MODULE_2_GRADE):
                        table+="\n<td>0.0</td>"
                    else:
                        table+="\n<td>❌</td>"
                    
            table+="\n</tr>\n"
        table+="</table>\n"
        table+="\nLast Checked: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n"

    except Exception as e:
        print("error")
        print(e)
    return table

def modify_readme():
    print("Modifying README.md")
    with open(os.path.join(os.getcwd(),'README.md'), 'r') as file:
        data = file.read()
        parts = data.split('### Estado de las entregas')

    with open(os.path.join(os.getcwd(),'README.md'), 'w') as file:
        print("Writing README.md")
        try: 
            file.write(parts[0])
            file.write('### Estado de las entregas\n')
            masters = list(MASTER_TITLES.items())
            for index, (master, title) in enumerate(masters):
                file.write(f'{title}\n')
                file.write(generate_table(master, check_class(os.path.join(os.getcwd(), "ALUMNOS", master))))
                if index < len(masters) - 1:
                    file.write('\n')
        except Exception as e:
            print("Error writing file")
            print(e)
            traceback.print_exc()
            file.close()
            with open(os.path.join(os.getcwd(),'README.md'), 'w') as file_recov:
                file_recov.write(data)

def check_profesores_modified():
    """
    Check if any files in PROFESORES folder are being modified in this PR/commit.
    Exits with error code 1 if any PROFESORES files are modified.
    """
    try:
        # Try multiple approaches to get modified files
        modified_files = []
        
        # Approach 1: Try origin/main...HEAD (works locally)
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'origin/main...HEAD'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        else:
            # Approach 2: Try HEAD^..HEAD (works for push events)
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD^..HEAD'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            else:
                # Approach 3: Get changed files from git status (last resort)
                result = subprocess.run(
                    ['git', 'diff', '--name-only', 'HEAD'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        
        print(f"\n🔍 Verificando archivos modificados... Total: {len(modified_files)}")
        
        # Check if any file is in PROFESORES folder
        profesores_files = [f for f in modified_files if f.startswith('PROFESORES/')]
        
        if profesores_files:
            print("\n❌ ERROR: No se permite modificar archivos en la carpeta PROFESORES")
            print("\nArchivos modificados en PROFESORES:")
            for file in profesores_files:
                print(f"  - {file}")
            print("\nPor favor, revierte estos cambios antes de continuar.")
            sys.exit(1)
        else:
            print("✅ No se detectaron modificaciones en la carpeta PROFESORES")
            
    except Exception as e:
        print("⚠️  No se pudo verificar archivos modificados")
        print(f"Error: {e}")
        pass

        



if __name__ == '__main__':  
    # First check if PROFESORES folder is being modified
    check_profesores_modified()
    
    for master in MASTER_DELIVERABLE_SOURCES:
        check_names(os.path.join(os.getcwd(), "ALUMNOS", master))
    modify_readme()    
    print("README.md updated")
