
import json
from datetime import datetime, timedelta
from config.settings import mongo_configs
from runner.mongo_utils import initialise_mongo_cloud_db_client, input_document_list_into_mongo_db_collection


client = initialise_mongo_cloud_db_client(
    mongo_configs["MONGO_PASSWORD"], mongo_configs["MONGO_USERNAME"],
    mongo_configs["MONGO_CLUSTER"]
)

# Set the batch interval to 24 hours
batch_interval = timedelta(hours=24)


def add_data_to_file(data, write_file: str = "db/data.json"):
    # Append the data to a JSON file along with a timestamp
    with open(write_file, "a+") as f:
        json.dump({"data": data, "timestamp": datetime.utcnow().isoformat()}, f)
        f.write("\n")


def flush_file_to_mongodb_and_blob():
    # ========================
    # Send metadata to mongodb
    # ========================

    try:
        with open("data.json", "r+") as f:
            data_to_send = []
            for line in f:
                data = json.loads(line)
                if (
                    datetime.utcnow() - datetime.fromisoformat(data["timestamp"])
                    >= batch_interval
                ):
                    data_to_send.append(data["data"])

        input_document_list_into_mongo_db_collection(
            client, mongo_configs["RAG_DB_NAME"], mongo_configs["RAG_COLL_NAME"], data_to_send
        )

        # Remove the sent data from the file
        with open("data.json", "w+") as f:
            for line in f:
                data = json.loads(line)
                if (
                    datetime.utcnow() - datetime.fromisoformat(data["timestamp"])
                    < batch_interval
                ):
                    json.dump(data, f)
                    f.write("\n")

        print("Chat metadata successfully flushed to DB")
    except Exception as reason:
        print(f"Exception has occured :--: Reasons due to {reason}")
    