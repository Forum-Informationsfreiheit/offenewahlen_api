#!/bin/bash
python src/manage.py import_results 'data/test/nrw_2013_1_results.json' nrw13 --file_type json --mapping_file 'data/test/nrw_2013_mapping.json'
echo "NRW13 results imported."