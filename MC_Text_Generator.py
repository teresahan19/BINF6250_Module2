#!/usr/bin/env python
# Shebang line to execute script directly from command line

# Import necessary modules and packages
# Random for generating random numbers in weighting,
# allowing for probabilistic token selection during text generation
import random
# re for regex use in tokenize(), enabling extraction of words, numbers, punctuation
import re
# textwrap for ease of reading of generated text]
import textwrap
# defaultdict: used throughout model to automatically initiate dict
# values like counts without checking for key existence
# Counter: used in word_frequencies() to tally token occurrences efficiently
from collections import defaultdict, Counter


def read_text_file(filepath):
    """
    Function to open and read text file by line, remove whitespace,
    newline chars, leading and trailing whitespace.
        Parameters: filepath (string): Path to text file
        Return: text (string): sting of continuous, cleaned text
    """

    # Initialize empty string
    text = " "
    # Open file with context manager
    with open(filepath, "r") as file:
        # Read file by line
        for line in file:
            # Strip whitespace, newline chars, leading and trailing,
            # Add space between lines
            text += " " + line.strip()
    # Return final, continuous text string
    return text


def tokenize(text):
    """
    Helper fxn to convert raw text into a list of lowercase tokens.
    Handles words, archaic contractions, hyphens, and punctuation.
    Parameters: text (string): text to tokenize
    Returns: list (string): List of tokens extracted from text
    """

    # Token patterns:
    # [A-Za-z]+(?:[-'][A-Za-z]+)* -> words, incl those with hyphens or apostrophes
    # Note: Even though converting to lowercase before tokenizing, include capitals
    # For robustness and clarity purposes (convention)
    # \d+ -> numbers
    # [\"'()\-\.,!?;:] -> single punctuation characters
    pattern = r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+|[\"'()\-\.,!?;:]"

    # Convert to lowercase and extract words, numbers, punctuation as
    # regex-pattern defined tokens
    tokens = re.findall(pattern, text.lower())

    return tokens


def word_frequencies(text):
    """
    Count the number of times each token appears in input text
    Parameter: text (string): raw input text
    Returns: token freqs (dictionary): mapping of tokens to their frequencies
    """

    # Convert raw text into list of tokens with tokenize helper function
    tokens = tokenize(text)

    # Counter auto-counts frequencies for each token within text
    freqs = Counter(tokens)

    return freqs  # Return frequency dictionary


def word_probabilities(text):
    """
    Compute probabilities of each token in the text
    Parameters: text (string): Raw input text
    Returns: dictionary: mapping of tokens to probabilities
    """

    # Get raw freq counts for each token
    freqs = word_frequencies(text)

    # Total number tokens in text
    total = sum(freqs.values())

    # Convert freqs for each token into probability
    probs = {token: count / total for token, count in freqs.items()}

    # Return probability dictionary
    return probs


def ngram_frequencies(text, order):
    """
    Counts how often each n-gram state transitions to another token. Establishes
    the premise of Markov chain by creating the structure from which counts become
    transition and ending probabilities for text generation model.
        Parameters: text (string): raw input text
                    order (int): the Markov chain order (size of state)
        Returns: dict: mapping of state tuples to dictionaries of next token counts:
    """

    # Tokenize raw text into list of tokens
    tokens = tokenize(text)

    # Add start (beta) and end markers so model knows where sequences begin/end
    tokens = ["*S*"] * order + tokens + ["*E*"]

    # Initialize nested dictionary with lambda where outer dict maps state -> inner dict
    # and inner dict maps next_token -> count
    # Use defaultdict because new state doesn't have dictionary yet,
    # and new next_token has no count yet
    freqs = defaultdict(lambda: defaultdict(int))

    # Iterate through tokens to build n-gram counter
    for i in range(len(tokens) - order):
        # The state is the previous order tokens
        state = tuple(tokens[i : i + order])

        # Initialize next token after state
        next_token = tokens[i + order]

        # Increment count for transition
        freqs[state][next_token] += 1

    # Convert nested defaultdicts to normal dicts for clarity
    return {state: dict(next_tokens) for state, next_tokens in freqs.items()}


def build_markov_model(text, order):
    """
    Build full Markov model from input text
        Parameters: text (string): raw input text
                    order (int): the Markov chain order (size of state)
        Returns: dict:: mapping of state tuples to dictionaries of next_token counts
    """

    # Compare n-gram transition freqs for text to determine state -> {next_token: count}
    model = ngram_frequencies(text, order)

    # Return model dictionary to use for text generation
    return model


def distribution_frequencies(items):
    """
    Count frequencies of any list of items.
        Parameters: items (list): a list of hashable items (e.g., states)
        Returns: dict: mapping of each item to its frequency count
    """

    freqs = defaultdict(int)

    # Count how often each item appears
    for item in items:
        freqs[item] += 1

    return dict(freqs)


def distribution_probabilities(freqs):
    """
    Convert frequency dictionary into probability distribution.
        Parameters: freqs (dict): mapping of items to frequency counts
        Returns: dict: mapping of items to probabilities
    """

    total = sum(freqs.values())
    probs = {}

    # Convert each count into probability
    for item, count in freqs.items():
        if total == 0:
            probs[item] = 0.0
        else:
            probs[item] = count / total

    return probs



def beta_frequencies(text, order):
    """
    Counts how often each starting state appears in text
        Parameters: text (string): raw input text
                    order (int): the Markov chain order (size of state)
        Returns: dict: mapping of start-state tuples to their frequencies
    """

    # Tokenize raw text into list of tokens
    tokens = tokenize(text)

    # Add "order" start markers for model to identify sequence beginning
    # This creates an artificial start token of length: order since an
    # nth order Markov chain is defined as the previous N tokens, but
    # at the start of a text, there are no previous tokens
    tokens = ["*S*"] * order + tokens

    # Extract start state, allowing beta to be computed
    start_state = tuple(tokens[:order])

    # Use generalized frequency counter on a list containing the start state
    # For a single text, this will usually yield {start_state: 1}
    freqs = distribution_frequencies([start_state])

    # Return frequency dictionary
    return freqs


def beta_probabilities(beta_freqs):
    """
    Converts start-state frequencies (beta) into start-state probabilities.
        Parameters: beta_freqs (dict): mapping of start-state tuples to frequencies
        Returns: dict: mapping of start-state tuples to probabilities
    """

    # Use generalized probability normalizer
    beta_probs = distribution_probabilities(beta_freqs)

    # Return dictionary containing normalized beta probabilities
    return beta_probs



def omega_frequencies(markov_model):
    """
    Count how often each state transitions to end marker *E*.
        Parameters: markov_model (dict): mapping of state tuples to next-token counts
        Returns: dict: mapping of state tuples to frequency of ending transitions
    """

    # Create dictionary to store number of times each state concludes sequence
    # Each key is state tuple, and value is count of transitions to *E*.
    omega_freqs = {}

    # Iterate through all states in Markov model
    # Each state has dictionary of next-token counts
    for state, transitions in markov_model.items():

        # Check whether state transitions to end marker *E*
        # If so, record how many times it occurs
        if "*E*" in transitions:
            omega_freqs[state] = transitions["*E*"]
        else:
            # If state never transitions to *E*, ending frequency is zero.
            omega_freqs[state] = 0

    # Return dictionary of ending frequencies
    return omega_freqs


def omega_probabilities(omega_freqs):
    """
    Converts end-state frequencies (omega) into end-state probabilities
        Parameters: omega_freqs (dict): mapping of end-state tuples to frequencies
        Returns: dict: mapping of end-state tuples to ending probabilities
    """

    # Use generalized probability normalizer
    omega_probs = distribution_probabilities(omega_freqs)

    # Return dictionary of ending probabilities
    return omega_probs


def weighted_choice(options_dict):
    """
    Select token from dictionary of {token: probability} applying random weightings
        Parameters: options_dict (dict): mapping of tokens to probabilities
        Returns: string: single token chosen according to probability weight
    """

    # Generate random float between 0 and 1
    # Use to decide which token to return
    r = random.random()

    # Track total probabilities while iterating through text
    cumulative = 0.0

    # Iterate through tokens and probabilities
    for token, prob in options_dict.items():

        # Add token's probability to running total
        cumulative += prob

        # If random number falls within cumulative range,
        # Select this token
        if r <= cumulative:
            return token

    # If rounding errors occur and no token was returned above,
    # return the last token in the dictionary as a fallback
    return token


def get_next_word(state, model, omega_probs):
    """
    Given current state, predict next token based on model's transition
    probabilities and omega (ending) probabilities
        Parameters: state (tuple): the current Markov state of length 'order'
                model (dict): mapping of states to next-token counts
                omega_probs (dict): omega probabilities from each state
        Returns: string: next token (either real token or '*E*')
    """

    # Check whether current state should end sequence
    # If omega probability >0, treat as possible outcome
    end_prob = omega_probs.get(state, 0.0)

    # Initialize dictionary of probabilities for all possible next tokens
    # This includes both real tokens and omega marker '*E*'
    next_token_probs = {}

    # If state exists in model, convert next-token counts into probabilities
    if state in model:

        # Retrieve next-token counts dictionary for this state
        transitions = model[state]

        # Compute the total number of transitions out of this state
        total = sum(transitions.values())

        # Convert each count into a probability
        for token, count in transitions.items():
            next_token_probs[token] = count / total

    # Add the ending probability (omega) as a possible next token
    # This tells generator to stop when appropriate
    if end_prob > 0:
        next_token_probs["*E*"] = end_prob

    # Use weighted_choice to select the next token
    return weighted_choice(next_token_probs)


def generate_random_text(model, beta_probs, omega_probs, order, max_words=50):
    """
    Generate a random text sequence using the Markov model.
    Parameters: model (dict): mapping of states to next-token counts
                beta_probs (dict): start-state probability distribution
                omega_probs (dict): ending-state probability distribution
                order (int): the Markov chain order (size of the state)
                max_words (int): maximum number of tokens to generate
    Returns: string: the generated text
    """

    # Choose starting state using beta (start) probabilities
    # weighted_choice returns one of the possible start states
    current_state = weighted_choice(beta_probs)

    # Create a list to store the generated tokens.
    generated = []

    # Generate up to max_words tokens.
    for _ in range(max_words):

        # Choose the next token based on the current state
        next_token = get_next_word(current_state, model, omega_probs)

        # If the next token is the end marker, stop generation
        if next_token == "*E*":
            break

        # Add the chosen token to the output list
        generated.append(next_token)

        # Update the state by shifting left and adding the new token
        current_state = tuple(list(current_state[1:]) + [next_token])

    # Join the generated tokens into a single string
    return " ".join(generated)


def output_generated_text(text, filename, width=80):
    """
    Print generated text to terminal and save to text file using text wrapping for visual ease
        Parameters: text (string): generated text from Markov model trained with input text
                    filename (string): name of file to save generated text to
        Returns: None
    """

    # Wrap text for readability
    wrapped_text = textwrap.wrap(text, width=width)

    # Print results to terminal
    print(wrapped_text)

    # Save text generated from Markov model to output file
    with open(filename, "w") as f:
        f.write(wrapped_text)


if __name__ == "__main__":
    """
    Driver code to run the Markov chain text generator.
    This block executes only when the script is run directly
    (not when imported as a module).
    """

    # Input file to use from project directory
    input_file = "one_fish_two_fish.txt"

    # Markov chain order (N)
    order = 1

    # Open and read input file by line
    raw_text = read_text_file(input_file)

    # Apply Markov model to learn text style for generating new text
    model = build_markov_model(raw_text, order)

    # Compute beta (start-state) distribution
    beta_freqs = beta_frequencies(raw_text, order)
    beta_probs = beta_probabilities(beta_freqs)

    # Compute omega (end-state) distribution
    omega_freqs = omega_frequencies(model)
    omega_probs = omega_probabilities(omega_freqs)

    # Generate text
    generated_text = generate_random_text(
        model=model,
        beta_probs=beta_probs,
        omega_probs=omega_probs,
        order=order,
        max_words=50
    )

    # Print  generated text to terminal and save to output file
    output_generated_text(generated_text, "generated_output.txt")

