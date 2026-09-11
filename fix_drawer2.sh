#!/bin/bash
sed -i '/\/\//,/} else {/d' app/src/main/java/com/example/navigation/AppNavigation.kt
sed -i '/\/\//,/}/d' app/src/main/java/com/example/navigation/AppNavigation.kt
