package main

import (
    "github.com/gin-gonic/gin"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"log"
	"io"
	"strconv"
	"time"
	"os/exec"
	"golang.org/x/sync/errgroup"
)

type Report struct {
    Id  string `json:"id"`
    Bos_url string `json:"bos_url"`
    Report_url *string `json:"allure_report"`
}


var (
	g errgroup.Group
)

func main() {
    // gin.SetMode(gin.ReleaseMode)
    r := gin.Default()
    // 定义一个 POST 路由
    r.POST("/reportgenerator", func(c *gin.Context) {
        // 绑定 JSON 数据到 User 结构体
        var report Report
        if err := c.BindJSON(&report); err != nil {
            c.AbortWithStatusJSON(400, gin.H{"error": err.Error()})
            return
        }
        println("Id:", report.Id)
        println("Bos_url:", report.Bos_url)
        println("Report_url:", report.Report_url)
        if report.Report_url != nil {
        	response, err := http.Get(*report.Report_url)
        	if err == nil {
        		defer response.Body.Close()
        	}
	        if err != nil || (err == nil && response.StatusCode == 404) {
	            // 页面不存在
	            println("页面不存在")
	            {}
	        } else {
	            c.JSON(http.StatusOK, gin.H{"allure_report": report.Report_url})
	            return
	        }

	    }

	    // 定义常量
        REPORT_SOURCE_NAME := "/home/work/pts/pts_report.tar"
        SOURCE := "/home/work/pts/source/"
        REPORT := "/home/work/pts/report/"
        // REPORT_SOURCE_NAME := "pts_report.tar"
        // SOURCE := "/go/pts/source/"
        // REPORT := "/go/pts/report/"
        ALLURE := "/home/work/allure/bin/allure"
        REPORT_SERVER := "http://yq01-qianmo-com-255-137-11.yq01.baidu.com:8666/"


        // 打印用户信息
        println("Id:", report.Id)
        println("Bos_url:", report.Bos_url)
        println("Report_url:", report.Report_url)

        // 判断文件是否存在 并删除
        if _, err := os.Stat(REPORT_SOURCE_NAME); err == nil {
        	os.Remove(REPORT_SOURCE_NAME)
    	}

        // 下载请求
		response, err := http.Get(report.Bos_url)

	    if err != nil {
	        fmt.Println("Failed to download file:", err)
	        return
	    }
	    defer response.Body.Close()
	    file, err := os.Create(REPORT_SOURCE_NAME)
	    if err != nil {
	        fmt.Println("Failed to create file:", err)
	        return
	    }
	    defer file.Close()

	    _, err = io.Copy(file, response.Body)
	    if err != nil {
	        fmt.Println("Failed to save file:", err)
	        return
	    }

	    // 解压

	    filename := strconv.Itoa(rand.Intn(34)) + strconv.FormatInt(time.Now().Unix(), 10) + "_id_" + report.Id
    	fmt.Println(filename)
    	source_path := SOURCE + filename
    	report_path := REPORT + filename
    	fmt.Println(source_path)
    	// 创建文件夹
    	cmd := exec.Command("mkdir", "-p", source_path)
	    err = cmd.Run()
	    if err != nil {
	        fmt.Println("Failed to create directory:", err)
	        return
	    }

	    // 解压到指定位置
    	cmd = exec.Command("tar", "xf", REPORT_SOURCE_NAME, "-C", source_path, "--strip-components", "1")
	    err = cmd.Run()
	    if err != nil {
	    	println("tar failed:", err)
	        c.AbortWithError(http.StatusInternalServerError, err)
	        return
	    }

	    // allure
	    cmd = exec.Command(ALLURE, "generate", source_path, "-o", report_path, "--clean")
	    err = cmd.Run()
	    if err != nil {
	    	println("allure generate failed:", err)
	        c.AbortWithError(http.StatusInternalServerError, err)
	        return
	    }
	    report_url := REPORT_SERVER + filename
        // 返回响应
        c.JSON(200, gin.H{"allure_report": report_url})
        return
    })

    // 启动服务器
    s1 := &http.Server{
		Addr:           ":8801",
		Handler:        r,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	s2 := &http.Server{
		Addr:           ":8802",
		Handler:        r,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	s3 := &http.Server{
		Addr:           ":8803",
		Handler:        r,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	s4 := &http.Server{
		Addr:           ":8804",
		Handler:        r,
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	g.Go(func() error {
		return s1.ListenAndServe()
	})

	g.Go(func() error {
		return s2.ListenAndServe()
	})

	g.Go(func() error {
		return s3.ListenAndServe()
	})

	g.Go(func() error {
		return s4.ListenAndServe()
	})

	if err := g.Wait(); err != nil {
		log.Fatal(err)
	}
}

