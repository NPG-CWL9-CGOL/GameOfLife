"""Moduł odpowiedzialny za zarządzanie stanem projektu i operacje na plikach."""

from __future__ import annotations

import numpy as np

from gameoflife.grid import GridData
from gameoflife.settings import AppSettings

class ProjectState:
    """Obsługa stanu projektu - obsługa plików"""

    def __init__(self, project_path: str, name: str, grid: GridData, settings: AppSettings | None = None):
        """Inicjalizuje nowy stan projektu z podaną ścieżką, nazwą i danymi siatki."""
        self.project_path = project_path
        self.name = str(name)

        self.grid = grid
        self.settings = settings if settings is not None else AppSettings()

    @classmethod
    def from_file(cls, project_path: str) -> ProjectState:
        """Odczyt z pliku .npz"""
        
        with np.load(project_path, allow_pickle=True) as bundle:
            name = bundle["name"].item()
            grid_data = bundle["grid"]

            return cls(
                project_path,
                name,
                GridData.from_data(grid_data)
            )

    def save(self) -> None:
        """Zapis do pliku"""

        path = self.project_path

        if not path.endswith('.npz'):
            path += '.npz'

        np.savez(
            path, 
            name=self.name, 
            grid=self.grid.data
        )
