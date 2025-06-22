"""
Exportadores para diferentes formatos de datos.
"""

import json
import csv
from typing import List, Dict, Any, Protocol
from abc import ABC, abstractmethod


class Exporter(Protocol):
    """Protocolo para exportadores de datos."""
    
    def export(self, data: List[Dict[str, Any]], output_file: str) -> str:
        """Exportar datos a un archivo."""
        ...


class BaseExporter(ABC):
    """Clase base para exportadores."""
    
    @abstractmethod
    def export(self, data: List[Dict[str, Any]], output_file: str) -> str:
        """Exportar datos a un archivo."""
        pass


class JSONExporter(BaseExporter):
    """Exportador para formato JSON."""
    
    def export(self, data: List[Dict[str, Any]], output_file: str) -> str:
        """
        Exportar datos a formato JSON.
        
        Args:
            data: Datos a exportar
            output_file: Archivo de salida
            
        Returns:
            Ruta del archivo generado
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_file


class CSVExporter(BaseExporter):
    """Exportador para formato CSV."""
    
    def export(self, data: List[Dict[str, Any]], output_file: str) -> str:
        """
        Exportar datos a formato CSV.
        
        Args:
            data: Datos a exportar
            output_file: Archivo de salida
            
        Returns:
            Ruta del archivo generado
        """
        if not data:
            # Crear archivo vacío si no hay datos
            with open(output_file, 'w', encoding='utf-8') as f:
                pass
            return output_file
        
        # Obtener todas las claves únicas de todos los registros
        all_keys = set()
        for item in data:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        fieldnames = sorted(list(all_keys))
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in data:
                if isinstance(item, dict):
                    # Asegurar que todos los campos estén presentes
                    row = {key: item.get(key, '') for key in fieldnames}
                    writer.writerow(row)
        
        return output_file
