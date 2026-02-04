# Introduction
This project implements a probabilistic text generation system using Markov Chains, a stochastic model that predicts sequences based on the statistical properties of training data. The generator analyzes input text to learn word transition patterns, then uses these patterns to create novel text sequences that mimic the style and structure of the original material.
A Markov Chain is a mathematical system that transitions from one state to another based on probabilistic rules. The key property of Markov Chains is that the future state depends only on the current state, not on the sequence of events that preceded it. In text generation:

- **States** are words or sequences of words (n-grams)
- **Transitions** represent the probability of one word following another
- **Order** determines how many previous words influence the next word prediction

For example, in a 2nd-order Markov Chain, the next word depends on the previous two words, allowing the model to capture more context and generate more coherent text than a 1st-order model.

### Training Phase
1. **Text Processing**: Input text is tokenized into individual words and punctuation marks
2. **N-gram Construction**: The text is analyzed to build state representations (sequences of N words)
3. **Transition Counting**: The model counts how often each word follows each state
4. **Probability Calculation**: Raw counts are converted to probability distributions

### Generation Phase
1. **Initialization**: Start with a beginning state (marked with special tokens)
2. **Probabilistic Selection**: Randomly choose the next word based on learned probabilities
3. **State Update**: Shift the context window forward (sliding window technique)
4. **Iteration**: Repeat until reaching an end condition (end marker or maximum length)

## Key Features

- **Configurable Order**: Supports nth-order Markov models for varying levels of context
- **Beta Distribution**: Models how sequences begin (start probabilities)
- **Omega Distribution**: Models how sequences end (ending probabilities)
- **Weighted Random Selection**: Uses transition frequencies to probabilistically choose next words
- **Metadata Tracking**: Calculates statistics like average sentence length from training data
- **Reproducible Generation**: Seed-based random number generation for consistent outputs

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

We went through multiple stages of code development to reach our objectives while also trying to go above and beyond the expectations of the project. Through this experience, we learned how to navigate each another towards our goals while also being respectful of each other .One of the key successes of this project was the time and effort we invested in planning before implementation. We developed well-thought-out pseudocode that clearly outlined the structure and logic of our Markov chain algorithms, which helped guide our coding decisions and kept the project organized. By taking the time to discuss approaches and expectations early on, we established a shared understanding of the problem and how to solve it. We also made a conscious effort to coordinate our schedules and work through the project collaboratively. This deliberate planning and communication significantly improved the collaborative experience, allowing us to build on each other’s ideas, address questions early, and maintain consistency across the project. As a result, the implementation process was smoother and more efficient.

# Struggles
Description of the stumbling blocks the team experienced

As a team, we struggled to collaborate all of our ideas together and come up with a final implementation decision. It was a challenge as we had similar ideas at the beginning but towards the end, we took different approaches and had to integrate all our ideas together. A major challenge we encountered was merging code and ideas that worked correctly in isolation. While each of us had functional components, integrating them into a single, cohesive solution introduced unexpected roadblocks, such as differences in structure and implementation style. Despite these challenges, we worked through the issues by communicating openly, revisiting our design choices, and refining our approach as a group. Overcoming these obstacles strengthened our collaboration and problem-solving skills. By the end of the project, we were able to successfully integrate our work and were very satisfied with the final results.

# Personal Reflections
## Group Leader
Group leader's reflection on the project
Thu Thu Han - During this project, I faced some challenges with trying to be on track while also trying to fully grasp the concept of a markov model. Like everyone in my team, I had a hard time breaking through to get the optimal solution. From my perspective, I beleive that I had a harder time than my teammates in terms of understanding and designing a markov model algorithm for the Nth order. With that being said, I believe I have learned quite a lot in terms of colloboration and leadership in a tehnical project. I tried my best to merge all of our ideas together into one and doing so, I get to understand my teammates' thought process and the technical solutions they demonstrated to back up their ideas. This was my first time as a team leader and working with Stefanie and Shameem definitely made my job easier. 

## Other member
Shameem - I found this project to be a really enriching challenge. It seemed intimidating at first, but through the pseudocode and collaborating with my peers, I found that the process was much more manageable in chunks. Working on the individual functions to match a singular task decluttered my thought process, and as we moved on to the next steps, it made them easier. We also bounced a lot of really helpful ideas, such as the data structures and probability weightage, which also reinforced my understanding of the concepts. Overall, as difficult as I found this project, it was ultimately rewarding to see our outputs as somewhat meaningful texts.

Stefanie's Reflection:
This project was considerably more complex and challenging than Project01, particularly because of the volume of work upon breaking the instructions down into manageable components, required to fulfill the expectations of the assignment. We met and collaborated via phone in excess of a dozen times over the past week, and we all had very different ideas on how we each envisioned designing the program and each function to train the model and succeed in novel text generation in the style and characteristics of the input text. We considered obtaining novel text matching the input text's style as clear indication that our model was successful in learning the directions delineated in our functions to identify patterns from the input text. Ultimately, however, we agreed upon designing a single program with an Nth order parameter that was reusable with any input text file. We also tokenized each word/state and identified words with hyphens, words with apostrophes, isolated punctuation marks and numbers as individual states that became tokenized to preserve their semantic value. Start and end states were created and tokenized as well. We were very conscientious about adhering to DRY coding style and  one function  one task, and we feel we were able to successfully apply our program to the different input files and obtain the outputs we expected. Collaboration was key for success in this project because there was too much to account for for any one individual in a week's time, and this is where we really excelled. 

# Generative AI Appendix
As per the syllabus
Description of AI and version: We used Microsoft Copilot, powered by GPT-4

The prompt used was: “I have three versions of code here that we are trying to merge into a single program that is a markov chain based model to generate new text based on the style of the input text but we are struggling to merge these three versions. Can you help us identify where our parameters might not be matching up"

Explanation of use: Generative AI was used to assist in understanding how to merge independently written Python code by aligning logic, structure, and handling potential errors.

Justification for use: Generative AI was used to improve efficiency and support collaboration by providing guidance on code integration while allowing the team to focus on problem-solving and implementation.

