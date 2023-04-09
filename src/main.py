import subprocess
import time

from bot import build


def main():
    app = build()

    command = 'lt -p 8000 -s fdshfusdhfsd78f'
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        start_new_session=True,
    )
    time.sleep(1)
    output = process.stdout.readline()
    url = output.decode().strip().split(': ')[1]

    print(url)

    app.run_webhook(listen='0.0.0.0', port='8000', secret_token='228322aza', webhook_url=url)


if __name__ == "__main__":
    main()
