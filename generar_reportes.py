"""Ejecuta unittest y genera evidencia HTML, JSON y cobertura real."""

from datetime import datetime, timezone, timedelta
from html import escape
import io
import json
import os
from pathlib import Path
import platform
import sys
import unittest

import coverage

ROOT = Path(__file__).resolve().parent


class ResultadoHTML(unittest.TextTestResult):
    """Registra los resultados que entrega unittest, sin simularlos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.casos = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.casos.append({'caso': test.id(), 'estado': 'PASÓ', 'detalle': ''})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.casos.append({'caso': test.id(), 'estado': 'FALLÓ',
                           'detalle': self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.casos.append({'caso': test.id(), 'estado': 'ERROR',
                           'detalle': self._exc_info_to_string(err, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.casos.append({'caso': test.id(), 'estado': 'OMITIDO', 'detalle': reason})


def main():
    os.chdir(ROOT)
    reportes = ROOT / 'reportes'
    reportes.mkdir(exist_ok=True)
    cov = coverage.Coverage(config_file=str(ROOT / '.coveragerc'))
    cov.start()
    suite = unittest.defaultTestLoader.discover('.', pattern='test.py')
    salida = io.StringIO()
    resultado = unittest.TextTestRunner(
        stream=salida, verbosity=2, resultclass=ResultadoHTML
    ).run(suite)
    cov.stop()
    cov.save()
    cov.html_report()
    cov.json_report(outfile=str(reportes / 'cobertura.json'))
    resumen = io.StringIO()
    cov.report(file=resumen)
    fecha = datetime.now(timezone(timedelta(hours=-5))).isoformat(timespec='seconds')
    datos = {'fecha_bogota': fecha, 'python': platform.python_version(),
             'coverage': coverage.__version__, 'ejecutadas': resultado.testsRun,
             'fallos': len(resultado.failures), 'errores': len(resultado.errors),
             'omitidas': len(resultado.skipped), 'correcto': resultado.wasSuccessful(),
             'casos': resultado.casos}
    (reportes / 'pruebas.json').write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding='utf-8')
    (reportes / 'pruebas.txt').write_text(salida.getvalue(), encoding='utf-8')
    (reportes / 'cobertura.txt').write_text(resumen.getvalue(), encoding='utf-8')
    filas = ''.join('<tr><td>' + escape(c['caso'].split('.')[-1]) + '</td><td>'
                    + escape(c['estado']) + '</td><td><pre>' + escape(c['detalle'])
                    + '</pre></td></tr>' for c in resultado.casos)
    html = f'''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laboratorio 04 - Ejecución de pruebas</title>
<style>body{{font:16px/1.6 system-ui;margin:40px auto;padding:0 24px;max-width:1000px;color:#173e56}}
h1{{line-height:1.2}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #b6c6cf;padding:10px;text-align:left}}
th{{background:#e4eef4}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}}.resumen{{background:#edf5f7;padding:20px}}</style>
<h1>Laboratorio 04 · Ejecución de pruebas</h1><p>Python {escape(datos['python'])} · unittest · {escape(fecha)} (Bogotá)</p>
<p class="resumen">Ejecutadas: <b>{resultado.testsRun}</b> · Fallos: <b>{len(resultado.failures)}</b> · Errores: <b>{len(resultado.errors)}</b> · Omitidas: <b>{len(resultado.skipped)}</b></p>
<p>CP1-CP4 son los casos base. Los casos extra amplían las entradas comprobadas.</p>
<table><thead><tr><th>Caso</th><th>Resultado</th><th>Detalle de fallo</th></tr></thead><tbody>{filas}</tbody></table>
<h2>Salida real de unittest</h2><pre>{escape(salida.getvalue())}</pre>
<h2>Resumen de cobertura</h2><pre>{escape(resumen.getvalue())}</pre>
<p><a href="cobertura/index.html">Abrir reporte detallado de Coverage.py</a></p></html>'''
    (reportes / 'pruebas.html').write_text(html, encoding='utf-8')
    print(salida.getvalue())
    print(resumen.getvalue())
    print('Reportes: reportes/pruebas.html y reportes/cobertura/index.html')
    return 0 if resultado.testsRun > 0 and resultado.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
