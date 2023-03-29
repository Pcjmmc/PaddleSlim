#!/usr/bin/env bash

mkdir output
cp -R ./backend ./output/
cp -R ./frontend ./output/

# build allure_service
cd allure_service
export GOENV=`pwd`/go.env
go get -u github.com/gin-gonic/gin
go get -u golang.org/x/sync/errgroup
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
go get -u gorm.io/gorm/schema
go build allure_service.go
cp allure_service ../output
cp nginx.conf ../output
