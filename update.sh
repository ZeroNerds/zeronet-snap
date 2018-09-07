#!/bin/sh

op="$PWD"

git pull

cd "$HOME/ZeroNet"

git pull

#lver=$(git tag | sort | tail -n 1)
lver=$(cat src/Config.py | grep "^[ ]*self.version" | grep "[0-9]*\.[0-9]*\.[0-9]*" -o)

lat=$(git log --grep="Rev[0-9]*" --format="[%H] = %s" | head -n 1)
lc=$(echo "$lat" | grep "\[[a-z0-9A-Z]*\]" -o | grep "[a-z0-9A-Z]*" -o)
lrev=$(echo "$lat" | grep "Rev[0-9]*" -o)
echo "commit = $lc / rev = $lrev / ver = $lver"

v1=$(echo "$lver")
v2=$(echo "$lrev" | sed "s/Rev/r/g")
v="$v1-$v2"

cd "$op/snap"

pre=$(echo $(cat snapcraft.yaml | grep "^version: " | grep " [0-9a-z.-]*" -o))

if [ "$pre" != "$v" ]; then
  echo "Update... ($pre => $v)"
  set -x
  sed "s/^version: .*$/version: $v/" -i snapcraft.yaml
  sed "s/source-commit: .*/source-commit: $lc/" -i snapcraft.yaml
  git commit -m "$lrev" snapcraft.yaml
else
  echo "Up-to-date! ($v)"
fi

git gc --aggressive
