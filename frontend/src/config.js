/**
 * Created by liuhuanling on 2020/11/11.
 */

function getBaseUrl() {
  // return 'paddle-dev_api';
  // 开发环境
  if (process.env.NODE_ENV === 'development') {
    return 'http://127.0.0.1:8000';
  // 编译环境
  } else {
    // 测试环境
    let protocol = window.location.protocol;
    let host = window.location.host;
    return protocol + '//' + host;
  }
}

export const BASEURL = getBaseUrl();
