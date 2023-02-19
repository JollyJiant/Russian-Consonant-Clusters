import re
import numpy as np
import matplotlib.pyplot as plt

sig_fig = 10
russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
file = '1grams-3.txt'
total_freq = 0

#   Report total number of unique clusters and display them (in alph. Order)
#   Report the frequency of the consonant cluster ONLY at the word-initial position
#   Categorize each cluster into groups and report how many clusters are in each group:
#       * 2 letter
#       * 3 letter
#       * 4 letter

# WORD-INITIAL CLUSTER DICTIONARY
word_initial_clusters_dict = {}

# UNIQUE CLUSTER DICTIONARY
unique_clusters_dict = {}

# CLUSTER LENGTH DICTIONARIES
two_cluster_dict = {}
three_cluster_dict = {}
four_cluster_dict = {}
more_cluster_dict = {}

# ENTRIES THAT HAVE HYPHENS IN THEM
hyphenated_entries_dict = {}

# (all dictionaries mapped by token:frequency)
def get_key_val(line):
    freq = int(line.split()[0]) #val
    # characters in the entry are normalized to lower case
    token = line.split()[1].lower() #key
    return token, freq

# check if a token has any numbers in it
def has_digit(token):
    return any(char.isdigit() for char in token)

def has_invalid_character(token):
    return any(char not in russian_alphabet for char in token)

def has_hyphen(token):
    return any(char == '-' for char in token)

print("Processing the frequency list...")

with open(file) as freq_list:
    for line in freq_list:

        # get the entry's frequency and token
        token, freq = get_key_val(line)

        # separate any tokens with hyphens into their own group for manual analysis
        if(has_hyphen(token)):
            if token in hyphenated_entries_dict: hyphenated_entries_dict[token] += freq
            else: hyphenated_entries_dict[token] = freq
            continue

        # WORD PROCESSING:
        #   ignore entries that have digits
        #   subtract brackets
        #   ignore entries that have non-modern-russian characters
        #   TODO: ignore entries that are abbreviations

        # if the token contains any digits, move to the next token in the frequenct list
        if(has_digit(token)): continue

        # remove brackets from the token
        token = re.sub(r'[\[\]<>]', '', token)

        # if the token contains any non-modern-russian characters, move to the next token in the frequenct list
        if(has_invalid_character(token)): continue

        # TODO: scispacy AbbreviationDetector()

        # working with a valid token: update the total frequency
        total_freq += freq

        # currently: splits the token on vowels
        filtered_token = re.split(r'а|е|ё|и|о|у|ы|э|ю|я', token)

        # get the consonant clusters from the current split (filtered) token
        token_clusters = list(filter(lambda x: len(x)>1, filtered_token))

        # if there are any clusters
        if len(token_clusters) > 0:
            # add word-initial cluster (if exists) to the word-initial cluster dictionary
            if filtered_token[0] == token_clusters[0]:
                if token_clusters[0] in word_initial_clusters_dict: word_initial_clusters_dict[token_clusters[0]] += freq
                else: word_initial_clusters_dict[token_clusters[0]] = freq
            
            # go through each cluster in the list and
            #   1. add it to the unique dictionary
            #   2. check its length and add it to its corresponding cluster length dictionaries
            for cluster in token_clusters:
                if cluster in unique_clusters_dict: unique_clusters_dict[cluster] += freq
                else: unique_clusters_dict[cluster] = freq
                
                cluster_length = len(cluster)
                if cluster_length == 2:
                    if cluster in two_cluster_dict: two_cluster_dict[cluster] += freq
                    else: two_cluster_dict[cluster] = freq
                elif cluster_length == 3:
                    if cluster in three_cluster_dict: three_cluster_dict[cluster] += freq
                    else: three_cluster_dict[cluster] = freq
                elif cluster_length == 4:
                    if cluster in four_cluster_dict: four_cluster_dict[cluster] += freq
                    else: four_cluster_dict[cluster] = freq
                else:
                    if cluster in more_cluster_dict: more_cluster_dict[cluster] += freq
                    else: more_cluster_dict[cluster] = freq

print("Writing results to files...")

# write the hyphenated_entries dictionary to a file
hyphenated_file = open('output_files/hyphenated_entries.txt', 'w')
items = hyphenated_entries_dict.items()
for item in items:
    print(item[1], item[0], sep='\t', file=hyphenated_file)

# write the word_initial_clusters dictionary to a file
sorted_word_initial_clusters_list = sorted(word_initial_clusters_dict.keys())
word_initial_clusters_dict_freq = sum(word_initial_clusters_dict.values())
word_initial_clusters = open('output_files/word_initial_clusters.txt', 'w')
for cluster in sorted_word_initial_clusters_list:
    relative_freq = word_initial_clusters_dict[cluster]/word_initial_clusters_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), word_initial_clusters_dict[cluster], sep='\t\t', file=word_initial_clusters)

# write the unique_clusters dictionary to a file
sorted_unique_clusters_list = sorted(unique_clusters_dict.keys())
unique_clusters_dict_freq = sum(unique_clusters_dict.values())
unique_clusters = open('output_files/unique_clusters.txt', 'w')
for cluster in sorted_unique_clusters_list:
    relative_freq = unique_clusters_dict[cluster]/unique_clusters_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), unique_clusters_dict[cluster], sep='\t\t', file=unique_clusters)

# write the two_cluster dictionary to a file
sorted_length_two_cluster_list = sorted(two_cluster_dict.keys())
two_cluster_dict_freq = sum(two_cluster_dict.values())
length_two_clusters = open('output_files/length_two_clusters.txt', 'w')
for cluster in sorted_length_two_cluster_list:
    relative_freq = two_cluster_dict[cluster]/two_cluster_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), two_cluster_dict[cluster], sep='\t\t', file=length_two_clusters)

# write the three_cluster dictionary to a file
sorted_length_three_cluster_list = sorted(three_cluster_dict.keys())
three_cluster_dict_freq = sum(three_cluster_dict.values())
length_three_clusters = open('output_files/length_three_clusters.txt', 'w')
for cluster in sorted_length_three_cluster_list:
    relative_freq = three_cluster_dict[cluster]/three_cluster_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), three_cluster_dict[cluster], sep='\t\t', file=length_three_clusters)

# write the four_cluster dictionary to a file
sorted_length_four_cluster_list = sorted(four_cluster_dict.keys())
four_cluster_dict_freq = sum(four_cluster_dict.values())
length_four_clusters = open('output_files/length_four_clusters.txt', 'w')
for cluster in sorted_length_four_cluster_list:
    relative_freq = four_cluster_dict[cluster]/four_cluster_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), four_cluster_dict[cluster], sep='\t\t', file=length_four_clusters)

# write the the more_cluster dictionary to a file
sorted_length_more_cluster_list = sorted(more_cluster_dict.keys())
more_cluster_dict_freq = sum(more_cluster_dict.values())
other_clusters = open('output_files/other_clusters.txt', 'w')
for cluster in sorted_length_more_cluster_list:
    relative_freq = more_cluster_dict[cluster]/more_cluster_dict_freq
    print(cluster, '{:.{d}f}'.format(relative_freq, d=sig_fig), more_cluster_dict[cluster], sep='\t\t', file=other_clusters)

print("Done!")

print("Plotting...")

# lists of cluster frequencies
unique = np.fromiter(unique_clusters_dict.values(), dtype=int)
initial = np.fromiter(word_initial_clusters_dict.values(), dtype=int)
two = np.fromiter(two_cluster_dict.values(), dtype=int)
three = np.fromiter(three_cluster_dict.values(), dtype=int)
four = np.fromiter(four_cluster_dict.values(), dtype=int)
more = np.fromiter(more_cluster_dict.values(), dtype=int)

unique_total = sum(unique)
print(unique_total, 'unique_total')
initial_total = sum(initial)
two_total = sum(two)
three_total = sum(three)
four_total = sum(four)
more_total = sum(more)

names = ['unique', 'word-initial', 'two', 'three', 'four', 'more']
values = [unique_total, initial_total, two_total, three_total, four_total, more_total]
plt.figure(figsize=(5,5))
plt.bar(names, values)
plt.title('Overall cluster count')
plt.savefig('figures/overall_count')

unique_relative = unique / unique_total
initial_relative = initial / initial_total
two_relative = two / two_total
three_relative = three / three_total
four_relative = four / four_total
more_relative = more / more_total

fig, axs = plt.subplots(2,3, figsize=(10,10))
fig.suptitle('Distribution of relative frequencies')
axs[0,0].violinplot(unique_relative)
axs[0,0].set_title('unique')
axs[0,1].violinplot(initial_relative)
axs[0,1].set_title('word-initial')
axs[0,2].violinplot(two_relative)
axs[0,2].set_title('two')
axs[1,0].violinplot(three_relative)
axs[1,0].set_title('three')
axs[1,1].violinplot(four_relative)
axs[1,1].set_title('four')
axs[1,2].violinplot(more_relative)
axs[1,2].set_title('more')
fig.savefig('figures/relative_distributions.png')