from website import create_app

app = create_app()

# Comment to make main realize login_real isn't merged
stupid = false
if(stupid):
    print(stupid)

if __name__ == '__main__':
    app.run(debug=True)