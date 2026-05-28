# SQL 注入漏洞复现与防御分析

## 📌 项目简介
本项目独立搭建了一个基于 Python 的 SQL 注入模拟靶场，用于演示 **SQL 注入攻击的原理、利用过程以及最有效的防御方案——参数化查询**。  
项目通过 Docker 容器化部署，能够一键启动测试环境，并配合 Burp Suite、Wireshark 完成全流程的“攻击→抓包→防御对比”实验。

## 🛠 环境要求
- Python 3.8+
- Flask（`pip install flask`）
- Docker 20.10+（可选，用于容器化部署）
- Burp Suite / Wireshark（用于分析和验证）

## 🚀 快速开始
1. 克隆本仓库：
   ```bash
   git clone https://github.com/Leo-ctrl-ak/sql-injection-lab.git
   cd sql-injection-lab
2. 直接运行有漏洞的版本：
   pip install flask
   python app.py
或使用 Docker：
   docker build -t sqli-lab .
   docker run -d -p 8081:8081 --name sqli-lab sqli-lab
3.访问 http://localhost:8081 开始测试。
🧪漏洞复现步骤
正常登录
预设账号 admin / password，正常登录成功。

SQL 注入绕过
用户名输入 ' OR '1'='1，密码随意，点击登录。成功绕过验证，获取所有用户数据。

https://screenshots/01-injection-success.png

Wireshark 流量分析
使用 Wireshark 过滤 tcp.port == 8081，可看到恶意 payload 被明文发送。

https://screenshots/02-wireshark-capture.png

🛡️ 防御方案：参数化查询
原理
原始代码使用字符串拼接构造 SQL，导致输入中的 ' 破坏语法。
防御版本 app_fixed.py 采用参数化查询，将用户输入作为参数绑定，从根本上杜绝注入。

运行防御版本
python app_fixed.py
再次使用 payload ' OR '1'='1，注入失败，返回 “Login failed”。
https://screenshots/03-defense-fail.png

📝 个人收获
理解了 SQL 注入的成因：代码与数据未分离。

学会使用 Docker 快速搭建安全测试环境。

结合 Wireshark 分析攻击流量，提升网络分析能力。

实践参数化查询修复漏洞，形成“发现→分析→修复”闭环。
