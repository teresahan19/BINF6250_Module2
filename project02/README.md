# Introduction
Description of the project2

# Pseudocode
Put pseudocode in this box:

```
## PART 1: FILE READING AND TOKENIZATION

### FUNCTION read_text_file(filepath)

**Purpose:** Load and prepare text from file

**Steps:**
1. Initialize empty text string
2. Open file with UTF-8 encoding
3. Read file line by line
4. Strip whitespace and newline characters from each line
5. Concatenate lines with space separators
6. Return prepared text string

---

### FUNCTION tokenize(text)

**Purpose:** Convert raw text into list of processable tokens

**Steps:**
1. Define regex pattern for tokens (words, numbers, punctuation)
2. Convert text to lowercase
3. Use regex to extract all matching tokens
4. Return list of tokens

---

## PART 2: WORD FREQUENCY AND PROBABILITY CALCULATIONS

### FUNCTION word_frequencies(text)

**Purpose:** Count occurrences of each token

**Steps:**
1. Tokenize the input text
2. Use Counter to count token occurrences
3. Return frequency dictionary

---

### FUNCTION word_probabilities(text)

**Purpose:** Convert word frequencies to probabilities

**Steps:**
1. Get word frequencies from text
2. Calculate total word count by summing all frequencies
3. Divide each frequency by total to get probability
4. Return probability dictionary

---

## PART 3: N-GRAM FREQUENCY BUILDING

### FUNCTION ngram_frequencies(text, order)

**Purpose:** Build state transition counts for Markov model

**Steps:**
1. Tokenize the input text
2. Add order number of start markers to beginning
3. Add single end marker to end
4. Initialize nested defaultdict structure for transition counts
5. Loop through tokens with sliding window of size order
6. For each position, extract current state as tuple of order tokens
7. Get next token after current state
8. Increment transition count for current state to next token
9. Convert nested defaultdicts to regular dictionaries
10. Return frequency model dictionary

---

### FUNCTION build_markov_model(text, order)

**Purpose:** Wrapper to create complete Markov model

**Steps:**
1. Call ngram_frequencies with text and order
2. Return resulting model dictionary

---

## PART 4: DISTRIBUTION UTILITIES

### FUNCTION distribution_frequencies(items)

**Purpose:** Generic frequency counter for any list of items

**Steps:**
1. Initialize defaultdict with integer default
2. Loop through items list
3. Increment count for each item
4. Convert defaultdict to regular dictionary
5. Return frequency dictionary

---

### FUNCTION distribution_probabilities(freqs)

**Purpose:** Convert any frequency dictionary to probabilities

**Steps:**
1. Calculate total by summing all frequency values
2. Initialize empty probability dictionary
3. Loop through each item and its frequency
4. Handle division by zero case
5. Calculate probability as frequency divided by total
6. Store probability in dictionary
7. Return probability dictionary

---

## PART 5: BETA DISTRIBUTION (START PROBABILITIES)

### FUNCTION beta_frequencies(text, order)

**Purpose:** Calculate start state frequencies

**Steps:**
1. Tokenize the input text
2. Add order number of start markers to beginning only
3. Extract first order tokens as start state tuple
4. Pass start state in list to distribution_frequencies
5. Return start state frequency dictionary

---

### FUNCTION beta_probabilities(beta_freqs)

**Purpose:** Convert start frequencies to probabilities

**Steps:**
1. Call distribution_probabilities on beta_freqs
2. Return start state probability dictionary

---

## PART 6: OMEGA DISTRIBUTION (END PROBABILITIES)

### FUNCTION omega_frequencies(markov_model)

**Purpose:** Calculate ending state frequencies

**Steps:**
1. Initialize empty omega frequency dictionary
2. Loop through each state in markov model
3. For each state, check if end marker exists in transitions
4. If end marker exists, store its count
5. If end marker doesn't exist, store zero
6. Return ending frequency dictionary

---

### FUNCTION omega_probabilities(omega_freqs)

**Purpose:** Convert ending frequencies to probabilities

**Steps:**
1. Call distribution_probabilities on omega_freqs
2. Return ending probability dictionary

---

## PART 7: TEXT GENERATION

### FUNCTION get_next_word(current_word, markov_model)

**Purpose:** Select next word using weighted random choice

**Steps:**
1. Check if current state exists in model
2. If state not in model, return end marker
3. Get transitions dictionary for current state
4. Extract counts as list of values
5. Extract words as list of keys
6. Use random.choices with counts as weights
7. Extract first element from result list
8. Return selected next word

---

### FUNCTION generate_random_text(markov_model, seed, max_length, order)

**Purpose:** Generate complete text sequence

**Steps:**
1. Set random seed if provided
2. Initialize current state as tuple of order start markers
3. Initialize empty sentence list
4. Loop up to max_length iterations
5. Call get_next_word with current state
6. Check if next word is end marker
7. If end marker, break loop
8. Append next word to sentence list
9. Update current state by sliding window
10. Remove first element from current state tuple
11. Add next word to end of state tuple
12. After loop ends, join sentence list with spaces
13. Return generated text string

---

### FUNCTION compute_metadata(text)

**Purpose:** Calculate text statistics like average sentence length

**Steps:**
1. Split text by sentence-ending punctuation using regex
2. Remove empty strings and whitespace
3. Return default if no sentences found
4. Count words in each sentence
5. Calculate average by dividing total words by sentence count
6. Round to nearest integer
7. Return metadata dictionary with average length

---

### FUNCTION output_generated_text(text, filename, width)

**Purpose:** Display and save generated text

**Steps:**
1. Wrap text to specified width using textwrap
2. Print wrapped text to terminal
3. Open output file with UTF-8 encoding
4. Write wrapped text to file
5. Close file

---

## PART 8: MAIN PROGRAM EXECUTION

### MAIN PROGRAM FLOW

**Steps:**
1. Specify input file path
2. Set model order parameter
3. Read raw text from file
4. Build Markov model with specified order
5. Set random seed for reproducibility
6. Generate text with model, seed, max length, and order
7. Output generated text to terminal and file
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
