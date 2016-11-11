#!/bin/bash
cd ../../ && pytest &> /dev/null
if [ $? -ne 0 ]; then
    echo "This commit is rejected due to failing tests. Please fix them and try again."
    exit 1
fi

exit 0
