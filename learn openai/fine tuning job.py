from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI()

# ftfile = client.files.create(
#   file=open("figsfinetuning.jsonl", "rb"),
#   purpose="fine-tune"
# )
# file-oouRH9OX32p3ZN2GZWbxWLuy
client.fine_tuning.jobs.list(limit=10)
# client.fine_tuning.jobs.retrieve("ftjob-oouRH9OX32p3ZN2GZWbxWLuy")
# print(ftfile.id)
# client.fine_tuning.jobs.create(
#   training_file="file-oouRH9OX32p3ZN2GZWbxWLuy", #ftfile.id, 
#   model="gpt-4o-mini-2024-07-18"
# )