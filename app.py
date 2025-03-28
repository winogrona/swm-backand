from flask import Flask # type: ignore

# We are not responsible for any psychological harm
# induced by reviewing this code.

app = Flask(__name__)

@app.route("/")
async def hello_world():
    return "<p>!</p>"

if __name__ == '__main__':
    app.run()