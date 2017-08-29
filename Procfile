web: gunicorn --pythonpath src offenewahlen_nrw17.wsgi --timeout 60 --log-level debug --log-file -
reset: sh reset_db.sh
migrate: sh migrate_db.sh
drop: sh drop_db.sh
import_data: sh import_data.sh
import_base: sh import_base.sh
import_nrw13: sh import_nrw13.sh
import_nrw17: sh import_nrw17.sh
