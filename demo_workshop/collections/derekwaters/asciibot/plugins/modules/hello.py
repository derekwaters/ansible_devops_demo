#!/usr/bin/python

DOCUMENTATION = r'''
---
module: hello
short_description: Say hello, in a pretty way
description:
    - Say hello to someone in a pretty fashion
version_added: "1.0.0"
options:
    account_name:
        description: A username to greet
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Say hello to Joe
  derekwaters.asciibot.hello:
    account_name: Joe
'''

RETURN = r'''
greeting:
    description: The pretty greeting message
    type: str
    returned: always
'''

from art import text2art
from ansible.module_utils.basic import AnsibleModule

def main():
    module_args = dict(
        account_name = dict(type = 'str', required = True)
    )
    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    name = module.params['account_name']

    msg = text2art("Hi " + name)

    module.exit_json(greeting=msg)

if __name__ == '__main__':
    main()