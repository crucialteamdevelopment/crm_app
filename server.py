import http.server
import socketserver

# Указываем порт для веб-сервера
PORT = 5555

# Создаем обработчик запросов, который будет раздавать файлы из текущей директории
Handler = http.server.SimpleHTTPRequestHandler

# Создаем объект TCPServer
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    # Запускаем сервер
    httpd.serve_forever()
