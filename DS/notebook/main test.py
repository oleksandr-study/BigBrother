from fastapi import FastAPI, File, UploadFile
import nbformat
from nbconvert import PythonExporter
import subprocess

app = FastAPI()


def run_notebook(file_path):

    with open(file_path) as f:
        nb = nbformat.read(f, as_version=4)

    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nb)
    

    temp_py_file = "temp_code.py"
    with open(temp_py_file, 'w') as f:
        f.write(python_code)
    
    result = subprocess.run(["python", temp_py_file], capture_output=True, text=True)
    
    return result.stdout

@app.post("/process_image/")
async def upload_image(file: UploadFile = File(...)):

    file_path = "uploaded_image.jpg"
    with open(file_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)
    

    notebook_output = run_notebook("Automatic_Number_Plate_Recognition.ipynb")
    
    return {"status": "success", "notebook_output": notebook_output}
