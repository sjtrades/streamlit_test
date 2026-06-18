import os
import pandas as pd
import pyarrow.parquet as pq


def load_single_file(filepath):
    table = pq.read_table(filepath)
    df = table.to_pandas()

    df["event"] = df["event"].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)

    return df

def is_bot(user_id):
    return str(user_id).isdigit()

def load_all_data(data_folder):
    frames = []

    for day_folder in os.listdir(data_folder):
        day_path = os.path.join(data_folder, day_folder)

        if not os.path.isdir(day_path):
            continue

        for file_name in os.listdir(day_path):
            file_path = os.path.join(day_path, file_name)

            try:
                table = pq.read_table(file_path)
                # print(table.schema.field("ts"))
                # break
                df = table.to_pandas()

                df["event"] = df["event"].apply(
                    lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
                )

                df["date"] = day_folder
                df["is_bot"] = df["user_id"].apply(is_bot)

                frames.append(df)

            except Exception as e:
                print(f"Failed loading {file_name}: {e}")

    return pd.concat(frames, ignore_index=True)

