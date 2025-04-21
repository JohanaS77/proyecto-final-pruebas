import pytest
import os
import datetime

if __name__ == "__main__":
    # Crear nombre de archivo para el reporte con fecha y hora
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"report_{timestamp}.html"
    
    # Ejecutar pytest con la opción para generar reporte HTML
    pytest.main(["-v", "--html=" + report_name, "--self-contained-html"])
    
    print(f"Reporte generado: {report_name}")