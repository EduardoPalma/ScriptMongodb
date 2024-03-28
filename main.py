import subprocess

def execute_script(cant: int, category_time: str, count_time: int):
    process = []
    for index in range(cant):
        process_ = subprocess.Popen(['python', 'main.py', '-index', str(index), "-time", category_time,
                                     "-count", str(count_time)])
        process.append(process_)

    for proces in process:
        proces.wait()

    print("Insercion masiva terminada")

if __name__ == '__main__':
    num_execute = int(input("numero de veces a ejecutar : "))
    category_time = input("Categoria de tiempo hrs o sec : ")
    count_time = int(input("Cantidad de horas o sec : "))
    execute_script(num_execute, category_time=category_time, count_time=count_time)
