"""Rebuild the corrected report without replacing an open original."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    runpy.run_path(str(here / 'revise_diagrams.py'), run_name='__main__')
    runpy.run_path(str(here / 'revise_report.py'), run_name='__main__')
