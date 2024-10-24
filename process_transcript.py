import re
import csv

def split_into_sentences(text):
    # Use regular expressions to split the text by punctuation that ends sentences.
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+|\n+', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def count_words(sentence):
    return len(sentence.split())

def combine_short_sentences(sentences, threshold):
    combined_sentences = []

    i = 0
    while i < len(sentences):
        current_sentence = sentences[i]
        if count_words(current_sentence) < threshold:
            if i == 0:  # If it's the first sentence, combine with the next one
                next_sentence = sentences[i + 1] if i + 1 < len(sentences) else ""
                combined_sentence = current_sentence + " " + next_sentence
                combined_sentences.append(combined_sentence)
                i += 2  # Skip the next sentence because it's been combined
            elif i == len(sentences) - 1:  # If it's the last sentence, combine with the previous one
                combined_sentences[-1] = combined_sentences[-1] + " " + current_sentence
                i += 1
            else:  # Otherwise, combine with the shorter of the previous or next sentence
                prev_sentence = combined_sentences[-1]
                next_sentence = sentences[i + 1] if i + 1 < len(sentences) else ""

                if count_words(prev_sentence) <= count_words(next_sentence):
                    combined_sentences[-1] = prev_sentence + " " + current_sentence
                    i += 1
                else:
                    combined_sentence = current_sentence + " " + next_sentence
                    combined_sentences.append(combined_sentence)
                    i += 2  # Skip the next sentence
        else:
            combined_sentences.append(current_sentence)
            i += 1

    # Recursively apply the combination until all sentences meet the threshold
    if any(count_words(s) < threshold for s in combined_sentences):
        return combine_short_sentences(combined_sentences, threshold)
    return combined_sentences

def process_transcript(input_file, output_file, word_threshold=7):
    # Read the transcript from the .txt file
    with open(input_file, 'r', encoding='utf-8') as file:
        transcript = file.read()

    # Split transcript into sentences
    sentences = split_into_sentences(transcript)

    # Combine sentences below the threshold
    combined_sentences = combine_short_sentences(sentences, word_threshold)

    # Write the result to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Don't write the header, just the sentences
        # csvwriter.writerow(['Sentence'])  # Write the header
        for sentence in combined_sentences:
            csvwriter.writerow([sentence])

if __name__ == "__main__":
    # Example of how to use the script
    input_filename = 'transcript.txt'
    output_filename = 'transcript.csv'
    word_threshold = 7  # Example threshold for minimum word count

    process_transcript(input_filename, output_filename, word_threshold)

