CGO_ENABLED=1 GOOS=windows GOARCH=386 go build -buildmode=c-archive -o main.a main.go
#CGO_ENABLED=1 GOOS=windows GOARCH=386 go build -buildmode=c-shared -o main.dll main.go
#CGO_ENABLED=1 GOOS=windows GOARCH=amd64 go build -buildmode=c-shared -o main.a main.go
