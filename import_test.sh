#!/bin/bash
echo "\n== IMPORT TEST =="
python src/manage.py import_results 'src/austria/tests/data/example_01.json' 'src/austria/tests/data/example_config.json'
echo "Test results imported."
