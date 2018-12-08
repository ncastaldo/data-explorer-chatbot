from modules.database import resolver


def get_buttons_relation_list(element_type):
    relation_list = resolver.get_element_properties(element_type)['relation_list']
    buttons = []
    for r in relation_list:
        title = r['type']
        payload = '/view_related_element{{"element":"{}"}}'.format(r['type'])
        buttons.append({'title': title, 'payload': payload})
    return buttons


def get_buttons_select_element(element_type, element_list):
    word_list = resolver.get_element_properties(element_type)['word_list']
    buttons = []
    for i, e in enumerate(element_list):
        title = ' '.join(e[x] for x in word_list)
        payload = '/select_element_by_position{{"position":"{}"}}'.format(i+1)
        buttons.append({'title': title, 'payload': payload})
    return buttons


def get_buttons_word_list(element_type, element_list, payload_list):
    word_list = resolver.get_element_properties(element_type)['word_list']
    buttons = []
    for i, e in enumerate(element_list):
        title = ' '.join(e[x] for x in word_list)
        payload = payload_list[i]
        buttons.append({'title': title, 'payload': payload})
    return buttons