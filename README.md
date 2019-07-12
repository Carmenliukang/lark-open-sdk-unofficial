# lark open sdk unofficial

#1. 概要
##### 工作需要，将相关的接口写成 sdk 便于后期的开发与维护
开放平台链接如下:
https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM

#2. 使用方法：
   ####2.1 目录结构
  api 为 相关接口的封装类，因为接口的token 是有过期时间，所以每次 实例都 刷新token，
  如果code 返回 token 失效，那么就自动调用 fresh token api 再次 请求相关接口。
  