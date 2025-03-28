
<img width="1000" alt="Screenshot 2025-03-18 at 6 08 57 PM" src="https://github.com/user-attachments/assets/eeb55158-1a26-47cf-b6da-322d35dd44e1" />

## Introduction
The EEG Stimulus Package is a comprehensive tool designed to assist researchers and clinicians in administering and managing auditory stimuli during EEG (electroencephalogram) sessions. This software, built using Python and Streamlit, provides a user-friendly graphical interface that facilitates the seamless integration of stimulus protocols and patient data management. It is especially useful for experiments involving precise auditory stimulus timing, randomized trial administration, and detailed patient record-keeping.

In Winter 2025, we've also integrated modular Python scripts (e.g., `rodika_modularized.py` , `claassen_analysis.py`) that allow researchers to filter, artifact-remove, epoch, and analyze EEG recordings after administering stimuli. These additions let you run operations like inter-trial phase coherence (ITPC) for speech tracking or machine-learning classification for motor command-following, all within the same codebase. The Streamlit GUI (`gui_stimulus.py`) now triggers these analysis functions, enabling a seamless workflow from stimulus administration to data-driven insights, with no separate pipelines required.

Check out a video of our application here:
<video src="https://github.com/user-attachments/assets/fcf604e9-d5cf-4985-b3c2-1fb92a1c226c" width="300" />

## Features
### Graphical User Interface (GUI):
A web-based interface powered by Streamlit, allowing for easy interaction with the software without requiring deep technical knowledge.

### Stimulus Administration:

- **Randomized Trials:** Automatically randomizes and prepares trial sequences, including language-based stimuli, command prompts, and auditory beeps.  
- **Jittered Delay:** Introduces random delays between stimuli to reduce predictability and improve experiment robustness.  
- **Multiple Stimulus Types:** Supports language stimuli, right/left command prompts, and beep stimuli, with configurable playback options.

### Patient Data Management:

- **Patient/EEG ID Input:** Allows users to input and track patient IDs during stimulus administration.  
- **Trial Tracking:** Records detailed trial information, including the type of trial, start and end times, and duration, which are stored in a CSV format for easy access and analysis.  
- **Prevent Redundant Administration:** Automatically checks if a patient has already received the stimulus protocol on the current date to avoid redundancy.

### Search and Retrieval:

- **Search Administered Stimuli:** Users can search for and review stimuli that have been administered to patients on specific dates.  
- **View Stimuli Details:** Displays the specific stimuli administered to a patient, helping researchers track the protocol's progress and effectiveness.

### Notes Management:

- **Add Notes:** Enables users to append notes to patient records, ensuring that all observations and important details are documented.  
- **Retrieve Notes:** Allows for easy retrieval of previously added notes, providing a comprehensive overview of patient interactions and observations.

### Cross-Platform Support:
Compatible with *Windows/Linux/MacOS* operating systems.

## Installation for Audio Stimilus Administration
Please follow the steps below to download the depnedencies and files needed to deliver a randomized auditory stimulus to a patient. Read more about our auditory stimulus [here](https://github.com/EEG-project-capstone/brain-waves-2.0/blob/main/doc/EEG-TBI_AuditoryStimulusDetails.pdf).

### *Prerequisites*
This software requires the installation of:
* [Anaconda](https://docs.anaconda.com/anaconda/install/)/[Miniconda](https://docs.anaconda.com/miniconda/)
* Python
### *Setup Environment*
#### 1. Create CONDA env
```bash
conda create -n "eeg"
conda activate eeg
conda install pip
pip install -r requirements.txt
```

#### 2. Install mpv package (*for Windows*)
```bash
pip install mpv
```
Go to this [repo](https://github.com/jaseg/python-mpv), download `mpv.py` to /Script folder.    
To check where Script folder is, use command `conda env list`.    
Go to this [link](https://sourceforge.net/projects/mpv-player-windows/) to download dev package.
Choose the one with x84_64 if your computer is 64-bit. If 32 bit, choose the one with 32 bit.
After downloading, extract libmpv-2.dll (or a combination of mpv.exe + mpv.com + mpv-1.dll) to /Script folder. Refer to this [issue](https://github.com/jaseg/python-mpv/issues/60#issuecomment-352719773).    
Then run
```bash
pip install python-mpv
```
#### 3. Install ffmpeg (*for Windows or Mac if an error occurs*)
##### For Windows
Install [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) to current directory.    
Extract and rename to `ffmpeg`.    
Make sure to have these 2 files:    
`ffmpeg\bin\ffmpeg.exe`    
`ffmpeg\bin\ffprobe.exe`

##### For Mac
`brew install ffmpeg`.

#### 4. Install audio folder
Download the audio folder from this [link](https://drive.google.com/drive/folders/1VktnddvsY1kFihuCpRO4GKf7Z4wXVKIa) 
to the `data` folder. Make sure the folder name matches the `sentences_path` field in `config.yml`.    
If the `data/static/` is not already available, run `python auditory_stim/static_sound.py`
to create the static audio files. 

#### 5. Set File Upload Limit
```bash
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=400
```

## Usage
### Steps to Run Stimuli App
For a detailed step-by-step guide to setting up the repository to run analysis, please follow this [guide](https://github.com/EEG-project-capstone/brain-waves-2.0/blob/main/doc/Brain%20Waves%20Repository%20Step-by-Step%20Guide.pdf).

For a detailed step-by-step guide to using the Brain Wave Application (on Streamlit) to run analysis, please follow this [guide](https://github.com/EEG-project-capstone/brain-waves-2.0/blob/main/doc/Brain%20Waves%20Application%20Step-by-Step%20Guide.pdf).

### Data

This directory contains various datasets and analysis results related to patient studies. The files in this directory are ignored by Git and are structured as follows:

```
data/
├── edfs/
│   ├── [PatientID]_[Date].edf
├── images/
├── patient_df.csv
├── patient_history.csv
├── patient_notes.csv
├── patient_records.csv
├── patients/
│   └── [PatientName]_[Date].csv
└── results/
    ├── cmd/
    │   ├── [PatientID]_[Date]/
    │   │   ├── EEG_spatial_patterns.png
    │   │   ├── average_predicted_probability.png
    │   │   ├── cross_validation_performance.png
    │   │   ├── epochs_during_instructions.png
    │   │   ├── log.txt
    │   │   ├── permutation_results.png
    │   │   └── permutation_test_distribution.png
    └── lang_tracking/
        ├── [PatientID]/
        │   ├── ITPC_C3.png
        │   ├── ITPC_C4.png
        │   ├── ITPC_Cz.png
        │   ├── ITPC_F3.png
        │   ├── ITPC_F4.png
        │   ├── ITPC_F7.png
        │   ├── ITPC_F8.png
        │   ├── ITPC_FT10.png
        │   ├── ITPC_FT9.png
        │   ├── ITPC_Fp1.png
        │   ├── ITPC_Fp2.png
        │   ├── ITPC_Fpz.png
        │   ├── ITPC_Fz.png
        │   ├── ITPC_O1.png
        │   ├── ITPC_O2.png
        │   ├── ITPC_P3.png
        │   ├── ITPC_P4.png
        │   ├── ITPC_P7.png
        │   ├── ITPC_P8.png
        │   ├── ITPC_Pz.png
        │   ├── ITPC_T7.png
        │   ├── ITPC_T8.png
        │   └── avg_itpc_plot.png
```
### Directory Breakdown

#### `edfs/`

This folder contains EEG data files in `.edf` format, with filenames structured as `[PatientID]_[Date].edf`.

#### `images/`

Reserved for any images or visualizations related to the study.

#### `patients/`

Contains individual CSV files for each patient, storing their records, with filenames structured as `[PatientName]_[Date].csv`.

#### `results/`

Contains analyzed data for each patient, organized into two main subdirectories:

##### `cmd/`

Stores CMD analysis results for each patient in `[PatientID]_[Date]/` folders.

- `log.txt` contains analysis results such as AUC scores, and can also be used to check error logs.
- If you need to re-run the analysis, delete the corresponding `[PatientID]_[Date]` folder.

##### `lang_tracking/`

Stores language tracking analysis data per patient.

- Includes ITPC plots for different brain regions (`ITPC_C3.png`, `ITPC_F3.png`, etc.) and an averaged ITPC plot (`avg_itpc_plot.png`).

#### Notes
- Deleting a specific patient’s folder in `results/cmd/` allows for re-running the analysis.

## Contributing
- Nguyen Ha (Summer 2024)
- Khanh Ha (Summer 2024)
- Joobee Jung (Fall 2024)
- Trisha Prasant (Fall 2024)

## License
- The license under which the project is distributed.

## Contact
- Dr. Peter Schwab, MD
