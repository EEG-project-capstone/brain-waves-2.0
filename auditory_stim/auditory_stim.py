import time
import os
import random
import pandas as pd
from gtts import gTTS
import pyttsx3
from playsound import playsound
import yaml
import time
import streamlit as st
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub import AudioSegment
config_file_path = 'config.yml'  # Replace with the actual path to your config file

with open(config_file_path, 'r') as file:
    config = yaml.safe_load(file)

if config['os'].lower() == 'windows':
    import winsound
    import mpv

    player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)

def jittered_delay():
    time.sleep(random.uniform(1.2, 2.2))

def play_mp3(mp3_path, verbose=True):
    if verbose:
        print(f"Playing {mp3_path}...")
    if config['os'].lower() == 'windows':
        player.play(mp3_path)
        player.wait_for_playback()
    elif config['os'].lower() == 'streamlit':
        st.audio(mp3_path, format="audio/mpeg", autoplay=True)
    else:
        playsound(mp3_path)

# Event handler for when the playback position changes
if config['os'].lower() == 'windows':
    @player.property_observer('time-pos')
    def on_time_pos_change(_name, value):
        """Print video start and end times"""
        if value == 0 or value is None:
            start_time = time.time()
            print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

# def remove_silence(input_path, output_path, silence_thresh=-40, min_silence_len=500, padding=55):
#     # Load the audio file
#     audio = AudioSegment.from_mp3(input_path)
    
#     # Detect non-silent parts
#     nonsilent_parts = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
#     # Add padding around non-silent parts and concatenate them
#     segments = []
#     for start, end in nonsilent_parts:
#         start = max(0, start - padding)
#         end = min(len(audio), end + padding)
#         segments.append(audio[start:end])
    
#     # Combine all non-silent segments
#     combined = AudioSegment.empty()
#     for segment in segments:
#         combined += segment
    
#     # Export the processed audio
#     combined.export(output_path, format="mp3")

# def speed_up_audio(input_path, output_path, speed_factor=1.5):
#     audio = AudioSegment.from_mp3(input_path)
#     audio = audio.speedup(playback_speed=speed_factor)
#     audio.export(output_path, format="mp3")

# def gen_lang_stim(output_file_path, num_sentence=12):
#     sentence_list = ['cold homes need heat', 'black dog bit thieves', 'smart guys fix things', 'red cat ate rats',
#     'fast car hit walls', 'sweet boys kiss girls', 'nice dad held sons', 'good minds save lives', 'dry fur rubs skin',
#     'great goat climbs hills', 'hot tea burns tongues', 'wise teen read books', 'poor men want work', 'clear words make sense',
#     'slow wolf stole eggs', 'brave votes help towns', 'mad wife broke plates', 'fat kid likes food', 'big chimps throw fruits',
#     'young fans cheer stars', 'loud sound hurts ears', 'sharp knife cuts ropes', 'hard rocks smash heads', 'fine chefs cook meals',
#     'bright queens wear crowns', 'sick tramp drank wine', 'ill trees lost leafs', 'thick smoke kills bees', 'bored mum did stuff',
#     'dark lord threw spells', 'rich counts own lands', 'long walks strain legs', 'grey ship fires bombs', 'large planes cross clouds',
#     'small boat fought waves', 'old king loves deer', 'kind host gave beers', 'cool bands play songs', 'fun jokes please crowds',
#     'pure gas lights lamps', 'skilled smiths craft steel', 'new staff broke rules', 'strict law had flaws', 'weak birds built nests',
#     'green bug seeks holes', 'tall slaves pour tea', 'bold cop beats crime', 'brown bears feed cubs', 'cute pug felt pain',
#     'tough scene shows blood', 'tired aunt bakes cakes', 'warm rain melt snow', 'flat feet cause aches', 'starved hounds chase trucks',
#     'huge spoon brought soup', 'strong wind shuts doors', 'odd clown sang tales', 'best friends end stress', 'short dwarfs forge swords',
#     'white shark scares fish', 'thin guards swipe cards', 'blue pen leaks ink', 'high heels squeeze toes', 'blunt axe chops wood',
#     'worn toys wound hands', 'quick fox caught hens', 'grand branch blocks streets', 'deep rock hid gold', 'wet dirt soil socks',
#     'pink squid sinks rafts', 'vast space lacks air', 'slick crooks steal rings']

#     # Randomly select num_sentence sentences for 1 trial
#     sample_ids = random.sample(range(len(sentence_list)), num_sentence)
#     selected_sentences = [sentence_list[i] for i in sample_ids]
#     joined_sentences = ' '.join(selected_sentences)

#     if config['tts_package'] == 'gtts':
#         tts = gTTS(text=joined_sentences, lang="en")
#         tts.save(output_file_path)   
#         remove_silence(output_file_path,output_file_path)
#     elif config['tts_package'] == 'pyttsx3':
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 165)
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[1].id) 
#         engine.save_to_file(joined_sentences, output_file_path)
#         engine.runAndWait()    

#     return sample_ids

def random_lang_stim(output_path, num_sentence=12):

    sentence_files = os.listdir(config['sentences_path'])

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

        file = os.path.join(config['sentences_path'], f'lang{id}.wav')

        if os.path.exists(file):
            # If the file exists, add its ID to sample_ids and selected_ids
            sample_ids.append(id)
            selected_ids.add(id)

            # Read and concatenate the audio
            audio = AudioSegment.from_wav(file)
            combined += audio

    # Export the processed audio
    combined.export(output_path, format="mp3")
    
    return sample_ids

def play_lang_stim(output_path):
    start_time = time.time()
    play_mp3(output_path)
    end_time = time.time()
    return start_time, end_time

def right_cmd_stim():
    start_time = time.time()
    for _ in range(8):
        play_mp3(config['right_keep_path'])
        time.sleep(10)

        play_mp3(config['right_stop_path'])
        time.sleep(10)
    end_time = time.time()
    return start_time, end_time

def left_cmd_stim():
    start_time = time.time()
    for _ in range(8):
        play_mp3(config['left_keep_path'])
        time.sleep(10)

        play_mp3(config['left_stop_path'])
        time.sleep(10)
    end_time = time.time()
    return start_time, end_time

def administer_beep():

    if config['os'].lower() == 'windows':
        start_time = time.time()
        time.sleep(10)
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 10000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        time.sleep(10)
        end_time = time.time()

    else:
        start_time = time.time()
        time.sleep(10)
        play_mp3(config['beep_path'])
        end_time = time.time()
        time.sleep(10)
        end_time = time.time()
        # Break until 45secs

    return start_time, end_time

def randomize_trials(language_stim=72, right_cmd_stim=3, left_cmd_stim=3, beep_stim=6):
    trial_types = []
    num_trials = {
        "lang": language_stim,
        "rcmd": right_cmd_stim,
        "lcmd": left_cmd_stim,
        "beep": beep_stim
    }
    for key in num_trials:
        for i in range(num_trials[key]):
            if key == "lang":
                trial = f"lang_{i}"
            else:
                trial = key
            trial_types.append(trial)

    random.shuffle(trial_types)
    return trial_types

def generate_stimuli(trial_types):
    gen_bar = st.progress(0, text="0")
    n = len(trial_types)
    lang_trials_ids = []
    for i in range(n):
        trial = trial_types[i]
        if trial[:4] == "lang":
            output_path = os.path.join(config['stimuli_dir'], f"{trial}.mp3")
            sample_ids = random_lang_stim(output_path)                       # Last edit 08/25
            percent = int(i/n*100)
            gen_bar.progress(percent, text=f"{percent}%")
            lang_trials_ids.append(sample_ids)
            print(f"{i}: {output_path}")
        else:
            lang_trials_ids.append([])
    gen_bar.progress(100, text=f"Done")
    return lang_trials_ids

def play_stimuli(trial):
    if trial[:4] == "lang":
        output_path = os.path.join(config['stimuli_dir'], f"{trial}.mp3")
        start_time, end_time = play_lang_stim(output_path)
        jittered_delay()
    elif trial == "rcmd":
        start_time, end_time = right_cmd_stim()
        jittered_delay()
    elif trial == "lcmd":
        start_time, end_time = left_cmd_stim()
        jittered_delay()
    else:
        start_time, end_time = administer_beep()
        jittered_delay()
    return start_time, end_time
