import os


def execute_command():
    # fab command -i /path/to/key.pem [-H [user@]host[:port]]
    os.system("fab deploy -i ~/.ssh/basket_together.pem -H ubuntu@52.78.69.17")


if __name__ == "__main__":
    execute_command()