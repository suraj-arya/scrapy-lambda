# -*- coding: utf-8 -*-

import types
import boto3
import json
import logging
from scrapy.exceptions import NotConfigured


class AWSLambdaPipelineException(Exception):
    pass


class AWSLambdaPipeline(object):

    DEFAULT_REGION = 'us-west-1'

    def __init__(self, settings):
        access_key = settings.get('AWS_ACCESS_KEY_ID')
        secret_key = settings.get('AWS_SECRET_ACCESS_KEY')
        region = settings.get('AWS_LAMBDA_REGION',
                              AWSLambdaPipeline.DEFAULT_REGION)
        function = settings.get('AWS_LAMBDA_FUNCTION_NAME')

        if None in (access_key, secret_key, function):
            raise NotConfigured

        self.function_name = function
        self.client = boto3.client('lambda',
                                   region_name=region,
                                   aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            try:
                res = self.client.invoke(FunctionName=self.function_name,
                                         InvocationType='Event',
                                         Payload=json.dumps(item))
                logging.debug('Invoked lambda function: {},'
                              ' response: {}'.format(self.function_name, res))
            except Exception as e:
                raise AWSLambdaPipelineException(e.message)

            return item
