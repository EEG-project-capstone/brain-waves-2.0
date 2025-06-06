import time
import os
import random
import yaml
import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
import sounddevice as sd
import numpy as np


class AuditoryStimulator:

    config: any

    lang_audio: list[any]
    lang_trials_ids: list[any]

    right_keep_audio: any
    right_stop_audio: any
    left_keep_audio: any
    left_stop_audio: any

    beep_audio: any 

    loved_one_file: any
    loved_one_gender: any
    loved_one_voice_audio: any
    control_voice_audio: any
     
    def __init__(self, config_file_path='config.yml'):
        """Initialize the auditory stimulator with configuration"""

        # Initialize attributes
        config_file_path = 'config.yml'
        with open(config_file_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.lang_audio = []
        self.lang_trials_ids = []

        self.right_keep_audio = None
        self.right_stop_audio = None
        self.left_keep_audio = None
        self.left_stop_audio = None

        self.beep_audio = None

        self.loved_one_file = None
        self.loved_one_gender = None
        self.loved_one_voice_audio = None
        self.control_voice_audio = None

        # import numpy as np
        # import sounddevice as sd

        # from pydub.utils import ratio_to_db

        # # Generate test tones
        # fs = 44100
        # tone1 = 0.5 * np.sin(2 * np.pi * 440 * np.arange(fs * 2) / fs)  # 2 sec tone
        # tone2 = 0.3 * np.sin(2 * np.pi * 880 * np.arange(fs * 2) / fs)  # Quieter tone

        # def adaptive_volume(audio_segment, threshold_db=-20):
        #     rms = audio_segment.rms
        #     if rms > threshold_db:
        #         return audio_segment - 6  # Reduce loud segments
        #     return audio_segment

        # instruction = adaptive_volume(tone1)
        # feedback = adaptive_volume(tone2)





    def generate_trials(self, num_of_each_trials):      
        # generate random set of trials
        trial_names = []

        # interate through each trial type
        for key in num_of_each_trials:
            # add trial names for for each trial type save gather audio data
            if num_of_each_trials[key] > 0:
                # prepare language stims
                if key == "lang":
                    self._generate_language_stimuli(num_of_each_trials[key])
                    for i in range(num_of_each_trials[key]):
                        trial_names.append(f"lang_{i}")
                # prepare right hand commands
                elif key == "rcmd":
                    self.right_keep_audio = AudioSegment.from_mp3(self.config['right_keep_path'])
                    self.right_stop_audio = AudioSegment.from_mp3(self.config['right_stop_path'])
                    for i in range(num_of_each_trials[key]):
                        trial_names.append(key)
                # prepare left hand commands
                elif key == "lcmd":
                    self.left_keep_audio = AudioSegment.from_mp3(self.config['left_keep_path'])
                    self.left_stop_audio = AudioSegment.from_mp3(self.config['left_stop_path'])
                    for i in range(num_of_each_trials[key]):
                        trial_names.append(key)
                # prepare beep
                elif key == "beep":
                    self.beep_audio = AudioSegment.from_mp3(self.config['beep_path'])
                    for i in range(num_of_each_trials[key]):
                        trial_names.append(key)
                elif key == "odd":
                    for i in range(num_of_each_trials[key]):
                        trial_names.append('oddball')
                elif key == "loved":
                    # path to loved ones voice recording
                    temp_path = os.path.join("audio_data/static/", self.loved_one_file.name)
                    # add loved ones voice recording 
                    self.loved_one_voice_audio = AudioSegment.from_wav(temp_path)
                    # add a gendered control voice recording 
                    if self.loved_one_gender == 'Male':
                        self.control_voice_audio = AudioSegment.from_wav(self.config['male_control_path'])
                        print("added male control")
                    elif self.loved_one_gender == 'Female':
                        # self.control_voice_audio = AudioSegment.from_wav(self.config['female_control_path'])
                        self.control_voice_audio = AudioSegment.from_wav('audio_data/static/ControlStatement_female.wav')
                        print("added female control")
                    else:
                        print("no control audio was added")
                    # add loved ones or control voice recording
                    trial_names += ['control'] * num_of_each_trials[key]
                    trial_names += ['loved_one'] * num_of_each_trials[key]

        # shuffle the trials to be random
        random.shuffle(trial_names)

        trial_names = ['sync'] + trial_names

        return trial_names
    
    def play_stimuli(self, trial):

        # add sentences list for lang and oddball orders
        sentences = []

        # administered correct 
        if trial == "sync":
            print("abouit to play sync")
            start_time, end_time = self._administer_sync()
        elif trial[:4] == "lang":
            start_time, end_time, sentences = self._administer_lang(trial)
        elif trial == "rcmd":
            start_time, end_time = self._administer_right_cmd()
        elif trial == "lcmd":
            start_time, end_time = self._administer_left_cmd()
        elif trial == "beep":
            start_time, end_time = self._administer_beep()
        elif trial == "oddball":
            start_time, end_time, sentences = self._administer_oddball()
        elif trial == "control":          
            start_time, end_time = self._administer_control()
        elif trial == "loved_one": 
            start_time, end_time = self._administer_loved_one()

        print(f"Successfully administered {trial}")

        time.sleep(random.uniform(1.2, 2.2))

        return start_time, end_time, sentences
    
    def _generate_language_stimuli(self, num_of_lang_trials):
        gen_bar = st.progress(0, text="0")
        for i in range(num_of_lang_trials):
            self._random_lang_stim()
            percent = int(i/num_of_lang_trials*100)
            gen_bar.progress(percent, text=f"{percent}%")
        gen_bar.progress(100, text=f"Done")

    def _random_lang_stim(self, num_sentence=12):

        sentence_files = os.listdir(self.config['sentences_path'])

        # Filter out non-wav files
        wav_files = [file for file in sentence_files if file.endswith('.wav')]

        # Ensure num_sentence does not exceed available wav files
        if num_sentence > len(wav_files):
            raise ValueError(f"Requested {num_sentence} files, but only {len(wav_files)} available.")

        selected_ids = set()  # To keep track of already selected IDs
        combined = AudioSegment.empty()
        sample_ids = []

        while len(sample_ids) < num_sentence:
            # Randomly choose an ID
            id = random.choice(range(len(wav_files)))
            if id in selected_ids:
                continue  # Skip if this ID was already selected
            file = os.path.join(self.config['sentences_path'], f'lang{id}.wav')
            if os.path.exists(file):
                # If the file exists, add its ID to sample_ids and selected_ids
                sample_ids.append(id)
                selected_ids.add(id)

                # Read and concatenate the audio
                audio = AudioSegment.from_wav(file)
                combined += audio
            else:
                # raise ValueError(f"Requested lang{id}.wav file, but lang{id}.wav does not exist.")
                continue
        # save audio segement
        self.lang_audio.append(combined)
        # save sample IDs
        self.lang_trials_ids.append(sample_ids)

    # def _list_output_devices(self):
    #     """List all available audio output devices"""
    #     devices = sd.query_devices()
    #     output_devices = []
    #     for i, dev in enumerate(devices):
    #         if dev['max_output_channels'] > 0:
    #             output_devices.append((i, dev['name']))
    #     return output_devices

    def _administer_lang(self, trial):

        sentences = []
        n = int(trial[5:])
        start_time = time.time()

        # Debug info
        print(f"Trial: {trial}, index: {n}")
        # print(f"lang_trials_ids length: {len(self.lang_trials_ids)}")
        # print(f"lang_audio length: {len(self.lang_audio)}")
        
        # Safely access data
        if 0 <= n < len(self.lang_trials_ids):
            sentences = self.lang_trials_ids[n]
            print(f"Playing the following lang_trials_ids: {sentences}")
    

        if 0 <= n < len(self.lang_audio):
            print("Playing audio")
            play(self.lang_audio[n])

        # print("Audio playback complete")

        end_time = time.time()

        return start_time, end_time, sentences

    def _administer_right_cmd(self):
        start_time = time.time()
        for _ in range(8):
            play(self.right_keep_audio)
            time.sleep(10)
            play(self.right_stop_audio)
            time.sleep(10)
        end_time = time.time()
        return start_time, end_time

    def _administer_left_cmd(self):
        start_time = time.time()
        for _ in range(8):
            play(self.left_keep_audio)
            time.sleep(10)
            play(self.left_stop_audio)
            time.sleep(10)
        end_time = time.time()
        return start_time, end_time

    def _administer_beep(self):
        start_time = time.time()
        play(self.beep_audio)
        time.sleep(10)
        end_time = time.time()
        return start_time, end_time

    def _administer_oddball(self):

        sentences = []
        start_time = time.time()

        # play 5 standard tones
        for _ in range(5):
            audio_segment = Sine(1000).to_audio_segment(duration=100)
            samples = audio_segment.get_array_of_samples()
            sd.play(samples, audio_segment.frame_rate, device=0)
            sd.wait()
            sentences.append('standard')
            
            # sleep for 1 seconds
            time.sleep(1)

        # play 20 standard or rare tones 
        for i in range(20):
            # play rare tone with 20% probability
            if random.random() < 0.2:
                audio_segment = Sine(2000).to_audio_segment(duration=100)
                samples = audio_segment.get_array_of_samples()
                sd.play(samples, audio_segment.frame_rate, device=0)
                sd.wait()
                sentences.append('rare')
            # else play standard tone 
            else:
                audio_segment = Sine(1000).to_audio_segment(duration=100)
                samples = audio_segment.get_array_of_samples()
                sd.play(samples, audio_segment.frame_rate, device=0)
                sd.wait()
                sentences.append('standard') 
            # sleep for 1 seconds
            time.sleep(1)
 
                    
        end_time = time.time()

        # print out sentences: standard or rare
        print(f"Playing the following frequencies: {sentences}")

        return start_time, end_time, sentences

    def _administer_control(self):
        start_time = time.time()
        print(f"Playing control recording")
        play(self.control_voice_audio)
        end_time = time.time()
        time.sleep(5)
        return start_time, end_time

    def _administer_loved_one(self):
        start_time = time.time()
        print(f"Playing loved one recording")
        play(self.loved_one_voice_audio)
        end_time = time.time()
        time.sleep(5)
        return start_time, end_time
    
    def _administer_sync(self):
        start_time = time.time()
        print(f"Playing sync")

        # # Generate square wave (50% duty cycle)
        # square_wave = np.array()
        # for _ in range(10):
        #     square_wave.append(1)

        # # Play once
        # sd.play(square_wave, 44100)
        # sd.wait()  # Wait until playback finishes

        # Configuration
        FREQ = 440    # Frequency (Hz) - A4 musical note
        DURATION = 1  # Seconds
        VOLUME = 0.5  # 0.0 (silent) to 1.0 (max)

        # Generate square wave (50% duty cycle)
        t = np.linspace(0, DURATION, int(44100 * DURATION), False)
        square_wave = VOLUME * np.sign(np.sin(2 * np.pi * FREQ * t))

        # Play once
        sd.play(square_wave, 44100)
        sd.wait()  # Wait until playback finishes

        end_time = time.time()
        time.sleep(5)
        return start_time, end_time