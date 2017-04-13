Flask-Demo
==========

测试服运行::

    python manage.py [-c demo.config.YourConfig] runsert -p 8080

正式服可以使用uwsgi

fabric的配置参考 `dansimau/flask-bootstrap <https://github.com/dansimau/flask-bootstrap>`_

- `A Better Pip Workflow <http://www.kennethreitz.org/essays/a-better-pip-workflow>`_

- password的保存

- @hybrid_property的使用

- overholt_

只保留最新的N个tag::

    ./tags.sh

secret_key生成方式::

    In [1]: import os
    In [2]: os.urandom(10)
    Out[2]: '\xd4m1<w\x15\xe2?\x1e\xe3'

celery
------

- deploy celery via flask-fabric_.

.. _overholt: https://github.com/mattupstate/overholt
.. _flask-fabric: https://github.com/codeif/flask-fabric
