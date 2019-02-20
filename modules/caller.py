import logging
import datetime
import threading

from modules import conversation
from modules.actions import executors
from modules.settings import INTENT_CONFIDENCE_THRESHOLD, CONTEXT_PERSISTENCE_SECONDS

context_dict = {}

lock = threading.Lock()


def run_action_from_parsed_message(parsed_message, chat_id):

    intent_confidence = parsed_message.get('intent').get('confidence')
    intent_name = parsed_message.get('intent').get('name')

    entities = parsed_message.get('entities')

    if intent_confidence < INTENT_CONFIDENCE_THRESHOLD:
        intent_name = None

    context = get_context(chat_id)

    return executors.execute_action_from_intent_name(intent_name, entities, context)


def get_context(chat_id):

    lock.acquire()

    check_timestamps()

    # conversation was already defined
    if context_dict.get(chat_id):

        update_timestamp(chat_id)
        context = context_dict[chat_id]['context']

    else:

        context = conversation.Context(chat_id)
        context_dict[chat_id] = {'context': context}
        update_timestamp(chat_id)

        # schedule_delete_event(chat_id)

    lock.release()

    return context


def check_timestamps():

    max_age = datetime.datetime.now() - datetime.timedelta(CONTEXT_PERSISTENCE_SECONDS)

    for k, v in list(context_dict.items()):
        if v['timestamp'] < max_age:
            del context_dict[k]


def update_timestamp(chat_id):
    context_dict[chat_id]['timestamp'] = datetime.datetime.now()
