DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
rm -rf libs/*

while read p; do
  ln -s $DIR/dev/lib/python2.7/site-packages/$p $DIR/libs/$p
done < libs.txt
