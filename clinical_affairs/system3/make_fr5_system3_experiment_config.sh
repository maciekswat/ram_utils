#!/usr/bin/env bash
# NOTE:
# THIS IS THE CONFIG FILE GENERATOR FOR PS4_FR5 AND FOR FR5.

read -p "SUBJECT: " subject
read -p "EXPERIMENT (PS4_FR5 | FR5): " experiment
read -p "ELECTRODE CONFIG FILE : " config_file
if [ "${experiment}" = "PS4_FR5" ]
then
    read -p "ANODE1:   " anode1
    read -p "CATHODE1: " cathode1
    read -p "Minimum amplitude 1(mA): " min_amplitude_1
    read -p "Maximum amplitude 1(mA): " max_amplitude_1

    read -p "ANODE2:   " anode2
    read -p "CATHODE2: " cathode2
    read -p "Minimum amplitude 2(mA): " min_amplitude_2
    read -p "Maximum amplitude 2(mA): " max_amplitude_2
    target_amplitude=${max_amplitude_1}
elif [ "${experiment}" = "FR5" ]
then
    read -p "STIM ANODE: " anode1
    read -p "STIM CATHODE: " cathode1
    read -p "ANODE2: " anode2
    read -p "CATHODE2: " cathode2
    read -p "Target Amplitude (mA): " target_amplitude
    min_amplitude_1=0.1
    min_amplitude_2=0.1

    max_amplitude_1=${target_amplitude}
    max_amplitude_1=${target_amplitude}

else
    echo "Unknown experiment type"
    exit 1
fi
#anode1=LTG29
#cathode1=LTG30
#anode2=LTG30
#cathode2=LTG31
#target_amplitude=1.9
#min_amplitude=0.1
#max_amplitude=1.9

today=$(date +%m_%d_%y)

pulse_frequency=200
stim_pair_1=${anode1}-${cathode1}
stim_pair_2=${anode2}-${cathode2}

if [ -z "${config_file}" ]
then

config_dir="/scratch/system3_configs/${experiment}_biomarkers/${subject}_${experiment}_${anode1}_${cathode1}_${max_amplitude_1}mA_${anode2}_${cathode2}_${max_amplitude_2}mA_${today}/electrode_configs"
python ../../system_3_utils/odin_config_tool_generator.py --subject=${subject}\
 --contacts-json-output-dir=${config_dir}\
 --stim-channels ${stim_pair_1} ${stim_pair_2}

config_file=${config_dir}/contacts${subject}.csv
fi

workspace_dir="/scratch/system3_configs/${experiment}_biomarkers/${subject}_${experiment}_${anode1}_${cathode1}_${max_amplitude_1}mA_${anode2}_${cathode2}_${max_amplitude_2}mA_${today}"


python ../../tests/fr5_biomarker/system3/fr5_util_system_3.py\
 --subject=${subject}\
 --workspace-dir=${workspace_dir}\
 --experiment=${experiment}\
 --electrode-config-file=${config_file}\
 --anodes ${anode1} ${anode2}\
 --cathodes ${cathode1} ${cathode2}\
 --pulse-frequency=${pulse_frequency}\
 --target-amplitude=${target_amplitude}\
 --min-amplitudes ${min_amplitude_1} ${min_amplitude_2}\
 --max-amplitudes ${max_amplitude_1} ${max_amplitude_2} "${@:1}"
