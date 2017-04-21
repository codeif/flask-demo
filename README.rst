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

使用过程
--------

- clone

  .. code-block::

    git clone https://github.com/codeif/flask-demo.git

- 删除目录

  .. code-block::
  
    rm -rf .git .gitmodules fabfile

- 使用pycharm重构 demo -> <your name>

- 替换文件内容

  - Linux

    .. code-block::
    
      find . -not -path '*/\.*' -type f -exec sed -i 's/demo/<new name>/g; s/DEMO/<NEW NAME>/g' {} \;

  - macOS

    .. code-block::
    
      find . -not -path '*/\.*' -type f -exec sed -i '' 's/demo/<new name>/g; s/DEMO/<NEW NAME>/g' {} \;

- 使用git管理

  .. code-block::

    git init
    git submodule add https://github.com/codeif/flask-fabric.git fabfile

.. _overholt: https://github.com/mattupstate/overholt
.. _flask-fabric: https://github.com/codeif/flask-fabric
