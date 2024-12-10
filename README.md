# 🔍️ DNSQueryA

<div align="center">
    <img height="78" src="/globalping.png">
    <img height="78" src="/jsdelivr.png">
</div>

## 📚️ 一个基于 Globalping API 实现的、根据所传入的域名、国家以及上限获取并以 Json 格式输出给定域名的A记录的程序。
### ✍🏻 用法
```
DNSQueryA -d <domain> [-c <country>] [-l <limit>] [-h]

参数说明:
  -d, --domain      必选，指定域名
  -c, --country     可选，默认值为 'JP'
  -l, --limit       可选，默认值为 10，需为整数
  -h, --help        显示帮助信息
```
### 🌰 示例
**1、输入 `DNSQueryA.exe -d nyaa.si` ，输出 `["186.2.163.20"]`**

**2、输入 `DNSQueryA -d pixiv.net -c JP -l 20` ，输出 `["210.140.139.155", "210.140.139.158", "210.140.139.161"]`**
### 🌏 相关链接
**📖 [Globalping API 文档](https://globalping.io/docs/api.globalping.io)**

**🧪 [Globalping API Demo](https://api.globalping.io/demo/)**

**🛠️ [JSON在线解析格式化验证 - JSON.cn](https://www.json.cn/)**
