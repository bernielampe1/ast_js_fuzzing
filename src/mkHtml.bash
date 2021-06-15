#!/bin/bash

function echoDoc() {
echo "<html>
<script src=\"$1\"></script>
<body>
<div id=\"DONE\"> ***** NOT DONE ***** </div>
</body>
<!-- rewrite the message to indicate that it ran  -->
<script>e = document.getElementById(\"DONE\"); e.innerHTML = \"DONE!!!!!\";</script>
</html>"
}

for i in $*; do
  echoDoc $i
done

exit 0 
