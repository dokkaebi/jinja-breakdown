Description
===========

Breakdown is a lightweight python webserver that parses jinja2 templates.  It's intended to be used by designers for doing rapid prototyping.


Basic Usage
===========

Breakdown needs a ``templates`` directory and a ``static`` directory to serve from.  If your working directory contains these, you can simply run breakdown with no arguments::

    $ breakdown

Or, you can specify the path to a directory containing ``templates`` and ``static``::

    $ breakdown /path/to/project

Breakdown will also work with a django project structure.  If the project path contains an ``apps`` directory, breakdown will automatically detect this and combine the ``static`` and ``templates`` directories for each django app.  You'll also get a listing of the directories it found.  Here's the output of running breakdown on a django project with two apps: 'mainsite' and 'blog'::

    $ breakdown ~/django/myproject
    Serving templates from:
      /Users/josh/django/myproject/apps/blog/templates
      /Users/josh/django/myproject/apps/mainsite/templates

    Serving static data from:
      /Users/josh/django/myproject/apps/blog/static
      /Users/josh/django/myproject/apps/mainsite/static

Template Context Objects
------------------------

You can define values for template variables by supplying a json dictionary for each page.

When loading a template, breakdown will attempt to load a json dictionary of the same name from the context directory (``context`` by default) and add it to the page context. For example, when loading ``blog/article_detail.html`` breakdown will look for ``<project root>/context/blog/article_detail.json``.  

For all pages, breakdown also attempts to load ``<project root>/context/base.json``.  Any values defined here will be available on all pages, and will be overridden by any of the same name defined in individual page context objects.

For example, if we define ``base.json`` like this::

    {
     "request": {
        "user": {
             "name":"Austin",
             "member": "Member #4812"
         }
     },
     "object": {
        "id": 555,
        "title": "Excellent Blog Post"
     }
    }

then ``request`` and ``object`` become available to all templates, and ``{{request.user.name}}`` yields ``Austin``.

You can specify a function by adding a key with trailing parentheses::

    {
     "request": {
        "user": {
             "name":"Austin",
             "is_authenticated()": true,
             "birth_year()": 1982,
             "middle_name()": "David",
             "member": "Member #4812"
         }
     }
    }

The trailing parentheses are removed, and now ``{{request.user.is_authenticated()}}`` returns ``True``.  Functions defined in this way ignore any arguments and return the value specified in the json dictionary. ``{{request.user.is_authenticated(arg1, arg2, arg3)}}`` also returns ``True``. However, these functions cannot be used without parentheses and ``{{request.user.is_authenticated}}`` prints something like ``at 0x101f32f50>``.

If you define a ``__unicode__`` or ``__unicode__()`` key, its value will be used when referencing its enclosing object directly.  With a context object such as either::

    {
      "request": {
        "user": {
             "name":"Austin",
             "__unicode__": "User named Austin"
         }
     }
    }

or::

    {
      "request": {
        "user": {
             "name":"Austin",
             "__unicode__()": "User named Austin"
         }
     }
    }

referencing ``{{request.user}}`` will yield ``User named Austin``.

Breakdown does not support full context object inheritance, but top-level values defined for individual pages override those defined in ``base.json``.  If you define ``<project root>/context/blog/article_detail.json`` like this::

    {
      "blog": {
        "title": "Skiing Blog"
      },
      "request": {
        "user": {
          "name": "Josh"
        }
      }
    }

then in ``/blog/article_detail.html`` a reference to ``{{request.user.name}}`` will print ``Josh``, ``{{request.user.birth_year}}`` is blank, and ``{{request.user}}`` yields ``{u'name': u'Josh'}``.


Viewing Templates
-----------------

Once breakdown is running, it will print the local URL the webserver is listening on::

    Server running at http://127.0.0.1:5000 ...

You can now view templates in your browser by navigating to http://127.0.0.1:5000.  However, you won't see anything here unless one of your template directories contains a file named ``index.html``.  The URL of any template (besides ``index.html``) will be identical to its filename, with all relative paths preserved.  Below is an example of template filenames and their corresponding URL on the local server:

==================== ====================================
**Template**         **URL**
-------------------- ------------------------------------
index.html           http://127.0.0.1:5000/
article.html         http://127.0.0.1:5000/article
blog/index.html      http://127.0.0.1:5000/blog
blog/post.html       http://127.0.0.1:5000/blog/post
==================== ====================================

*Note: The server will accept template URLs with or without .html appended to them*

Additional Features
===================

Template tags
-------------

For convenience, A few template functions have been added to the `jinja2 template API <http://jinja.pocoo.org/docs/templates/>`_:

################
{{ greeking() }}
################

Generates a block of randomized lorem ipsum text marked-up with various HTML elements: ``<em>``, ``<strong>``, ``<code>``, ``<a>``, ``<ol>``, and ``<ul>``.

##########################
{{ image(width, height) }}
##########################

If you have `PIL <http://www.pythonware.com/products/pil/>`_ installed, you can use this function to generate an ``<img>`` tag with a sample image of the specified size (without PIL, the width/height are ignored and you get a large sample image)

#############################
{{ url(\*args, \*\*kwargs) }}
#############################

Ignores all arguments and returns ``'#'``.

CleverCSS
---------

Breakdown also supports automatic `CleverCSS <http://http://sandbox.pocoo.org/clevercss/>`_ parsing.  If the file ``foo.css`` is requested and not found, breakdown will then look for a matching ``foo.clevercss`` and compile it to vanilla css on the fly.

    
Advanced
========

**Command line options**:
  -h, --help                        show this help message and exit
  -p PORT, --port=PORT              run server on an alternate port (default is 5000)
  -m, --media                       treat MEDIA_URL as STATIC_URL in templates
  -v, --version                     display the version number and exit
  -c DIR, --context_dir_name=DIR    set the directory name for context object files (default is ``context``)

