#!/usr/bin/env bash

mkdir output
cp -R ./backend ./output/
cp -R ./frontend ./output/


# build allure_service
cd allure_service
go get -u github.com/gin-gonic/gin
go get -u golang.org/x/sync/errgroup
go build allure_service.go
cp allure_service ../output
