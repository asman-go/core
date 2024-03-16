from pathlib import Path
import subprocess

src = Path('src')

"""
    Я хочу пройтись по всем директориям, где есть proto-файлы и сгенерировать python код с интерфейсами для схем
    Потом это надо добавить в setup.py
        https://pypi.org/project/grpcio-tools/
"""
proto_files = set(map(lambda path: Path(path).parent, src.glob('**/*.proto')))
for path in proto_files:
    result = subprocess.run([
        'python',
        '-m',
        'grpc_tools.protoc',
        '-I',
        path,
        f'--python_out={path}',
        f'--pyi_out={path}',
        f'schema.proto',
    ])
