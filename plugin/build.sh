CLPATH=`pwd`/build
NAME="plug"
CGO_ENABLED=1 GOOS=windows GOARCH=386 go build -buildmode=c-archive -o $NAME.a
rm $CLPATH/*.lib
rm $CLPATH/*dll.a
rm $CLPATH/*.a
rm $CLPATH/*.exp
rm $CLPATH/*.h
mv $NAME.a $NAME.h $CLPATH
cd $CLPATH
bash exchange.sh