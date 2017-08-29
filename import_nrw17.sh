#!/bin/bash
echo "\n== IMPORT NRW17 =="
python src/manage.py import_results 'data/test/example_1.xml' nrw17 --file_type xml --mapping_file 'data/test/nrw_2017_mapping.json'
echo "NRW17 results imported."