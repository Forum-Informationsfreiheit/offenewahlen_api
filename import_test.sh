#!/bin/bash
echo "\n== IMPORT TEST =="
python src/manage.py import_results 'src/viz/tests/data/example_01.json' 'src/viz/tests/data/example_config.json'
echo "Test results imported."