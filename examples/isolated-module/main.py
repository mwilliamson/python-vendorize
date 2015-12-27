#!/usr/bin/env python

from _vendor import six

for key, value in six.iteritems({"one": 1}):
    print((key, value))
