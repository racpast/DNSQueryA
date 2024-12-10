import sys
import requests
import json

# 默认值
domain = None
country = "JP"
limit = 10

# 帮助信息
def print_help():
    print("""
用法: DNSQueryA -d <domain> [-c <country>] [-l <limit>] [-h]

参数说明:
  -d, --domain      必选，指定域名
  -c, --country     可选，默认值为 'JP'
  -l, --limit       可选，默认值为 10，需为整数
  -h, --help        显示帮助信息
    """)
    sys.exit(0)

# 解析命令行参数
def parse_arguments():
    global domain, country, limit
    
    if len(sys.argv) < 2:
        print("错误: 必须提供 -d 或 --domain 参数。\n")
        print_help()

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("-d", "--domain"):
            if i + 1 < len(sys.argv):
                domain = sys.argv[i + 1]
                i += 1
            else:
                print("错误: -d 或 --domain 参数需要一个值。\n")
                print_help()
        elif arg in ("-c", "--country"):
            if i + 1 < len(sys.argv):
                country = sys.argv[i + 1]
                i += 1
        elif arg in ("-l", "--limit"):
            if i + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[i + 1])
                    i += 1
                except ValueError:
                    print("错误: -l 或 --limit 参数的值必须是整数。\n")
                    print_help()
            else:
                print("错误: -l 或 --limit 参数需要一个值。\n")
                print_help()
        elif arg in ("-h", "--help"):
            print_help()
        i += 1

    if domain is None:
        print("错误: 必须提供 -d 或 --domain 参数。\n")
        print_help()

# 发送POST请求并处理响应
def send_post_request():
    post_url = "https://api.globalping.io/v1/measurements"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    post_data = {
        "type": "dns",
        "target": domain,
        "locations": [{"country": country, "limit": limit}]
    }

    try:
        response = requests.post(post_url, headers=headers, json=post_data)
        response.raise_for_status()  # 如果响应码不是2xx，抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.stdout.write(f"请求错误: {e}\n")
        sys.exit(1)

# 发送GET请求并获取结果
def send_get_request(measurement_id):
    get_url = f"https://api.globalping.io/v1/measurements/{measurement_id}"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.stdout.write(f"请求错误: {e}\n")
        sys.exit(1)

# 处理响应数据并提取IP地址
def extract_ip_addresses(data):
    values = {answer.get("value") for result in data.get("results", []) for answer in result.get("result", {}).get("answers", [])}
    return list(values)

# 主程序
def main():
    parse_arguments()

    # 发送POST请求并获取measurement_id
    post_json = send_post_request()
    measurement_id = post_json.get("id")

    if measurement_id:
        # 发送GET请求获取详细数据
        data = send_get_request(measurement_id)
        
        # 提取去重后的IP地址
        ip_list = extract_ip_addresses(data)

        # 输出结果
        sys.stdout.write(json.dumps(ip_list))
    else:
        sys.stdout.write("错误: 'id' 未在POST响应中找到。\n")
        sys.exit(1)

if __name__ == "__main__":
    main()