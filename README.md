## What does the project do?

1. create new machine from digitalocean(from [here](https://github.com/koalalorenzo/python-digitalocean))
2. update TCP congestion algorithm(from [here](https://github.com/tcp-nanqinlang/general))
3. deploy SSR(from [here](https://github.com/shadowsocksrr/shadowsocksr))

All I did was mix them together.

## Quick start

1. clone project to your machine
2. modifiy `settings.py` file

   * update the digitalocean token
   * update public key location
   * update ssr config

3. install requirements

    ```
    pip install -r requirements.txt
    ```

4. run `main.py` file

    ```
    python main.py
    ``` 

### TODO:

1. Send the message to the email after completion
2. Run forever until the event is received and then work
3. Waiting

Beacuse of i'm a lazy man, and my server here is always blocked. I don't want wast my time in deploying. so here i am.

