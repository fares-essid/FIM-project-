import logging

logging.basicConfig(
    filename="logs/fim.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def alert(message):
    print(message)
    logging.info(message)