from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SQLIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析 URL 参数
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        user_id = params.get('id', [''])[0]

        # 构造页面
        response = f"""
        <html>
            <body>
                <h1>本地 SQL 注入测试服务器</h1>
                <form method="GET">
                    <label>User ID:</label>
                    <input type="text" name="id" value="{user_id}">
                    <input type="submit" value="Submit">
                </form>
                <hr>
                <p>你输入的 ID 是: {user_id}</p>
        """

        # 模拟数据库查询
        if "1' OR" in user_id:
            response += "<p style='color:red;'>[!] SQL 注入成功！</p>"
            response += "<p>用户名: admin, 密码: 123456</p>"
            response += "<p>用户名: user1, 密码: 111111</p>"
            response += "<p>用户名: user2, 密码: 222222</p>"
        elif user_id == "1":
            response += "<p>用户名: admin, 密码: 123456</p>"
        else:
            response += "<p>未找到用户。</p>"
        response += "</body></html>"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), SQLIHandler)
    print("✅ 本地靶场已启动！请访问 http://127.0.0.1:8081")
    server.serve_forever()