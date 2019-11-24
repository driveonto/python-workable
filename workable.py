import requests
import os.path
import json


class Error(Exception):
    pass


class Workable(object):
    api_url = 'https://www.workable.com/spi/v3/accounts/'

    def __init__(self, token=None, subdomain=None):
        if token is None:
            token = self.read_token()
        if token is None:
            raise Error('You must provide a Workable API token')
        self.token = token
        if subdomain is None:
            subdomain = self.read_subdomain()
        self.acounts = Accounts(self)
        self.members = Members(self, subdomain, 'members')
        self.recruiters = Recruiters(self, subdomain, 'recruiters')
        self.stages = Stages(self, subdomain, 'stages')
        self.jobs = Jobs(self, subdomain, 'jobs')

    def read_token(self):
        token = None
        if 'WORKABLE_TOKEN' in os.environ:
            token = os.environ['WORKABLE_TOKEN']
        if token is None:
            paths = [os.path.expanduser('~/.workable.key'), '/etc/workable.key']
            for path in paths:
                try:
                    f = open(path, 'r')
                    token = f.read().strip()
                    f.close()
                    if token != '':
                        return token
                except:
                    pass
            return None
        return token

    def read_subdomain(self):
        subdomain = None
        if 'WORKABLE_SUBDOMAIN' in os.environ:
            subdomain = os.environ['WORKABLE_SUBDOMAIN']
        return subdomain

    def request(self, url):
        headers = {
            'content-type': 'application/json',
            'user-agent': 'Python-Workable/0.0.5',
            'authorization': 'Bearer ' + self.token
        }
        request = requests.get('%s%s' % (self.api_url, url), headers=headers)
        return request.json()


class WorkableSectionMixin(object):
    def __init__(self, workable, url=None):
        self.workable = workable

    def all(self):
        return self.workable.request('%s' % (self.url))


class WorkableSectionWithSubdomainMixin(WorkableSectionMixin):
    def __init__(self, workable, subdomain=None, url=None):
        super().__init__(workable)
        if subdomain is None:
            raise Error("You must provide the account's subdomain")
        self.subdomain = subdomain
        if url is None:
            raise Error("You must provide a url")
        self.url = url

    def all(self):
        result = self.workable.request('%s/%s' % (self.subdomain, self.url))
        return result[self.url]


class Accounts(WorkableSectionMixin):
    pass


class Members(WorkableSectionWithSubdomainMixin):
    pass


class Recruiters(WorkableSectionWithSubdomainMixin):
    pass


class Stages(WorkableSectionWithSubdomainMixin):
    pass


class Jobs(WorkableSectionWithSubdomainMixin):
    def job(self, shortcode):
        return self.nested_request(shortcode)

    def job_questions(self, shortcode):
        return self.nested_request(shortcode, 'questions')

    def job_members(self, shortcode):
        return self.nested_request(shortcode, 'members')

    def job_recruiters(self, shortcode):
        return self.nested_request(shortcode, 'recruiters')

    def job_candidates(self, shortcode):
        return self.nested_request(shortcode, 'candidates')

    def nested_request(self, shortcode=None, nested_url=""):
        if shortcode is None:
            raise Error("You must provide job's shortcode")
        result = self.workable.request('%s/%s/%s/%s' % (self.subdomain, self.url, shortcode, nested_url))
        return result
