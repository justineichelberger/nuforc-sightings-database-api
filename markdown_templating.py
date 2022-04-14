import glom
import os
from documentation import *
from glom import glom, Assign
from pprint import pprint


def githubflavoredmarkdown(sitemapper):    
    markdown_text_for_template = ''
    markdown_text = open("./templates/README.template.md", "r").read()
    path_list = []
    for link in sitemapper:
        if link == sitemapper[-1]:
            markdown_text_for_template += f"\n[`{link[0]}`](#index)\n"
        elif link[0].endswith('query') == True:
            markdown_text_for_template += f"\n[`{link[0] + '?'}`](#{link[0].replace('/', '').replace('_', '').replace(':', '').replace('.','')})\n"
        else:    
            markdown_text_for_template += f"\n[`{link[0].replace(':', '?')}`](#{link[0].replace('/', '').replace('_', '').replace(':', '').replace('.','')})\n"
    
    markdown_text_for_template += "\n</details></h3>\n"

    for link in sitemapper:
        if link == sitemapper[-1]:
            markdown_text_for_template += f"\n#### '/' (index)\n"
            
            markdown_text_for_template += glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}index.index.description") + "\n"

            markdown_text_for_template += '\nuse:   ' + glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}index.index.use") + "\n"

            markdown_text_for_template += '\ninput format:   `' + glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}index.index.input_format") + "`\n"

        else:
            markdown_text_for_template += f"\n#### '{link[0]}'\n"
           
            markdown_text_for_template += glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}.{link[0].replace('.', '').replace('/', '.').replace(':', '.').split('.')[-1]}.description") + "\n"

            markdown_text_for_template += '\nuse:   ' + glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}.{link[0].replace('.', '').replace('/', '.').replace(':', '.').split('.')[-1]}.use") + "\n"

            markdown_text_for_template += '\ninput format:   ' + glom(documentor(directory_list, target), f"endpoints{link[0].replace('.', '').replace('/', '.').replace(':', '.')}.{link[0].replace('.', '').replace('/', '.').replace(':', '.').split('.')[-1]}.input_format") + "\n"
        markdown_text_for_template += '\n<sub>[Glossary](#endpoints)</sub>\n'
        markdown_text_for_template += '\n<sub>[Contents](#nuforc-sightings-database-api)</sub>\n'
        
    new_markdown_text = markdown_text.replace("{random_sighting}", markdown_text_for_template)

    new_readme = open("README.md", "w")
    new_readme.write(new_markdown_text)

