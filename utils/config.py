ui_config = {
    'start_handler': {
        'msg': ('Please, choose an option', ''),
        'ui': ('Target words', 'Start parsing', 'Pause parsing', 'Show parsed posts',
               'Delete parsed posts'),
        'extras': (),
        'handlers': {
            'filters': None,
            'commands': 'start',
            'state': None,
        },
    },
    'cancel_handler': {
        'msg': ('Canceling. Going back to main menu', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Cancel',),
            'commands': None,
            'state': '*',
        },
    },
    'target_words_menu': {
        'msg': ('Please, choose an operation for target words', 'Current target words: '),
        'ui': ('Add words', 'Clear words', 'Cancel'),
        'extras': (),
        'handlers': {
            'filters': ('Target words',),
            'commands': None,
            'state': None,
        },
    },
    'get_target_words': {
        'msg': ('Please enter target words to parse (comma separated)', 'Current target words: '),
        'ui': ('Cancel',),
        'extras': (),
        'handlers': {
            'filters': ('Add words',),
            'commands': None,
            'state': None,
        },
    },
    'process_target_words': {
        'msg': ('Target words used in parsing:', 'Wrong target words input'),
        'ui': ('Append new words', 'Cancel'),
        'extras': (),
        'handlers': {
            'filters': None,
            'commands': None,
            'state': 'method_name',
        },
    },
    'modify_target_words': {
        'msg': ('Target words were modified: ', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Append new words', 'Replace existing words'),
            'commands': None,
            'state': 'method_name',
        },
    },
    'clear_target_words': {
        'msg': ('Target words are cleared', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Clear words',),
            'commands': None,
            'state': None,
        },
    },
    'start_parsing': {
        'msg': ('Started parsing', 'Set target words before starting parsing process'),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Start parsing',),
            'commands': None,
            'state': None,
        },
    },
    'pause_parsing': {
        'msg': ('Paused parsing', 'Parsing process is already stopped'),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Pause parsing',),
            'commands': None,
            'state': None,
        },
    },
    'show_parsed_posts': {
        'msg': ('Parsed posts:\n\n', 'There are no parsed posts'),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Show parsed posts',),
            'commands': None,
            'state': None,
        },
    },
    'delete_parsed_posts': {
        'msg': ('Parsed posts has been deleted', 'There are no parsed posts'),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Delete parsed posts',),
            'commands': None,
            'state': None,
        },
    },
}

db_config = {
    'db_name': 'heli_parser',
    'user_table_name': 'user',
    'parsed_data_table_name': 'post',
}
