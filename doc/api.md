# api

[TOC]

## user

### 注册

uri: `/api/user`

method: `POST`

data:

| 参数          | 格式     | 备注          |
| ----------- | ------ | ----------- |
| action      | string | register，必须 |
| wx_userinfo | dict   | 微信用户信息      |
| userinfo    | dict   | 用户信息        |
| code        | string | wx.login得到  |

样例：

```javascript
wx.request({
    url: 'http://127.0.0.1:5000/auth/user',
    method: "POST",
    data: {
        action: 'register',
        code: res.code,
        wx_userinfo: user_res.userInfo,
        userinfo: { 'name': 'zhangsan1' }
    },
    success: function success(login_res) {
    console.log(login_res);
    }
}
```



#### userinfo详细

| 名称      | 类型     | 备注                                       |
| ------- | ------ | ---------------------------------------- |
| name    | string | 姓名                                       |
| phone   | string | 电话号码                                     |
| address | string | 地址                                       |
| company | string | 用户所在单位                                   |
| age     | int    | 年龄                                       |
| email   | string | 邮箱                                       |
| role    | string | 可选[normal, repair, admin], 默认为normal，普通注册时一般不需要传role |



### 用户信息修改

uri: `/api/user`

method: `POST`

data:

| 参数          | 格式     | 备注         |
| ----------- | ------ | ---------- |
| action      | string | update，必须  |
| wx_userinfo | dict   | 微信用户信息     |
| userinfo    | dict   | 用户信息       |
| code        | string | wx.login得到 |



### 登录

uri: `/api/login`

method: `POST`

data:

| 参数            | 类型     | 备注   |
| ------------- | ------ | ---- |
| code          | string |      |
| encryptedData | string |      |
| iv            | string |      |

样例：

```javascript
wx.request({
    url: 'http://127.0.0.1:5000/auth/login',
    method: "POST",
    data: {
        code: code,
        encryptedData: res.encryptedData,
        iv: res.iv
    },
    success: function success(login_res) {
    	console.log(login_res);
    }
}
```



###  获取当前用户

uri: `/api/user`

method: `GET`

data:

| 参数   | 格式     | 备注                             |
| ---- | ------ | ------------------------------ |
| view | string | get_curr_user_info,直接写在url中也可以 |



## 流程

### 创建并启动一个流程

uri: `api/process/instance`

method: `POST`

data:

| 名称           | 格式     | 备注                        |
| ------------ | ------ | ------------------------- |
| action       | string | 操作，[create]               |
| process_name | string | 要启动的流程名，报修申请为repair_apply |
| form         | dict   | 申请表单，具体字段见数据模型            |