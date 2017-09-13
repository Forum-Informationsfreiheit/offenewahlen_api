#!/bin/bash
echo "\n== IMPORT NRW17 =="
python src/manage.py import_results 'data/test/example_01.json' 'data/test/example_config.json'
echo "NRW17 results imported."