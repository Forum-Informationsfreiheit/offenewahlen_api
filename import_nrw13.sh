#!/bin/bash
echo "\n== IMPORT NRW13 =="
python src/manage.py import_results 'data/results/nrw_2013_1_results.json' 'data/results/nrw13_config.json'
echo "NRW13 results imported."