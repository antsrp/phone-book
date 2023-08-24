import setup
import handler
import atexit

def main():
    conf = setup.setup_config()
    if conf == None:
        return
    storage = setup.create_storage(conf)

    handler.handle_input(storage)
    atexit.register(storage.save)

if __name__ == "__main__":
    main()