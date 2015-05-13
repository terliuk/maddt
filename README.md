
maddt - MAdison Desy Data Transfer
========================================

Dedicated software to solve the problem of
automation of large scale data-transfer via 
gsiftp.

The software is especially designed to copy data between 
UW Madison and DESY, Zeuthen and thus features specifics for those infrastructures.

However, it is designed in a flexible way and thus might be adapted to other needs

Features
---------

* queries a database for files to copy
* copies the files with globus-url-copy
* performs md5sum sanity check of copied files, optimized 
  for SGE clusters
* logs the process
* Simple webpage provides information about the amount
  of copied files

Requirements
--------------

* access to grid-tools, grid-certificate etc..
* python, python-django,...






 






