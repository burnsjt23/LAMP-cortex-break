green=`tput setaf 2`
cyan=`tput setaf 6`
reset=`tput sgr0`
find tests -name '*tests.py' -print0 |
    while IFS= read -r -d '' line; do
        echo "${line}"
        if [[ $line = "tests/primary_feature_tests.py" ]]
        then
            echo "${green} Running tests for ${line} ${reset}"
            coverage run -m unittest "$line"
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/primary/significant_locations.py
            coverage report -m cortex/primary/trips.py
            coverage report -m cortex/primary/screen_active.py
            coverage report -m cortex/primary/acc_jerk.py
        elif [[ $line = "tests/secondary_feature_tests.py" ]]
        then
            echo "${green} Running tests for ${line} ${reset}"
            coverage run -m unittest "$line"
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/nearby_device_count.py
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/data_quality.py
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/step_count.py
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/call_duration.py
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/call_number.py
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/secondary/call_degree.py
        elif [[ $line = "tests/util_tests.py" ]]
        then
            echo "${green} Running tests for ${line} ${reset}"
            coverage run -m unittest "$line"
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/utils/misc_functions.py
        elif [[ $line = "tests/neocortex_tests.py" ]]
        then
            echo "${green} Running tests for ${line} ${reset}"
            coverage run -m unittest "$line"
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m Neocortex/raw/steps.py
            coverage report -m Neocortex/primary/screen_active.py
            coverage report -m Neocortex/primary/significant_locations.py
            coverage report -m Neocortex/secondary/step_count.py
            coverage report -m Neocortex/secondary/hometime.py
            coverage report -m Neocortex/secondary/entropy.py
        else
            echo "TODO: add other tests here"
            # coverage report
        fi
    done
echo "${reset}"

