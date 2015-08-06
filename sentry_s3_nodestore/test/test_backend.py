import unittest

import boto
from moto import mock_s3

from sentry_s3_nodestore.backend import S3NodeStorage


class S3NodeStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_s3 = mock_s3()
        self.mock_s3.start()

        conn = boto.connect_s3()
        conn.create_bucket('test')

        self.ns = S3NodeStorage(bucket_name='test')

    def tearDown(self):
        self.mock_s3.stop()

    def test_get(self):
        node_id = self.ns.create({'foo': 'bar'})
        self.assertIsNotNone(node_id)

        result = self.ns.get(node_id)
        self.assertEqual(result, {'foo': 'bar'})

    def test_get_multi(self):
        node_ids = [
            self.ns.create({'foo': 'bar'}),
            self.ns.create({'bar': 'baz'}),
        ]

        results = self.ns.get_multi(node_ids)

        self.assertEqual(results, {node_ids[0]: {'foo': 'bar'},
                                   node_ids[1]: {'bar': 'baz'}})

    def test_set(self):
        node_id = self.ns.create({'foo': 'bar'})
        self.ns.set(node_id, {'foo': 'baz'})
        result = self.ns.get(node_id)
        self.assertEqual(result, {'foo': 'baz'})

    def test_multi_set(self):
        node_ids = [
            self.ns.create({'foo': 'bar'}),
            self.ns.create({'bar': 'baz'}),
        ]

        self.ns.set_multi({
            node_ids[0]: {'bar': 'foo'},
            node_ids[1]: {'baz': 'bar'},
        })

        results = self.ns.get_multi(node_ids)

        self.assertEqual(results, {node_ids[0]: {'bar': 'foo'},
                                  node_ids[1]: {'baz': 'bar'}})

    def test_delete(self):
        node_id = self.ns.create({'foo': 'bar'})
        self.assertIsNotNone(node_id)
        self.ns.delete(node_id)

        result = self.ns.get(node_id)
        self.assertIsNone(result)

    def test_multi_delete(self):
        node_ids = [
            self.ns.create({'foo': 'bar'}),
            self.ns.create({'bar': 'baz'}),
            self.ns.create({'tar': 'czf'}),
        ]

        self.ns.delete_multi([node_ids[0], node_ids[2]])

        results = self.ns.get_multi(node_ids)

        self.assertEqual(results, {
            node_ids[0]: None,
            node_ids[1]: {'bar': 'baz'},
            node_ids[2]: None,
        })

if __name__ == '__main__':
    unittest.main()
