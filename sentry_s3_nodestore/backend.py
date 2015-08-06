"""
sentry_s3_nodestore.backend
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Ernest W. Durbin III.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import json
from time import sleep

import boto

from sentry.nodestore.base import NodeStorage


def retry(attempts, func, *args, **kwargs):
    for _ in range(attempts):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            sleep(0.1)
            raise
    raise

def connect_s3(bucket_name, region=None, validate=False):
    if region is None:
        conn = boto.connect_s3()
    else:
        conn = boto.s3.connect_to_region(region)
    return conn.get_bucket(bucket_name, validate=validate)


class S3NodeStorage(NodeStorage):

    def __init__(self, bucket_name, region=None, max_retries=3):
        self.max_retries = max_retries
        self.bucket = connect_s3(bucket_name, region=region)

    def _put(self, node_id, data):
        key = boto.s3.key.Key(self.bucket)
        key.key = node_id
        retry(self.max_retries, key.set_contents_from_string, *(data,))
        return node_id

    def delete(self, id):
        """
        >>> nodestore.delete('key1')
        """
        self.bucket.delete_key(id)

    def delete_multi(self, id_list):
        """
        Delete multiple nodes.

        Note: This is not guaranteed to be atomic and may result in a partial
        delete.

        >>> delete_multi(['key1', 'key2'])
        """
        self.bucket.delete_keys(id_list)

    def get(self, id):
        """
        >>> data = nodestore.get('key1')
        >>> print data
        """
        key = self.bucket.get_key(id)
        if key is None:
            return None
        result = retry(self.max_retries, key.get_contents_as_string)
        return json.loads(result)

    def get_multi(self, id_list):
        """
        >>> data_map = nodestore.get_multi(['key1', 'key2')
        >>> print 'key1', data_map['key1']
        >>> print 'key2', data_map['key2']
        """
        return dict(
            (id, self.get(id))
            for id in id_list
        )

    def create(self, data):
        """
        >>> nodestore.create({'foo': 'bar'})
        """
        node_id = self.generate_id()
        self._put(node_id, json.dumps(data))
        return node_id

    def set(self, id, data):
        """
        >>> nodestore.set('key1', {'foo': 'bar'})
        """
        self._put(id, json.dumps(data))

    def set_multi(self, values):
        """
        >>> nodestore.set_multi({
        >>>     'key1': {'foo': 'bar'},
        >>>     'key2': {'foo': 'baz'},
        >>> })
        """
        for id, data in values.iteritems():
            self.set(id=id, data=data)

    def cleanup(self, cutoff_timestamp):
        raise NotImplementedError
