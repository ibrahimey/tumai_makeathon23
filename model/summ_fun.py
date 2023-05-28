import cohere
import re

co = cohere.Client('6xqBv4MIGMpmo5PRgZlsyUlMq3QZhoE8A1qLvsv3')


def magic_stuff(text):
    data = re.split("\n.", text)
    gen_data = []
    for x in data:
        gen_data = co.generate(prompt=x, model='base-light',
                               temperature=0.2, k=10, p=0.6)

    for x in gen_data:
        if x['relevance_score'] <= 0.3:
            gen_data[x['index']] = ""
    return_data = co.summarize(" ".join(gen_data), length="auto",format='bullets', model='summarize-xlarge', extractiveness="high", temperature=0.3, additional_command="written as a report")
    
    return return_data
