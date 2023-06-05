/**
 * Created by liuhuanling on 2017/11/18.
 */

import axios from 'axios';
import qs from 'qs';
import router from '../routes';
import {Message, LoadingBar} from 'iview';
import {BASEURL} from '../config.js';

// 请求时拦截器
axios.interceptors.request.use(
  config => {
    LoadingBar.start();
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 请求后的拦截器
axios.interceptors.response.use(
  response => response,
  error => Promise.resolve(error.response)
);

// 检查http状态
function checkStatus(response) {
  if (response && (response.status === 200 || response.status === 304)) {
    LoadingBar.finish();
    return response.data;
  } else if (response && (response.status === 301)) {
    // 请求重定向到请求todo
    console.log('发生了重定向');
    console.log(response.headers.Location);
  } else {
    LoadingBar.error();
    return {
      data: {
        status: 404,
        msg: response.statusText,
        data: response.statusText
      }
    };
  }
}

// 检查数据中自定义的数据状态
function checkDataStatus(res) {
  if (parseInt(res.code, 10) === 200) { // 200 正常返回数据
    return res;
  } else if (parseInt(res.code, 10) === 4001) { // 300 重定向到登录界面
    Message.destroy();
    let new_url = res.message;
    window.location.href = new_url;
  } else if (parseInt(res.code, 10) === 403) { // 403 跳转到权限页面
    Message.destroy();
    Message.warning({
      content: '您没有此权限，请先开通权限',
      duration: 30,
      closable: true
    });
  } else { // 其他错误返回，以后处理
    return res;
  }
}

// 封装请求
export default {
  post(url, data) {
    return axios({
      method: 'post',
      url: BASEURL + url,
      data: url.startsWith('/models_benchmark') ? JSON.stringify(data) : qs.stringify(data),
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'originUrl': window.location.href
      }
    }).then(checkStatus).then(checkDataStatus);
  },
  delete(url, data) {
    return axios({
      method: 'delete',
      url: BASEURL + url,
      data: qs.stringify(data),
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'originUrl': window.location.href
      }
    }).then(checkStatus).then(checkDataStatus);
  },
  put(url, data) {
    return axios({
      method: 'put',
      url: BASEURL + url,
      data: qs.stringify(data),
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'originUrl': window.location.href
      }
    }).then(checkStatus).then(checkDataStatus);
  },
  get(url, params) {
    // console.log(BASEURL + url);
    return axios({
      method: 'get',
      url: BASEURL + url,
      params,
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'originUrl': window.location.href
      }
    }).then(checkStatus).then(checkDataStatus);
  },
  postFile(url, formData) {
    return axios({
      method: 'POST',
      url: BASEURL + url,
      data: formData,
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'multipart/form-data;',
        'originUrl': window.location.href
      }
    }).then(checkStatus).then(checkDataStatus);
  },
  postExcel(url, data) {
    return axios({
      method: 'post',
      url: BASEURL + url,
      data: url.startsWith('/models_benchmark') ? JSON.stringify(data) : qs.stringify(data),
      timeout: 30000,
      responseType: 'arraybuffer'
    }).then(response => {
      if (response && (response.status === 200 || response.status === 304)) {
        LoadingBar.finish();
        return {
          data: response,
          status: response.status
        };
      } else if (response && (response.status === 301)) {
        // 请求重定向到请求todo
        console.log('发生了重定向');
        console.log(response.headers.Location);
      } else {
        LoadingBar.error();
        return {
          data: {
            status: 404,
            msg: response.statusText,
            data: response.statusText
          }
        };
      }
    }
    );
  }
};
