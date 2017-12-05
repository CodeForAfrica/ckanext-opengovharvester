import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.harvest.interfaces import IHarvester
import logging
from ckanext.harvest.harvesters.ckanharvester import CKANHarvester
import requests
import os
import json
import wget
import urlparse

log = logging.getLogger(__name__)

def download_resource_data(url):
    out_folder = '/tmp'
    parse_result = urlparse.urlparse(url)
    filename = os.path.basename(parse_result.path)
    file_path = '%s/%s'%(out_folder, filename)

    if not os.path.exists(file_path):
        download_path = wget.download(url, out=out_folder, bar=None)
        return download_path
    else:
        return file_path

class OpengovharvesterPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IHarvester, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'opengovharvester')
        log.info('Opengovharvester - CKAN Harvester with resource file download')
        self.ckan_harvester = CKANHarvester()
        self.config = config_

    def info(self):
        return {
            'title': 'Opengov Harvester',
            'name': 'opengovharvester',
            'description': 'CKAN Harvester with resource file download'
        }

    def get_package_dict(self, context, data_dict):
        return {}


    def gather_stage(self, harvest_job):
        '''
        Gather stage
        '''
        return self.ckan_harvester.gather_stage(harvest_job)

    def fetch_stage(self, harvest_obj):
        return True


    def import_stage(self, harvest_obj):
        '''
        Import stage

        Performs original CKAN's harverst import_stage task, downloads the associated resource files(into tmp folder)\
        and uploads to local CKAN instance via FileStore API then updates resource URLs of the harvested datasets.\
        The idea is to download the resource file from  Source instance and upload it to destination CKAN.
        '''
        import_result = self.ckan_harvester.import_stage(harvest_obj)

        try:
            content = json.loads(harvest_obj.content)
            resources = content.get('resources',[])
            if resources:
                for resource in resources:
                    current_url = resource.get('url', '')
                    if current_url:
                        log.info(current_url)
                        #Resource file download
                        tmp_resource_path = download_resource_data(current_url)

                        #Upload options to destination CKAN
                        #1. FileStore API - call filestore api to upload file(Auto upload to aws if configured)
                        #2. Upload to a server and provide a valid url path to file, TODO

                        #FileStore API
                        #Update resource 'url' to upload location
                        new_resource_url = self.upload_to_filestore(tmp_resource_path,\
                         resource.get('package_id'), resource.get('id'))

                    else:
                        raise Exception('Empty resource url')
        except Exception as e:
            raise

        return import_result


    def upload_to_filestore(self, file_path, package_id, resource_id):
        '''
        Returns new local resource URL
        '''
        filestore_api = '{}/api/action/resource_update'.format(self.config.get('ckan.site_url', 'http://0.0.0.0:5000'))
        file_name, file_ext = os.path.splitext(file_path)
        file_ext = file_ext.replace('.', '')
        ckan_api_key = self.ckan_harvester.config.get("ckan_api_key", '')
        if not ckan_api_key:
            raise Exception('CKAN API Key not found in harvester configuration')

        result = requests.post(filestore_api,
                      data={"package_id":package_id, "id":resource_id, 'format': file_ext},
                      headers={"Authorization": ckan_api_key},
                      files=[('upload', file(file_path))])
        try:
            api_response = json.loads(result.text)
            if api_response.get('success') == True:
                result = api_response.get('result')
                return result.get('url')

        except Exception as e:
            return resource_id
