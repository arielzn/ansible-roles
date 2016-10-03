from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        itemDefault = {
            'options': None,
            'when':    True,
            'dir':
                (variables['deploy_helper']['new_release_path'])
                    if variables.has_key('deploy_helper') else
                (variables['manala_deploy_dir'] + '/' +  variables['manala_deploy_current_dir']),
            'shared_dir':
                (variables['deploy_helper']['shared_path'])
                    if variables.has_key('deploy_helper') else
                (variables['manala_deploy_dir'] + '/' +  variables['manala_deploy_shared_dir'])
        }

        for term in self._flatten(terms):

            items = []

            # Task as a single line
            if isinstance(term, basestring):
                item = itemDefault.copy()
                item.update({
                    'task': term
                })
                items.append(item)
            else:
                # Guess task (first one not in blacklist)
                item = None
                for termKey, termValue in term.items():
                    if termKey not in ['when']:
                        item = itemDefault.copy()
                        item.update({
                            'task':    termKey,
                            'options': termValue
                        })
                        break
                if item:
                    item.update({
                        'when': term.get('when') if term.has_key('when') else True
                    })
                    items.append(item)

            # Merge
            for item in items:
                results.append(item)

        return results
