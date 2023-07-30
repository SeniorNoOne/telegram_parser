ui_config = {
    'start_handler': {
        'msg': 'Please, choose an option',
        'error_msg': '',
        'ui': ('Set target words', 'Start parsing', 'Pause parsing', 'Delete parsed info'),
        'handlers': {
            'filters': None,
            'commands': 'start',
            'state': None,
        },
    },
    'cancel_handler': {
        'msg': 'Canceling. Going back to main menu',
        'error_msg': '',
        'ui': (),
        'handlers': {
            'filters': ('Cancel',),
            'commands': None,
            'state': '*',
        },
    },
    'get_target_words': {
        'msg': 'Please enter target words to parse (comma separated)',
        'error_msg': '',
        'ui': ('Cancel',),
        'handlers': {
            'filters': ('Set target words',),
            'commands': None,
            'state': None,
        },
    },
    'process_target_words': {
        'msg': 'Target words used in parsing:',
        'error_msg': 'Sorry, I cannot process ',
        'ui': ('Append new words', 'Replace existing words', 'Cancel'),
        'handlers': {
            'filters': None,
            'commands': None,
            'state': 'method_name',
        },
    },
    'modify_target_words': {
        'msg': 'Target words were modified:',
        'error_msg': '',
        'ui': (),
        'handlers': {
            'filters': ('Append new words', 'Replace existing words'),
            'commands': None,
            'state': 'method_name',
        },
    },
    'start_parsing': {
        'msg': 'Started parsing',
        'error_msg': 'Set target words before starting parsing process',
        'ui': (),
        'handlers': {
            'filters': ('Start parsing',),
            'commands': None,
            'state': None,
        },
    },
    'pause_parsing': {
        'msg': 'Paused parsing',
        'error_msg': 'Parsing process is already stopped',
        'ui': (),
        'handlers': {
            'filters': ('Pause parsing',),
            'commands': None,
            'state': None,
        },
    },
    'delete_parsed_info': {
        'msg': 'Parsed info has been deleted',
        'error_msg': 'There is no parse info',
        'ui': (),
        'handlers': {
            'filters': ('Delete parsed info',),
            'commands': None,
            'state': None,
        },
    },
}

db = {
    'user_table_name': 'user',
    'msg_table_name': 'msg',
}
