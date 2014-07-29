if __name__ == "__main__":
    import threading
    from sris import app, manager
    # I'm not entirely happy with this solution, but it works!
    threading.Timer(10, manager.Manager().send_initial_sms).start()
    app.run()
