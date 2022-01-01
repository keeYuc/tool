CLPATH=`pwd`/exchange
CGO_ENABLED=1 GOOS=windows GOARCH=386 go build -buildmode=c-archive -o plug.a *.go
rm $CLPATH/*.lib
rm $CLPATH/*dll.a
rm $CLPATH/*.a
rm $CLPATH/*.exp
rm $CLPATH/*.h
mv plug.a plug.h $CLPATH
cd $CLPATH
bash exchange.sh