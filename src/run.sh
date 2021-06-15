#!/bin/bash

for i in *.js; do
  echo " - running $i"
  rhino $i
  if [ $? -ne 0 ]; then
    echo $i >> t
  fi
done

exit 0
