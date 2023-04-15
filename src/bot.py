from bot import build


def main():
    app = build()

    app.run_webhook(
        listen='0.0.0.0',
        port='8000',
        secret_token='228322aza',
        webhook_url='fdasdsfegsf342.loca.lt',
    )


if __name__ == "__main__":
    main()
