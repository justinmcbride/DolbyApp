from flask import Flask, jsonify

server = Flask(__name__)

@server.route('/')
def MainPage():
	return "Main Page"

if __name__ == '__main__':
    server.run()