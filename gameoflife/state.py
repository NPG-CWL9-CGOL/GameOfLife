import numpy as np

from gameoflife.grid import Grid
from gameoflife.settings import AppSettings

class ProjectState:
    """Obsługa stanu projektu - obsługa plików"""

    def __init__(self, project_path, name, grid, settings=None):
        self.project_path = project_path
        self.name = str(name)

        self.grid = grid
        self.settings = settings if settings is not None else AppSettings()

    @classmethod
    def from_file(cls, project_path):
        """Odczyt z pliku .npz"""
        
        with np.load(project_path, allow_pickle=True) as bundle:
            name = bundle["name"].item()
            grid_data = bundle["grid"]

            return cls(
                project_path,
                name,
                Grid.from_data(grid_data)
            )

    def save(self):
        """Zapis do pliku"""

        path = self.project_path

        if not path.endswith('.npz'):
            path += '.npz'

        np.savez(
            path, 
            name=self.name, 
            grid=self.grid.data
        )
