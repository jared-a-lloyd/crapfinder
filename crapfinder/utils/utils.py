from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.resolve()

if __name__ == '__main__':
    get_project_root()