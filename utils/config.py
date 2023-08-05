ui_config = {
    'start_handler': {
        'msg': ('Please, choose an option', '', ''),
        'ui': ('Set target words', 'Start parsing', 'Pause parsing', 'Delete parsed info'),
        'extras': (),
        'handlers': {
            'filters': None,
            'commands': 'start',
            'state': None,
        },
    },
    'cancel_handler': {
        'msg': ('Canceling. Going back to main menu', '', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Cancel',),
            'commands': None,
            'state': '*',
        },
    },
    'get_target_words': {
        'msg': ('Please enter target words to parse (comma separated)', '',
                'Current target words:'),
        'ui': ('Cancel',),
        'extras': (),
        'handlers': {
            'filters': ('Set target words',),
            'commands': None,
            'state': None,
        },
    },
    'process_target_words': {
        'msg': ('Target words used in parsing:', 'Sorry, I cannot process ', ''),
        'ui': ('Append new words', 'Replace existing words', 'Cancel'),
        'extras': (),
        'handlers': {
            'filters': None,
            'commands': None,
            'state': 'method_name',
        },
    },
    'modify_target_words': {
        'msg': ('Target words were modified:', '', ''),
        'ui': (),
        'extras': ('Append new words', 'Replace existing words'),
        'handlers': {
            'filters': ('Append new words', 'Replace existing words'),
            'commands': None,
            'state': 'method_name',
        },
    },
    'start_parsing': {
        'msg': ('Started parsing', 'Set target words before starting parsing process', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Start parsing',),
            'commands': None,
            'state': None,
        },
    },
    'pause_parsing': {
        'msg': ('Paused parsing', 'Parsing process is already stopped', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Pause parsing',),
            'commands': None,
            'state': None,
        },
    },
    'delete_parsed_info': {
        'msg': ('Parsed info has been deleted', 'There is no parse info', ''),
        'ui': (),
        'extras': (),
        'handlers': {
            'filters': ('Delete parsed info',),
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
