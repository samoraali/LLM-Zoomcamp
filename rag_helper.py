from ingest import load_faq_data, build_index

documents = load_faq_data()
index = build_index(documents)

INSTRUCTION = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

USER_PROMPT_TEMPLATE = '''
Question:
{question}

Context:
{context}
'''

class RAG:

    def __init__(self, index):
        self.index = index
        

def search(self, question, course='llm-zoomcamp'):
    boost_dict = {'question':2.0, 'answer':1.0, 'section':0.5}
    filter_dict = {'course':course}

    return self.index.search(
        question,
        boost_dict = boost_dict,
        filter_dict = filter_dict,
        num_results=5
    )

def build_context(search_results):
    lines = []

    for doc in search_results:
        lines.append(doc['section'])
        lines.append('Q: ' + doc['question'])
        lines.append('A: ' + doc['answer'])
        lines.append('')

    return '\n'.join(lines).strip()

def build_prompt(question, search_results):
    context = build_context(search_results)
    prompt = USER_PROMPT_TEMPLATE.format(
        question=question, 
        context=context
        )
    return prompt.strip()

def llm(instructions, user_prompt, model='gpt-5.4-mini'):
    message_hisstory = [
        {'role': 'system', 'content': INSTRUCTION}, # System prompt
        {'role': 'user', 'content': prompt} # User prompt, changeable 
    ]

    response = openai_client.responses.create(
        model='gpt-5.4-mini',
        input=prompt
    )

    return response.output_text

def rag(query, model='gpt-5.4-mini'):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(INSTRUCTION, prompt, model = model)

    return answer