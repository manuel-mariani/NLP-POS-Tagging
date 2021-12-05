import pandas as pd
from collections import defaultdict
from IPython.core.display import display, HTML


# Define a mapping between POS tags, their meaning and some colors
tag_map = {
    'CC': ('Coordin. Conjunction', '#c18401'),
    'TO': ('“to”', '#c18401'),
    'DT': ('Determiner', '#c18401'),
    'UH': ('Interjection', '#c18401'),
    'EX': ('Existential ‘there', '#c18401'),
    'MD': ('Modal can', '#c18401'),
    'LS': ('List item marker', '#c18401'),
    'IN': ('Preposition/sub-conj', '#c18401'),
    'CD': ('Cardinal number', '#282828'),
    'FW': ('Foreign word', '#282828'),
    'NN': ('Noun, singular/mass', '#282828'),
    'NNS': ('Noun, plural', '#282828'),
    'NNP': ('Proper noun, singul.', '#282828'),
    'NNPS': ('Proper noun, plural', '#282828'),
    'JJ': ('Adjective', '#50a14f'),
    'JJR': ('Adj. comparative ', '#50a14f'),
    'JJS': ('Adj. superlative ', '#50a14f'),
    'VB': ('Verb, base form', '#e45649'),
    'VBD': ('Verb, past tense ', '#e45649'),
    'VBG': ('Verb, gerund ', '#e45649'),
    'VBN': ('Verb, past particip. ', '#e45649'),
    'VBP': ('Verb, non-3sg pres', '#e45649'),
    'VBZ': ('Verb, 3sg pres ', '#e45649'),
    'WDT': ('Wh-determiner', '#4078f2'),
    'WP': ('Wh-pronoun', '#4078f2'),
    'WP$': (' Possessive wh-', '#4078f2'),
    'WRB': ('Wh-adverb how', '#4078f2'),
    'PDT': ('Predeterminer ', '#4078f2'),
    'POS': ('Possessive ending', '#4078f2'),
    'PP': ('Personal pronoun', '#4078f2'),
    'PP$': (' Possessive pronoun ', '#4078f2'),
    'RB': ('Adverb', '#a626a4'),
    'RBR': ('Adverb, comparative', '#a626a4'),
    'RBS': ('Adverb, superlative', '#a626a4'),
    'RP': ('Particle', '#a626a4'),
}
tag_map = defaultdict(lambda: ('', '#282828'), tag_map)


def display_pos_tagging(tokens: pd.Series,
                        predicted_tags: pd.Series,
                        correct_tags: pd.Series = None,
                        limit=1000):
    # If no correct tags are passed, we ignore the "error highlighting"
    if correct_tags is None:
        correct_tags = predicted_tags

    # Limit the inputs
    tokens = tokens[:limit]
    predicted_tags = predicted_tags[:limit]
    correct_tags = correct_tags[:limit]

    # Iterate through tokens and tags, generating styled HTML based on the tags
    html_sequence = []
    for token, tag, correct in zip(tokens, predicted_tags, correct_tags):
        tag_meaning = tag_map[tag][0]
        err = 'pos-error' if tag != correct else ''
        c = f'/{correct}' if tag != correct else ''
        h = f'<div class="token {tag} {err}">{token} <span class="tag">[{tag}{c}] {tag_meaning}</span></div>'

        if tag == '.':
            h += '<div class="separator"/>'
        html_sequence.append(h)
    html_body = '<div class="pos-visualizer">'
    html_body += ' '.join(html_sequence) + '</div>'

    # Generate the style (WARNING: CSS lies ahead)
    html_style = """
	<style>
	.pos-visualizer { padding: 32px; background-color: #FEFEFE; border-left:solid 1px grey;}
	.token { position:relative; display:inline-block; font-size:16px;}
	.token .tag { 
		visibility:hidden; width: 120px; text-align:center; position:absolute;
		width: 160px; background-color: #282828; color: #fff; border-radius: 6px;
		z-index: 1; bottom: 100%; left: 50%; margin-left:-80px; font-size:12px;
	}
	.pos-error { text-decoration: underline solid #F94144;}
	.separator { margin-top:12px }
	.token:hover .tag { visibility:visible }
	"""
    html_style += '\n'.join((f'.{tag} {{color:{tag_map[tag][1]};}}'
                             for tag in predicted_tags.unique()))
    html_style += '</style>'

    # Display the HTML in the cell's output
    display(HTML(html_style + html_body))


# USAGE EXAMPLE
#predicted_example = dataset['tag'].copy()
#predicted_example[0:8] = 'CD'  # Wrong prediction example for the first 8 words
#display_pos_tagging(dataset['token'],
#                    predicted_example,
#                    dataset['tag'],
#                    limit=120)
