sentry-s3-nodestorage
=====================

[Sentry](https://github.com/getsentry/sentry) extension implementing the
NodeStorage interface for [Amazon Simple Storage Service](https://aws.amazon.com/s3/)

# Installation

```bash
$ pip install sentry-s3-nodestore
```

# Configuration

```python
SENTRY_NODESTORE = 'sentry_s3_nodestore.backend.S3NodeStorage'
SENTRY_NODESTORE_OPTIONS = {
    'bucket_name': 'my-sentry-bucket',
    'region': 'us-west-1`, # Necessary for buckets outside US-Standard
    'aws_access_key_id': 'AKIAIJ....',
    'aws_secret_access_key': 'deadbeefdeadbeef....'
}
```
