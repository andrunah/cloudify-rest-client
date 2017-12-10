########
# Copyright (c) 2017 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
import urllib
import urlparse

import os
from functools import partial

from .. import bytes_stream_utils
from ..blueprints import BlueprintsClient
from . import wrapper


class ServiceTemplateClient(BlueprintsClient):

    def __init__(self, *args, **kwargs):
        super(ServiceTemplateClient, self).__init__(*args, **kwargs)
        self._uri_prefix = 'aria-service-templates'
        self._wrapper_cls = partial(wrapper.wrap, cls_name='ServiceTemplate')

    def _upload(self,
                csar_location,
                entity_id,
                application_file_name=None,
                private_resource=False,
                progress_callback=None):

        query_params = {'private_resource': private_resource}

        if application_file_name is not None:
            query_params['application_file_name'] = \
                urllib.quote(application_file_name)

        uri = '/{self._uri_prefix}/{id}'.format(
            self=self, id=entity_id)

        # For a Windows path (e.g. "C:\aaa\bbb.zip") scheme is the
        # drive letter and therefore the 2nd condition is present
        if urlparse.urlparse(csar_location).scheme and \
                not os.path.exists(csar_location):
            # archive location is URL
            query_params['service_template_csar_url'] = csar_location
            data = None
        else:
            # archive location is a system path - upload it in chunks
            data = bytes_stream_utils.request_data_file_stream_gen(
                csar_location, progress_callback=progress_callback)

        return self.api.put(uri,
                            params=query_params,
                            data=data,
                            expected_status_code=201)

    def publish_archive(self,
                        archive_location,
                        service_template_id,
                        **kwargs):
        return super(ServiceTemplateClient, self).publish_archive(
            archive_location=archive_location,
            blueprint_id=service_template_id,
            **kwargs
        )

    def upload(self,
               service_template_path,
               service_template_id,
               **kwargs):
        return super(ServiceTemplateClient, self).upload(
            service_template_path, service_template_id, **kwargs)
