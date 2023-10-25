import os
import shutil
import zipfile
import tarfile


def extract_file_system(archive_path, destination_path):
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination_path)
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(destination_path)
    else:
        print("Неподдерживаемый формат архива")
        exit(1)


def list_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            print(file)
    except FileNotFoundError:
        print(f"Директория {directory_path} не существует")


def main():
    archive_path = input("Введите путь к архиву: ")
    destination_path = "temp_directory"  # Временная директория для извлечения файловой системы
    extract_file_system(archive_path, destination_path)

    current_directory = os.path.abspath(destination_path)

    while True:
        command = input(f"{current_directory} $ ")
        if command == "pwd":
            print(current_directory)
        elif command == "ls":
            list_directory(current_directory)
        elif command.startswith("cd "):
            new_directory = command[3:]
            new_path = os.path.join(current_directory, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                current_directory = os.path.abspath(new_path)
            else:
                print(f"Директория {new_directory} не существует")
        elif command.startswith("cat "):
            file_name = command[4:]
            file_path = os.path.join(current_directory, file_name)
            try:
                with open(file_path, 'r') as file:
                    print(file.read())
            except FileNotFoundError:
                print(f"Файл {file_name} не найден")
        elif command == "exit":
            break
        else:
            print("Неподдерживаемая команда")


if __name__ == "__main__":
    main()