from pathlib import Path
import zipfile

class Zip:
    def zip_folder(self, to_zip, folder_to_zip) -> None:
        folder_path = Path(folder_to_zip)
        # Garante que a pasta de destino do ZIP exista
        Path(to_zip).parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(to_zip, "w", compression=zipfile.ZIP_DEFLATED) as zip_ref:
            # .rglob("*") encontra todos os arquivos e subpastas recursivamente
            for file in folder_path.rglob("*"):
                # Define o caminho dentro do ZIP relativo à pasta que está sendo compactada
                arcname = file.relative_to(folder_path.parent)
                zip_ref.write(file, arcname=arcname)
    
    def unzip_file(self, to_unzip, destination_folder) -> list[str]:
        with zipfile.ZipFile(to_unzip, "r") as zip_ref:
            return zip_ref.extractall(destination_folder)

# Caminho base do seu ambiente Termux/Android
projects = Path("/storage/emulated/0/Programs")

# Pastas que você quer compactar por inteiro
folder1 = projects / "Python Projects/chip8_emulator"
folder2 = projects / "HTML Projects/chip8"

zipf = projects / "compactions"

z = Zip()

# Passamos diretamente o caminho da pasta, não mais a lista de arquivos
z.zip_folder(zipf / "python.zip", folder1)
z.zip_folder(zipf / "html.zip", folder2)
