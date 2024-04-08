from pathlib import Path
import subprocess


def generate():
    print('Code generate start')
    src = Path('src')

    """
        Я хочу пройтись по всем директориям, где есть proto-файлы и сгенерировать python код с интерфейсами для схем
        Потом это надо добавить в setup.py
            https://pypi.org/project/grpcio-tools/
    """
    proto_files = set(map(lambda path: Path(path).parent, src.glob('**/*.proto')))
    for path in proto_files:
        print(path)
        result = subprocess.run([
            'python',
            '-m',
            'grpc_tools.protoc',
            '-I',
            path,
            f'--python_out={path}',
            f'--pyi_out={path}',
            'schema.proto',
        ],
        capture_output = True)
        print(result.stdout, result.stderr)

    print('Code generate end')


if __name__ == '__main__':
    generate()
