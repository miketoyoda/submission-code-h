import os

import yaml

from enum import Enum, unique


@unique
class EConfigTag(Enum):
    EMAIL = 'email'
    GIST_URL = 'github_url'
    SOLUTION_LANGUAGE = 'solution_language'
    SUBMISSION_URL = 'submit_url'
    SECRET_SUFFIX = 'suffix'


@unique
class ESolutionLanguage(Enum):
    GO = 'golang'
    PYTHON = 'python'

    @classmethod
    def from_str(cls, input_str):
        return cls(input_str.lower())


def build_request_data(gist_url, email, lang):
    return {'github_url': gist_url,
            'contact_email': email,
            'solution_language': ESolutionLanguage.from_str(lang).value}


def check_mandatory_presence(data, tag):
    value = data[tag.value]
    assert value, f'{tag.value} is a mandatory field, check your configuration'
    return value


class Parameters(object):
    def __init__(self, email, gist_url, solution, submit_url, secret_suffix):
        self.email = email
        self.body = build_request_data(gist_url, email, solution)
        self.submission_url = submit_url
        self.shared_secret = email + secret_suffix

    @classmethod
    def from_env(cls, file_name='./config.yaml'):
        if not os.path.isfile(file_name):
            raise RuntimeError(f'{file_name} is not a valid file')

        with open(file_name) as f:
            config_data = yaml.safe_load(f)

            try:
                def check(tag): return check_mandatory_presence(config_data, tag)

                constructor_args = [check(e) for e in EConfigTag]
                return cls(*constructor_args)

            except (AssertionError, KeyError) as err:
                raise RuntimeError(f'file path: {file_name}') from err
