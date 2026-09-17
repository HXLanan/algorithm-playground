# -*- coding: utf-8 -*-
"""启动入口。

用法（在 algo-playground/ 目录下）：
    python run.py
或指定端口：
    set ALGO_PORT=9000 && python run.py
"""
from server import config
from server.app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 60)
    print("  Algo Playground · 趣味算法讲解合集")
    print("  浏览器打开： http://%s:%d/" % (config.HOST, config.PORT))
    print("  停止服务： Ctrl+C")
    print("=" * 60)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
