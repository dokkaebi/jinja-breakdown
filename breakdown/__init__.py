""" 
Breakdown.py - 2011 Concentric Sky

Lightweight jinja2 template prototyping server with support for
some custom template tags

Copyright 2011 Concentric Sky, Inc. 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

VERSION = (1, 0, 6)

def pkg_path(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


# Default settings
ADDR = ''
PORT = 5000
STATIC_URL = '/static/'
BASE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
}
