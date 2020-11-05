import csv
import os
from pydub import AudioSegment, silence
from pydub.playback import play

# We have three conditions: High Frequency (HF), Low Frequency (LF), and Non-Words (NW).
# All words for each condition are stored in one .wav file.
# Your task is to:
#       split the words on the silence
#       make sure they all have the same loudness
#       save them in a folder corresponding to their condition (folder names: HF, LF, NW)

path_to_repository = "C:\\Users\\sopsla\\Desktop\\session2b-sound"  # add your own path here!

# This little piece of code is here to help you.
# It reads a text file with information about the stimuli you are going to split (names & condition)
# It returns a dictionary named 'stimuli' with condition as key, and the word itself as value.
# Use this dictionary to name the files you have to save.
stimuli_info = open(os.path.join(path_to_repository, "lexdec_stimuli.txt"))
stimuli_reader = csv.reader(stimuli_info, delimiter=',')
headers = next(stimuli_reader, None)

stimuli = {}

# Create the dictionary
for stimulus in stimuli_reader:
    if stimulus[2] not in stimuli.keys():
        stimuli[stimulus[2]] = list()
    stimuli[stimulus[2]].append(stimulus[3])

# Put them in alphabetical order
for condition, words in stimuli.items():
    sort = sorted(words)
    stimuli[condition] = sort

# change the non-word condition name
stimuli["NW"] = stimuli.pop("none")

# Now you have the stimulus names. (take a look at what it looks like using "print")
# YOUR CODE HERE.

# Where are the stimuli?
folder = os.path.join(path_to_repository, "raw")

# How loud do you want your stimuli to be?
target_dBFS = -10

# Where do you want to save your files?
edited_folder = "C:\\Users\\sopsla\\Desktop\\session2b-sound\\edited"  # your path here!
if not os.path.isdir(edited_folder):  # this makes sure that the folder is not created if it's already there
    os.mkdir(edited_folder)

# Loop over the audio files
for file in os.listdir(folder):
    condition_for_dict = file[0:2]  # HF, LF, NW
    folder_for_saving = os.path.join(edited_folder, condition_for_dict)

    if not os.path.isdir(folder_for_saving):
        os.mkdir(folder_for_saving)

    # Open the sound file
    sound = AudioSegment.from_wav(os.path.join(folder, file))
    print(sound.dBFS)

    # Normalize the volume for the whole sequence? No? Why not?
    # Split for silence (returns a list)
    words = silence.split_on_silence(sound, min_silence_len=199, silence_thresh=-50, keep_silence=False)

    # Did it work? Check the length or play the words
    print(len(words))

    for word in words:

        # Adjust the volume
        change_in_dBFS = target_dBFS - word.dBFS
        normalized_word = word.apply_gain(change_in_dBFS)

        # Did it work?
        print("orig", word.dBFS, "norm", normalized_word.dBFS)

        # OK! Use the index of the word to get the corresponding name
        filename = stimuli[condition_for_dict][words.index(word)] + ".wav"

        # Save the file
        normalized_word.export(os.path.join(folder_for_saving, filename), format="wav")

    # That's all!
