"""All knowledge specific to the approach is stored here."""

"""prompt prefix for ChatReadRetrieveReadApproach"""
prompt_prefix = """<|im_start|>system
Assistant helps the user with scientifica publication questions. Provide concise response in your answers.
Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. 
Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
For tabular information return it as an html table. Do not return markdown format.
Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response.
 Use square brakets to reference the source, e.g. [info1.pdf]. Don't combine sources, list each source separately, e.g. [info1.pdf][info2.pdf].
{follow_up_questions_prompt}
{injected_prompt}
Sources:
{sources}
<|im_end|>
{chat_history}
"""

follow_up_questions_prompt_content = """Generate three very brief follow-up questions that the user would likely ask next about the scientific publications. 
    Use double angle brackets to reference the questions, e.g. <<Are there any rate limits to be applied?>>.
    Try not to repeat questions that have already been asked.
    Only generate questions and do not generate any text before or after the questions, such as 'Next Questions'"""

query_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base about scientific publications.
    Generate a search query based on the conversation and the new question. 
    Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
    Do not include any text inside [] or <<>> in the search query terms.
    If the question is not in English, translate the question to English before generating the search query.

Chat History:
{chat_history}

Question:
{question}

Search query:
"""


# Path: app\backend\data\knowledge.py
# Examples for ReadDecomposeAsk Approach
# Modified version of langchain's ReAct prompt that includes instructions and examples for how to cite information sources
EXAMPLES = [
    """Question: What is the elevation range for the area that the eastern sector of the
Colorado orogeny extends into?
Thought 1: I need to search Colorado orogeny, find the area that the eastern sector
of the Colorado orogeny extends into, then find the elevation range of the
area.
Action 1: Search[Colorado orogeny]
Observation 1: [info1.pdf] The Colorado orogeny was an episode of mountain building (an orogeny) in
Colorado and surrounding areas.
Thought 2: It does not mention the eastern sector. So I need to look up eastern
sector.
Action 2: Lookup[eastern sector]
Observation 2: [info2.txt] (Result 1 / 1) The eastern sector extends into the High Plains and is called
the Central Plains orogeny.
Thought 3: The eastern sector of Colorado orogeny extends into the High Plains. So I
need to search High Plains and find its elevation range.
Action 3: Search[High Plains]
Observation 3: [some_file.pdf] High Plains refers to one of two distinct land regions
Thought 4: I need to instead search High Plains (United States).
Action 4: Search[High Plains (United States)]
Observation 4: [filea.pdf] The High Plains are a subregion of the Great Plains. [another-ref.docx] From east to west, the
High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130
m).
Thought 5: High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer
is 1,800 to 7,000 ft.
Action 5: Finish[1,800 to 7,000 ft (filea.pdf) ]""",
    """Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons"
character Milhouse, who Matt Groening named after who?
Thought 1: The question simplifies to "The Simpsons" character Milhouse is named after
who. I only need to search Milhouse and find who it is named after.
Action 1: Search[Milhouse]
Observation 1: [info7.pdf] Milhouse Mussolini Van Houten is a recurring character in the Fox animated
television series The Simpsons voiced by Pamela Hayden and created by Matt
Groening.
Thought 2: The paragraph does not tell who Milhouse is named after, maybe I can look up
"named after".
Action 2: Lookup[named after]
Observation 2: [historyref2.txt] (Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose
middle name was Milhous.
Thought 3: Milhouse was named after U.S. president Richard Nixon, so the answer is
Richard Nixon.
Action 3: Finish[Richard Nixon (historyref2.txt) ]""",
    """Question: Which documentary is about Finnish rock groups, Adam Clayton Powell or The
Saimaa Gesture?
Thought 1: I need to search Adam Clayton Powell and The Saimaa Gesture, and find which
documentary is about Finnish rock groups.
Action 1: Search[Adam Clayton Powell]
Observation 1: [info9.pdf] Could not find [Adam Clayton Powell]. Similar: ['Adam Clayton Powell
III', 'Seventh Avenue (Manhattan)', 'Adam Clayton Powell Jr. State Office
Building', 'Isabel Washington Powell', 'Adam Powell', vAdam Clayton Powell
(film)', 'Giancarlo Esposito'].
Thought 2: To find the documentary, I can search Adam Clayton Powell (film).
Action 2: Search[Adam Clayton Powell (film)]
Observation 2: [data123.txt] Adam Clayton Powell is a 1989 American documentary film directed by
Richard Kilberg. The film is about the rise and fall of influential
African-American politician Adam Clayton Powell Jr.[3][4] It was later aired
as part of the PBS series The American Experience.
Thought 3: Adam Clayton Powell (film) is a documentary about an African-American
politician, not Finnish rock groups. So the documentary about Finnish rock
groups must instead be The Saimaa Gesture.
Action 3: Finish[The Saimaa Gesture (data123.txt) ]""",
    """Question: What profession does Nicholas Ray and Elia Kazan have in common?
Thought 1: I need to search Nicholas Ray and Elia Kazan, find their professions, then
find the profession they have in common.
Action 1: Search[Nicholas Ray]
Observation 1: [files-987.png] Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 - June 16,
1979) was an American film director, screenwriter, and actor best known for
the 1955 film Rebel Without a Cause.
Thought 2: Professions of Nicholas Ray are director, screenwriter, and actor. I need
to search Elia Kazan next and find his professions.
Action 2: Search[Elia Kazan]
Observation 2: [files-654.txt] Elia Kazan was an American film and theatre director, producer, screenwriter
and actor.
Thought 3: Professions of Elia Kazan are director, producer, screenwriter, and actor.
So profession Nicholas Ray and Elia Kazan have in common is director,
screenwriter, and actor.
Action 3: Finish[director, screenwriter, actor (files-987.png)(files-654.txt) ]""",
    """Question: Which magazine was started first Arthur's Magazine or First for Women?
Thought 1: I need to search Arthur's Magazine and First for Women, and find which was
started first.
Action 1: Search[Arthur's Magazine]
Observation 1: [magazines-1850.pdf] Arthur's Magazine (1844-1846) was an American literary periodical published
in Philadelphia in the 19th century.
Thought 2: Arthur's Magazine was started in 1844. I need to search First for Women
next.
Action 2: Search[First for Women]
Observation 2: [magazines-1900.pdf] First for Women is a woman's magazine published by Bauer Media Group in the
USA.[1] The magazine was started in 1989.
Thought 3: First for Women was started in 1989. 1844 (Arthur's Magazine) < 1989 (First
for Women), so Arthur's Magazine was started first.
Action 3: Finish[Arthur's Magazine (magazines-1850.pdf)(magazines-1900.pdf) ]""",
    """Question: Were Pavel Urysohn and Leonid Levin known for the same type of work?
Thought 1: I need to search Pavel Urysohn and Leonid Levin, find their types of work,
then find if they are the same.
Action 1: Search[Pavel Urysohn]
Observation 1: [info4444.pdf] Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet
mathematician who is best known for his contributions in dimension theory.
Thought 2: Pavel Urysohn is a mathematician. I need to search Leonid Levin next and
find its type of work.
Action 2: Search[Leonid Levin]
Observation 2: [datapoints_aaa.txt] Leonid Anatolievich Levin is a Soviet-American mathematician and computer
scientist.
Thought 3: Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn
and Leonid Levin have the same type of work.
Action 3: Finish[yes (info4444.pdf)(datapoints_aaa.txt) ]""",
]
SUFFIX = """\nQuestion: {input}
{agent_scratchpad}"""
PREFIX = "Answer questions as shown in the following examples, by splitting the question into individual search or lookup actions to find facts until you can answer the question. " \
"Observations are prefixed by their source name in square brackets, source names MUST be included with the actions in the answers." \
"Only answer the questions using the information from observations, do not speculate."

# template prefix for ReadRetrieveReadApproach
template_prefix = \
"You are an intelligent assistant helping user with their questions on scientific publications. " \
"Answer the question using only the data provided in the information sources below. " \
"For tabular information return it as an html table. Do not return markdown format. " \
"Each source has a name followed by colon and the actual data, quote the source name for each piece of data you use in the response. " \
"For example, if the question is \"What color is the sky?\" and one of the information sources says \"info123: the sky is blue whenever it's not cloudy\", then answer with \"The sky is blue [info123]\" " \
"It's important to strictly follow the format where the name of the source is in square brackets at the end of the sentence, and only up to the prefix before the colon (\":\"). " \
"If there are multiple sources, cite each one in their own square brackets. For example, use \"[info343][ref-76]\" and not \"[info343,ref-76]\". " \
"Never quote tool names as sources." \
"If you cannot answer using the sources below, say that you don't know. " \
"\n\nYou can access to the following tools:"
    
template_suffix = """
Begin!

Question: {input}

Thought: {agent_scratchpad}"""   


# template for RetrieveThenReadApproach
template = \
"You are an intelligent assistant helping users with questions on scientific publications." + \
"Use 'you' to refer to the individual asking the questions even if they ask with 'I'. " + \
"Answer the following question using only the data provided in the sources below. " + \
"For tabular information return it as an html table. Do not return markdown format. "  + \
"Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. " + \
"If you cannot answer using the sources below, say you don't know. " + \
"""

###
Question: 'How can we use motion textures for automated skill assessmnet?'

Sources:
info1.pdf: Motion texture analysis for OSATS.
info2.pdf: Cross entropy analysis
info3.pdf: Sequential motion textures
info4.pdf: Spectral clustering

Answer:
Step 1) Motion feature extraction: To obtain the frame kernel matrix, first
detect the spatio-temporal interest points (STIP) using Laptev detector.
Step 2) Learning motion classes: Collect all the detected STIPs and their
corresponding HOG-HOF descriptors from two videos and
classify the STIPs into k distinct clusters by applying k-means clustering to the
HoG-HoF descriptors.
Step 3) Classification of STIPs into motion classes: Each cluster of points
(learnt in step 2) represents a distribution for a particular motion class in the
data. 
Step 4) Computing motion class counts: Process each video to compute
motion class counts for each of the k classes in each frame. 


###
Question: '{q}'?

Sources:
{retrieved}

Answer:
"""