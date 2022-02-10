@echo off

SET APP=<path_to_app>
SET TESTS=<path_to_tests>

SET MYPYPATH="%MYPYPATH%;%APP%;%TESTS%;"
SET PYTHONPATH="%PYTHONPATH%;%APP%;%TESTS%;"