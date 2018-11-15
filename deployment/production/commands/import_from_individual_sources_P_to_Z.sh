#!/usr/bin/env bash

SECONDS=0
DJANGO_SETTINGS_MODULE=berlinbuehnen.settings.production
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
DJANGO_PATH="${PROJECT_PATH}/project/berlinbuehnen"
#PROJECT_PATH="${HOME}/git/bitbucket/berlinbuehnen"
#DJANGO_PATH="${PROJECT_PATH}"
mkdir -p "${PROJECT_PATH}/logs"
CRON_LOG_FILE="${PROJECT_PATH}/logs/import_from_individual_sources_P_to_Z.log"

script_errors=0

# Use the null command (:) redirect (> filename) trick (:>), as this will truncate to zero or create the named file.
:> "${CRON_LOG_FILE}"

cd "${PROJECT_PATH}" || exit
# shellcheck source=../../../venv/bin/activate
source venv/bin/activate

function run_django_command {
    echo "$2"
    date
    DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE}" \
    PROJECT_PATH="${PROJECT_PATH}" \
        python "${DJANGO_PATH}/manage.py" "$1" --traceback --verbosity=2
    django_command_exit_code=$?
    echo "------------"
    return $django_command_exit_code
}

COMMANDS=(
#    "import_from_NON_EXISTING_SOURCE:Importing from Non-existing Source (should trigger error)"
#    "import_from_berliner_ensemble:Importing from Berliner Ensemble (New)"
#    "import_from_berliner_philharmonie:Importing from Berliner Philharmonie"
#    "import_from_boulezsaal:Importing from Pierre Boulez Saal (New)"
#    "import_from_culturebase_dob:Importing from Deutsche Oper Berlin"
#    "import_from_culturebase_radialsystem:Importing from RADIALSYSTEM V"
#    "import_from_deutsches_theater:Importing from Deutsches Theater"
#    "import_from_hau:Importing from HAU"
#    "import_from_komische_oper_berlin:Importing from Komische Oper Berlin"
#    "import_from_konzerthaus_new:Importing from Konzerthaus (New)"
#    "import_from_maxim_gorki_theater:Importing from Maxim Gorki Theater (New)"
    "import_from_parkaue:Importing from Theater an der Parkaue"
    "import_from_schaubuehne:Importing from Schaubuehne"
    "import_from_schlosspark_theater_new:Importing from Schlosspark Theater (New)"
    "import_from_sophiensaele:Importing from Sophiensaele"
    "import_from_staatsballet_berlin:Importing from Staatsballet Berlin"
    "import_from_staatsoper_berlin:Importing from Staatsoper Berlin (New)"
    "import_from_volksbuehne:Importing from Volksbuehne"
    "import_from_volksbuehne:Importing from Volksbühne (New)"
    "import_from_wuehlmaeuse:Importing from Wuehlmaeuse"
)


for command_colon_title in "${COMMANDS[@]}"; do
    command="${command_colon_title%%:*}"
    title="${command_colon_title##*:}"
    run_django_command "${command}" "${title}" >> "${CRON_LOG_FILE}" 2>&1
    function_exit_code=$?
    if [[ $function_exit_code -ne 0 ]]; then
        echo "<<<<<<<<<<<<" >> "${CRON_LOG_FILE}" 2>&1
        echo "Function exit code is non-zero ($function_exit_code) for command $command" >> "${CRON_LOG_FILE}" 2>&1
        script_errors=$((script_errors + 1))
        echo ">>>>>>>>>>>>" >> "${CRON_LOG_FILE}" 2>&1
    else
        echo "No error running command $command" >> "${CRON_LOG_FILE}" 2>&1
    fi
    echo "============" >> "${CRON_LOG_FILE}" 2>&1
done

deactivate
cd - || exit

echo "Finished." >> "${CRON_LOG_FILE}"
duration=${SECONDS}
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed." >> "${CRON_LOG_FILE}"

if [[ $script_errors -ne 0 ]]; then
    echo "<<<<<<<<<<<<" >> "${CRON_LOG_FILE}" 2>&1
    echo "Script encountered $script_errors errors during execution" >> "${CRON_LOG_FILE}" 2>&1
    echo ">>>>>>>>>>>>" >> "${CRON_LOG_FILE}" 2>&1
fi

exit $script_errors