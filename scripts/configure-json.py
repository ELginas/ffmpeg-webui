import re
import json
from pprint import pprint

path = '../../ffmpeg/build/configure.txt'
text = open(path).read()
text = text.removesuffix("NOTE: Object files are built at the place where configure is launched.\n")

last_end = 0
current_section = ""
sections = {}
for result in re.finditer(r'\n([a-zA-Z0-9() ]+):\n', text):
    section_name = result.group(1).strip()
    start, end = result.span(0)
    sections[current_section] = text[last_end:start]
    last_end = end
    current_section = section_name
sections[current_section] = text[last_end:len(text)]
sections.pop("")

def search_group_1(regex, text):
    match = re.search(regex, text)
    if match:
        return match.group(1)

def flag_text_to_title(text):
    words = [word for word in text.split('-')]
    words[0] = words[0].capitalize()
    return ' '.join(words)

def process_text_blob(state, text_blob):
    if state == "flag":
        lines = [line.strip() for line in text_blob]
        text = ' '.join(lines)
        match = re.search(r'--([a-zA-Z0-9-_=]+)', text)
        description = text[match.span(0)[1]:].strip()
        flag_text = match.group(1)

        value_suffix = search_group_1(r'\[([^\[\]]*)\]', description)

        if value_suffix != None:
            description = description.removesuffix(f' [{value_suffix}]')
        if description and description[0].isalpha():
            description = description[0].upper() + description[1:]

        flag = None
        name = None
        title = None
        obj = {}
        if '=' in flag_text:
            spl = flag_text.split('=', 1)
            title = flag_text_to_title(spl[0])
            flag = f'--{spl[0]}'
            obj['ty'] = 'text'
            obj['name'] = spl[1]
            if value_suffix:
                obj['def'] = value_suffix
        else:
            flag = f'--{flag_text}'
            title = flag_text_to_title(flag_text)
            obj['ty'] = 'checkbox'
            obj['isAutodetect'] = value_suffix in ['auto', 'autodetect']
        obj['title'] = title
        obj['flag'] = flag
        obj['description'] = description
        return obj
    elif state == "description":
        lines = [line.strip() for line in text_blob]

        text = ''
        for line in lines:
            if len(line) == 0:
                text += '\n\n'
            else:
                if len(text) > 0 and text[len(text)-1] != '\n':
                    text += ' '
                text += line
        
        text = text.strip()
        if len(text) == 0:
            return

        obj = {}
        obj['ty'] = 'description'
        obj['description'] = text
        return obj

def ignore_append_empty(arr, el):
    if not el:
        return
    arr.append(el)

data = {}
for section in sections:
    text = sections[section]
    state = ""
    text_blob = []
    section_data = []
    for line in text.splitlines():
        if line.startswith("  --"):
            ignore_append_empty(section_data, process_text_blob(state, text_blob))
            text_blob.clear()
            state = "flag"
            text_blob.append(line)
        elif line.startswith("    "):
            text_blob.append(line)
        else:
            if state != "description":
                state = "description"
                text_blob.clear()
            text_blob.append(line)
    ignore_append_empty(section_data, process_text_blob(state, text_blob))
    data[section] = section_data

json_text = json.dumps(data)
open('../src/lib/data.json', 'w').write(json_text)
print('Done')