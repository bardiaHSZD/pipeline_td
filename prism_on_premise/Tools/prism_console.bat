@echo off
start "" "%~dp0/../Python311/python" -i -c "import sys;sys.path.append(\"%~dp0/../Scripts\");import PrismCore;pcore=PrismCore.create(prismArgs=[\"noUI\", \"loadProject\"])"