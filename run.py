#!/usr/bin/env python

from typo import create_app

app = create_app('config.local.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)